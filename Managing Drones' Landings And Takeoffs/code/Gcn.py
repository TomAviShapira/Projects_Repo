import warnings

warnings.filterwarnings('ignore', category=FutureWarning)

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter


#  tensorboard --logdir=projectB_tom/runs --max_reload_threads 4 # debug


class Net(nn.Module):

    def __init__(self, features_in, hidden):
        super(Net, self).__init__()
        self.linear_1 = nn.Linear(features_in, hidden, bias=True)
        nn.init.xavier_uniform.__init__(self.linear_1.weight)
        self.linear_2 = nn.Linear(hidden, hidden, bias=True)
        nn.init.xavier_uniform.__init__(self.linear_2.weight)
        self.linear_3 = nn.Linear(hidden, 1, bias=True)
        nn.init.xavier_uniform.__init__(self.linear_3.weight)
        self.num_of_lanes_transform = nn.Linear(1, features_in, bias=True)
        nn.init.xavier_uniform.__init__(self.num_of_lanes_transform.weight)

    def forward(self, normalized_a_mat, x):
        planes_f = x[0]
        lanes_f = x[1]
        lanes_f = self.num_of_lanes_transform(lanes_f)
        lanes_f = nn.functional.softplus(lanes_f)
        x = torch.cat((planes_f, lanes_f), 1)

        x = self.linear_1(normalized_a_mat @ x)
        x = nn.functional.softplus(x)
        x = self.linear_2(normalized_a_mat @ x)
        x = nn.functional.softplus(x)
        x = self.linear_3(normalized_a_mat @ x)

        return x


def trainer(dataset):
    net = Net(3, 10)
    if torch.cuda.is_available():
        net.to(torch.device("cuda:0"))
    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=0.0025)
    writer = SummaryWriter()

    iteration = 0
    validation_set_index = -1
    while iteration < 30000:  # each while loop is epoch
        validation_loss = 0
        validation_set_len = 5
        validation_set_index = (validation_set_index + 1) % 5
        for i in range(len(dataset)):
            optimizer.zero_grad()  # we need to set the gradients to zero before starting to do backpropragation
                                   # because PyTorch accumulates the gradients on subsequent backward passes.
            output = net(dataset[i][0], dataset[i][1])
            loss = criterion(output, dataset[i][2])
            if dataset[i][3] == validation_set_index:  # validation set in this iteration.
                validation_loss += loss
            else:  # training set in this iteration.
                net.train()  # sets the mode to train. tells the model that we are training the model.
                writer.add_scalar('Training Loss', loss, iteration)
                loss.backward()  # Computes dloss/df for every parameter f which has requires_grad=True.
                                 # These are accumulated into f.grad for every parameter f.
                clipping_value = 1
                torch.nn.utils.clip_grad_norm_(net.parameters(), clipping_value)
                optimizer.step()  # Does the update
                for name, param in net.named_parameters():
                    if param.requires_grad:
                        writer.add_histogram(name, param, iteration)

                net.eval()  # sets the mode to test. tells the model that we are testing the model.

            iteration += 1

        validation_loss /= validation_set_len
        writer.add_scalar('Validation Loss', validation_loss, iteration)
    torch.save(net.state_dict(), 'saved_net.txt')

