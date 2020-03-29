import torch
import time

from fc_net import fc_net
from loss import PredLoss
from stocksdata_loader import StockDataset
from torch.utils.data import DataLoader

import config

def test(device):
    test_dataset = StockDataset(config.data_path, train_flag=True)
    test_data_loader = DataLoader(test_dataset, shuffle=False, batch_size=1,
                                   num_workers=config.num_workers)

    net = fc_net(5, len(config.pred_time), window=config.window_size)

    net.load_state_dict(torch.load(config.infer_path, map_location=device))
    print("Successfully loaded trained ckpt at {}".format(config.infer_path))
    net.eval()
    net.to(device)

    win_cnt = 0
    precision = 0
    total_cnt = 0

    for i, sample in enumerate(test_data_loader):
        input_data = sample['window'].to(device)
        label = sample['label'].to(device)

        prediction = net(input_data)

        print("pred", prediction, "label", label)

        prediction = prediction[0][0].cpu()
        label = label[0][0].cpu()

        # print(prediction > 1.0)

        if prediction > 1.0 and label > 1.0:
            win_cnt += 1
            if abs(prediction - label) < 0.05:
                precision += 1
        if prediction <= 1.0 and label <= 1.0:
            win_cnt += 1
            if abs(prediction - label) < 0.05:
                precision += 1

        total_cnt += 1

    win_rate = 1.0 * win_cnt / total_cnt
    precision /= (1.0 * total_cnt)

    return win_rate, precision


if __name__ == "__main__":
    device = torch.device('cuda:0')
    wr, prec = test(device)
    print("wr", wr)
    print("prec", prec)

