mode="train"
encoder="classifier"
dropout=0.1
bertpath="/home/ubuntu/workspace/YJH/KorBertSum/bert_data/korean"
modelpath="./models/bert_classifier_test"
lr=2e-3
v_gpu=0
gpu_r=0
bert_model="/home/ubuntu/workspace/YJH/korBert_models/001_bert_morp_pytorch"
bert_config_path="/home/ubuntu/workspace/YJH/korBert_models/001_bert_morp_pytorch/bert_config.json"

# train #
python3 ./src/train.py -mode train -encoder $encoder -dropout $dropout -bert_data_path $bertpath -model_path $modelpath -lr $lr -visible_gpus $v_gpu -gpu_ranks $gpu_r -world_size 1 -report_every 50 -save_checkpoint_steps 1000 -batch_size 1000 -decay_method noam -train_steps 1000 -accum_count 1 -log_file ./logs/bert_classifier -use_interval true -warmup_steps 8000 -bert_model $bert_model -bert_config_path $bert_config_path -temp_dir .

# validate #
#python train.py -mode validate -bert_data_path $bertpath -model_path $modelpath  -visible_gpus $v_gpu  -gpu_ranks $gpu_r -batch_size 1000  -log_file ./logs/bert_classifier  -result_path ./results/korean -bert_model $bert_model

# test #

#python train.py -mode test -bert_data_path /content/bert_data/korean -model_path ../models/bert_classifier  -visible_gpus 0  -gpu_ranks 0 -batch_size 1000  -log_file ../logs/bert_classifier  -result_path ../results/korean -bert_model /content/001_bert_morp_pytorch -test_from ./models/bert_classifier/model_step_1000.pt
