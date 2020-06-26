import os
from config import config_private as cfgp


def number_or_not(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


if __name__ == '__main__':
    folder_path = cfgp.save_path
    dataset_list_path = os.path.join(folder_path, 'all_list.txt')
    all_list = os.listdir(folder_path)
    all_path_list = []
    count = 0
    for f in all_list:
        fn, ext = os.path.splitext(f)
        if ext == '.csv' and number_or_not(fn[:6]):
            all_path_list.append(os.path.join(folder_path, f))
            count += 1

    print(count)

    all_str = '\n'.join(all_path_list)
    with open('tactics/all_list.txt', 'w') as f:
        f.write(all_str)
    with open('playback/all_list.txt', 'w') as f:
        f.write(all_str)
    with open(dataset_list_path, 'w') as f:
        f.write(all_str)
