import torch
import time

from fc_net import fc_net
from loss import PredLoss
from stocksdata_loader import StockDataset
from torch.utils.data import DataLoader

import numpy as np

import config


def normal_init(parm):
    torch.nn.init.normal_(parm, mean=0.0, std=0.01)


def weights_init(m):
    print(m)
    if isinstance(m, torch.nn.Linear):
        normal_init(m.weight.data)
        normal_init(m.bias.data)


def train(device):
    train_dataset = StockDataset(config.data_path, train_flag=True)
    train_data_loader = DataLoader(train_dataset, shuffle=True, batch_size=config.batch_size,
                                   num_workers=config.num_workers)

    net = fc_net(5, len(config.cls), window=config.window_size)
    net.apply(weights_init)
    net.to(device)
    if config.resume:
        net.load_state_dict(torch.load(config.old_model_path), map_location=device)
        print("Successfully loaded trained ckpt at {}".format(config.old_model_path))
    loss_op = PredLoss().to(device)

    if config.method == 'SGD':
        optimizer = torch.optim.SGD(net.parameters(), lr=config.lr, momentum=config.momentum)
    elif config.method == 'Adam':
        optimizer = torch.optim.Adam(net.parameters(), lr=config.lr, weight_decay=config.weight_decay)

    # optimizer = torch.optim.SGD(net.parameters(), lr=config.lr, momentum=config.momentum)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=config.lr_decay, gamma=config.gamma)

    net.train()
    optimizer.zero_grad()

    start = time.time()
    iter = 0
    for epoch in range(config.max_epoch):
        for i, sample in enumerate(train_data_loader):

            scheduler.step()

            input_data = sample['window'].to(device)
            label = sample['label'].to(device).long()

            # print(input_data.dtype)

            prediction = net(input_data)

            # print(prediction.shape, label.shape)

            # print(prediction.shape, label.shape)
            loss = loss_op(prediction, label)
            loss.backward()

            optimizer.step()
            optimizer.zero_grad()

            # for name, param in net.named_parameters():
            #     if name == 'fc1.weight':
            #         print(name, param[0:10])

            if iter % config.print_every == 0:
                mid = time.time()
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' '
                print_str = time_str + "Epoch " + str(epoch) + \
                            " Iter " + str(iter) + ": Loss = " + '%.6f' % loss + \
                            ', Elapsed time = %f s' % (mid - start)
                print(print_str)

            iter += 1

        if epoch == config.max_epoch or epoch % config.save_every == 0:
            model_path = config.model_prefix + 'epoch_%04d.pkl' % epoch
            torch.save(net.state_dict(), model_path)
            print('Checkpoint saved at {}').format(model_path)

    print("Finish training!")


if __name__ == "__main__":
    device = torch.device('cpu')
    train(device)
