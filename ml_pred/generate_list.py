import os
import random

folder_path = os.getcwd()
folder_path = os.path.join(folder_path, 'data/')
all_list = os.listdir(folder_path)

train_cnt = 1404
test_cnt = len(all_list) - train_cnt

train_list = random.sample(all_list, train_cnt)
test_list = list(set(all_list) ^ set(train_list))

train_path_list = []
for f in train_list:
    train_path_list.append(os.path.join(folder_path, f))

test_path_list = []
for f in test_list:
    test_path_list.append(os.path.join(folder_path, f))

train_str = '\n'.join(train_path_list)
test_str = '\n'.join(test_path_list)

with open('train_list.txt', 'w') as f:
    f.write(train_str)

with open('test_list.txt', 'w') as f:
    f.write(test_str)