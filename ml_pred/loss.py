import torch
import torch.nn as nn


class PredLoss(nn.Module):
    def __init__(self):
        super(PredLoss, self).__init__()
        # self.loss = torch.nn.BCELoss(reduce=True, reduction='mean')
        # self.loss = torch.nn.L1Loss(reduce=False, reduction='mean')
        self.loss = torch.nn.CrossEntropyLoss()
        self.relu = torch.nn.ReLU6()

    def forward(self, preds, targets):
        (b, k) = preds.shape
        # ratio_loss = self.loss(torch.abs(preds), torch.abs(targets))
        # # penalty = torch.exp(torch.neg(preds.mul(targets)))  # if oppose, penalty will > 1
        # penalty = self.relu(torch.neg(preds.mul(targets))) + 1
        # # loss = self.loss(preds, targets)

        loss = self.loss(preds, targets)

        # print(ratio_loss.shape)
        return loss


def test():
    import time

    # device = torch.device('cuda')
    preds = torch.randn((2, 7))
    targets = torch.randn((2, 7))
    net = PredLoss()
    start = time.clock()
    test_iter = 10000
    for i in range(test_iter):
        loss = net(preds, targets)
    end = time.clock()

    print('Running time: %f ms' % ((end - start) * 1000 / test_iter))
    print('preds', preds)
    print('targets', targets)
    print('loss', loss)

if __name__ == '__main__':
    test()