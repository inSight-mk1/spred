window_size = 250
pred_time = [10]

cls = [0.2, 0.15, 0.1, 0.05, 0.0, -0.05, -0.10, -0.15, -0.2, -1.0]
cls = [0.05, -0.05, -1.0]

data_path = '.'

batch_size = 64
num_workers = 16

method = 'Adam'
weight_decay = 0.0001
lr = 0.0001
momentum = 0.9
lr_decay = 2000
gamma = 0.5
max_iter = 100000
max_epoch = 4000
print_every = 5
save_every = 10

resume = False
old_model_path = None

model_prefix = "./trained_models/test_"

infer_path = "./trained_models/test_epoch_0120.pkl"
