#python src/run_weighting_experiment.py --dataset census --method none --bias none --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method none --bias oversampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method none --bias undersampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method none --bias age --bias_sample_size 1000

#python src/run_weighting_experiment.py --dataset census --method logistic_regression --bias none --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method logistic_regression --bias oversampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method logistic_regression --bias undersampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method logistic_regression --bias age --bias_sample_size 1000

#python src/run_weighting_experiment.py --dataset census --method random_forest --bias none --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method random_forest --bias oversampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method random_forest --bias undersampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method random_forest --bias age --bias_sample_size 1000

#python src/run_weighting_experiment.py --dataset census --method neural_network_classifier --bias none --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method neural_network_classifier --bias oversampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method neural_network_classifier --bias undersampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method neural_network_classifier --bias age --bias_sample_size 1000

#python src/run_weighting_experiment.py --dataset census --method neural_network_mmd_loss --bias none --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method neural_network_mmd_loss --bias oversampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method neural_network_mmd_loss --bias undersampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method neural_network_mmd_loss --bias age --bias_sample_size 1000

# python src/run_weighting_experiment.py --dataset census --method domain_adaptation --bias none --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method domain_adaptation --bias oversampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method domain_adaptation --bias undersampling --bias_sample_size 1000
python src/run_weighting_experiment.py --dataset census --method domain_adaptation --bias age --bias_sample_size 1000

#python src/run_weighting_experiment.py --dataset census --method random --bias none --bias_sample_size 1000
#python src/run_weighting_experiment.py --dataset census --method random --bias oversampling --bias_sample_size 1000
#python src/run_weighting_experiment.py --dataset census --method random --bias undersampling --bias_sample_size 1000
#python src/run_weighting_experiment.py --dataset census --method random --bias age --bias_sample_size 1000

#python src/run_weighting_experiment.py --dataset census --method mrs --bias none --bias_sample_size 1000
#python src/run_weighting_experiment.py --dataset census --method mrs --bias oversampling --bias_sample_size 1000
#python src/run_weighting_experiment.py --dataset census --method mrs --bias undersampling --bias_sample_size 1000
#python src/run_weighting_experiment.py --dataset census --method mrs --bias age --bias_sample_size 1000