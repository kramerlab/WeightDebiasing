from pathlib import Path
import torch
import shap
from scipy.spatial.distance import pdist
from utils.models import WeightingMlp
from .loss import WeightedMMDLoss
import numpy as np
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import ReduceLROnPlateau

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def neural_network_mmd_loss_weighting(
    N, R, columns, use_batches=False, early_stopping=True, *args, **attributes
):
    passes = 8000
    bias_variable = attributes["bias_variable"]
    bias_values = None
    if bias_variable is not None:
        bias_values = N[bias_variable]

    tensor_N = torch.FloatTensor(N[columns].values)
    tensor_R = torch.FloatTensor(R[columns].values)
    number_of_features = tensor_N.shape[1]
    latent_feature_list = [
        number_of_features,
        int(number_of_features * 0.75),
        int(number_of_features * 1.25),
    ]
    best_mmd = np.inf
    best_model = None
    best_mmd_list = None
    best_mean_list = None
    if bias_values is not None:
        bias_values = torch.FloatTensor(bias_values.values).to(device)

    for latent_features in latent_feature_list:
        mmd_model, mmd_list, mmd, means = compute_model(
            passes,
            tensor_N,
            tensor_R,
            use_batches=use_batches,
            latent_features=latent_features,
            bias_values=bias_values,
        )
        if mmd < best_mmd:
            best_model = mmd_model
            best_mmd_list = mmd_list
            best_mean_list = means

    # plot_line(best_mmd_list, save_path, "MMDs_per_pass")
    if bias_values is not None:
        attributes["mean_list"].append(best_mean_list)
        attributes["mmd_list"].append(best_mmd_list)

    with torch.no_grad():
        tensor_N = tensor_N.to(device)
        weights = best_model(tensor_N).cpu().squeeze().numpy()
    return weights


def compute_model(
    passes,
    tensor_N,
    tensor_R,
    patience=500,
    use_batches=False,
    latent_features=1,
    bias_values=None,
):
    model_path = Path("best_model_mmd_loss.pt")
    mmd_list = []
    batch_size = 512
    learning_rate = 0.001
    means = []

    gamma = calculate_rbf_gamma(np.append(tensor_N, tensor_R, axis=0))
    mmd_loss_function = WeightedMMDLoss(gamma, len(tensor_R), device)

    tensor_N = tensor_N.to(device)
    tensor_R = tensor_R.to(device)

    if bias_values is not None:
        validation_weights = (torch.ones(len(tensor_N)) / len(tensor_N)).to(device)
        positive_value = torch.sum(bias_values * validation_weights.squeeze())
        means.append(positive_value.cpu())

    best_mmd = torch.inf
    mmd_model = WeightingMlp(tensor_N.shape[1], latent_features).to(device)
    optimizer = torch.optim.Adam(
        mmd_model.parameters(), lr=learning_rate, weight_decay=1e-5
    )
    scheduler = ReduceLROnPlateau(optimizer, patience=int(patience / 2))
    for _ in range(passes):
        mmd_model.train()
        optimizer.zero_grad()

        if use_batches:
            training_indices = np.random.choice(batch_size, batch_size)
            training_data = tensor_N[training_indices]
            reference_indices = np.random.choice(
                len(tensor_R), len(tensor_R), replace=True
            )
            reference_data = tensor_R[reference_indices]
        else:
            training_data = tensor_N
            reference_data = tensor_R

        train_weights = mmd_model(training_data)
        mmd_loss = mmd_loss_function(training_data, reference_data, train_weights)
        if not torch.isnan(mmd_loss) and not torch.isinf(mmd_loss):
            loss = mmd_loss
            loss.backward()
            optimizer.step()

        mmd, validation_weights = validate_model(
            tensor_N, tensor_R, mmd_loss_function, mmd_model
        )
        mmd_list.append(mmd.cpu().numpy())

        if mmd < best_mmd:
            best_mmd = mmd
            torch.save(mmd_model.state_dict(), model_path)

        scheduler.step(mmd)
        if bias_values is not None:
            validation_weights = (validation_weights / sum(validation_weights)).to(
                device
            )
            positive_value = torch.sum(bias_values * validation_weights.squeeze())
            means.append(positive_value.cpu())

    mmd_model.load_state_dict(torch.load(model_path))
    mmd_model.eval()

    return mmd_model, np.squeeze(mmd_list), best_mmd, means


def validate_model(tensor_N, tensor_R, mmd_loss_function, mmd_model):
    mmd_model.eval()
    with torch.no_grad():
        validation_weights = mmd_model(tensor_N)
    mmd = mmd_loss_function(
        tensor_N,
        tensor_R,
        validation_weights,
    )

    return mmd, validation_weights


def compute_shap_values(model, tensor_N, columns, save_path):
    # Compute SHAP values to measure and visualise the bias
    model = model.cpu()
    with torch.no_grad():
        kernelExplainer = shap.Explainer(model, tensor_N, feature_names=columns)
        shap_values = kernelExplainer(tensor_N)
        shap.summary_plot(shap_values, tensor_N, show=False)
        plt.savefig(f"{save_path}/shap_summary.pdf")
        plt.clf()
        shap.plots.bar(shap_values, show=False)
        plt.savefig(f"{save_path}/shap_bars.pdf")
        plt.clf()


def calculate_rbf_gamma(aggregate_set):
    all_distances = pdist(aggregate_set, "euclid")
    sigma = np.median(all_distances)
    return 1 / (2 * (sigma**2))
