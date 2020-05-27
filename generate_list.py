import os
from config import config_private as cfgp

folder_path = cfgp.save_path
dataset_list_path = os.path.join(folder_path, 'all_list.txt')
all_list = os.listdir(folder_path)
all_path_list = []
for f in all_list:
    if os.path.splitext(f)[1] == '.csv':
        all_path_list.append(os.path.join(folder_path, f))

all_str = '\n'.join(all_path_list)
with open('tactics/all_list.txt', 'w') as f:
    f.write(all_str)
with open('playback/all_list.txt', 'w') as f:
    f.write(all_str)
with open(dataset_list_path, 'w') as f:
    f.write(all_str)
