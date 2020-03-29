import torch
import torch.nn as nn


class fc_net(nn.Module):
    def __init__(self, in_c, out_c, window):
        super(fc_net, self).__init__()
        self.out_chs = [8, 16, 32, 64, 64, 64, 4, 512, 4096]
        self.fc1 = nn.Linear(1, self.out_chs[0])
        self.conv1 = nn.Conv2d(1, self.out_chs[1], kernel_size=(13, 1))
        self.conv2 = nn.Conv2d(self.out_chs[1], self.out_chs[2], kernel_size=(5, 1))
        self.conv3 = nn.Conv2d(self.out_chs[2], self.out_chs[3], kernel_size=(3, 1))
        self.conv4 = nn.Conv2d(self.out_chs[3], self.out_chs[4], kernel_size=(3, 1))
        self.conv5 = nn.Conv2d(self.out_chs[4], self.out_chs[5], kernel_size=(3, 1))
        self.conv1x1 = nn.Conv2d(self.out_chs[5], self.out_chs[6], kernel_size=1)
        self.fc7 = nn.Linear(1 * (window - 0) * 5, self.out_chs[7])  # window - 12 - 4 - 2 - 2 - 2
        self.fc8 = nn.Linear(self.out_chs[7], self.out_chs[8])
        self.fc9 = nn.Linear(self.out_chs[8], out_c)
        self.actv = nn.LeakyReLU()
        self.dropout = nn.Dropout()
        self.softmax = nn.Softmax()

    def forward(self, input_x):
        # print(input.shape)
        (b, w, c) = input_x.shape
        ex_x = torch.unsqueeze(input_x, 1)
        # print(ex_x.shape)

        # conv1_x = self.conv1(ex_x)
        # act1_x = self.actv(conv1_x)
        #
        # conv2_x = self.conv2(act1_x)
        # act2_x = self.actv(conv2_x)
        #
        # conv3_x = self.conv3(act2_x)
        # act3_x = self.actv(conv3_x)

        # conv4_x = self.conv4(act3_x)
        # act4_x = self.actv(conv4_x)
        #
        # conv5_x = self.conv5(act4_x)
        # act5_x = self.actv(conv5_x)

        # conv6_x = self.conv1x1(act3_x)
        # act6_x = self.actv(conv6_x)

        # print(act6_x.shape)

        fc7_x = self.fc7(input_x.view(b, -1))
        act7_x = self.actv(fc7_x)
        dout7_x = self.dropout(act7_x)

        fc8_x = self.fc8(dout7_x)
        act8_x = self.actv(fc8_x)
        dout8_x = self.dropout(act8_x)

        fc9_x = self.fc9(dout8_x)
        # softmax = self.softmax(fc9_x)
        # act4_x = torch.sigmoid(fc4_x)

        return fc9_x


def test():
    import time

    # device = torch.device('cuda')
    x = torch.randn((2, 60, 8))
    net = fc_net(8, 7, window=60)
    start = time.clock()
    test_iter = 10000
    for i in range(test_iter):
        pred = net(torch.autograd.Variable(x))
    end = time.clock()

    print('Running time: %f ms' % ((end - start)*1000 / test_iter))
    print pred

if __name__ == '__main__':
    test()



