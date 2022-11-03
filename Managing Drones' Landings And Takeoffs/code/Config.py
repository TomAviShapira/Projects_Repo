import sys
import os
import torch
import numpy as np
import random
from copy import deepcopy

from projectB_tom.Exec import exec_
from projectB_tom.Gcn import trainer, Net
from projectB_tom.Plane import Plane


def fromConfigFile(gcn_mode):
    dataset = []
    exec_order = []
    sorted_configs = []
    configs = os.listdir('configs/')
    configs_num = [int(i[6:-4]) for i in configs]
    for i in range(len(configs)):
        sorted_configs.append([configs[i], configs_num[i]])
    sorted_configs = sorted(sorted_configs, key=lambda x: x[1])

    for i in [i[0] for i in sorted_configs]:
        # if i != 'config24.txt':  # debug
        #  continue
        exec_order.clear()
        with open('configs/' + i) as cfp:
            line = cfp.readline()
            num_of_planes = [int(s) for s in line.split() if s.isdigit()][0]
            line = cfp.readline()
            num_of_lanes = [int(s) for s in line.split() if s.isdigit()][0]
            line = cfp.readline()
            max_run_time = [int(s) for s in line.split() if s.isdigit()][0]
            # max_run_time = 60  # debug

            planes = []
            state = []
            chosen_lanes = []
            cnt = 0
            line = cfp.readline()
            while line:
                times = [int(s) for s in line.split() if s.isdigit()]
                pl = Plane(cnt, [times[0], times[1]], [times[2], times[3]], times[4], times[5])
                if pl.init_state == 1:
                    exec_order.append([pl.plane_id, times[6], "to"])
                    exec_order.append([pl.plane_id, times[7], "l"])
                elif pl.init_state == 5:
                    exec_order.append([pl.plane_id, times[6], "l"])
                cnt = cnt + 1
                planes.append(pl)
                if gcn_mode == 0:  # run with exec_ normally
                    state.append(pl.init_state)
                    chosen_lanes.append([-1, -1])
                line = cfp.readline()

        normalized_a_mat = createAdjacencyMatrix(planes)
        planes_f = createFeaturesMatrix(planes, normalized_a_mat.shape[1] - 1)
        lanes_f = np.expand_dims([[num_of_lanes]], axis=0)
        lanes_f = torch.tensor(lanes_f).float()
        lanes_f.requires_grad = True
        if torch.cuda.is_available():
            lanes_f = lanes_f.to(torch.device("cuda:0"))
        if gcn_mode == 0:  # run exec_
            net = Net(3, 10)
            net.load_state_dict(torch.load('saved_net.txt'))
            predicted_order = net(normalized_a_mat, [planes_f, lanes_f]).detach().numpy().squeeze()
            predicted_exec_order = deepcopy(exec_order)
            for j in range(len(predicted_exec_order)):
                predicted_exec_order[j][1] = predicted_order[j]
            exec_order.sort(key=lambda x: x[1])
            predicted_exec_order.sort(key=lambda x: x[1])
            is_print_full_solution = False
            log_output = open('log_output.txt', mode='w')
            # you can print to log_output by replace "sys.stdout" with "log_output"
            exec_(num_of_planes, num_of_lanes, planes, state, chosen_lanes, 0, i, sys.stdout, is_print_full_solution,
                  max_run_time, exec_order, predicted_exec_order)  # if you want to run with the true exec order,
                                                                   # replace "predicted_exec_order" with "exec_order".
        else:  # training gcn
            target = [i[1] for i in exec_order]
            target.append(num_of_lanes)
            target = [target]
            target = torch.tensor(target).float()
            target = torch.transpose(target, 0, 1)
            target = target.unsqueeze(0)
            if torch.cuda.is_available():
                target = target.to(torch.device("cuda:0"))
            dataset.append([normalized_a_mat, [planes_f, lanes_f], target, -1])

    if gcn_mode == 1:  # train gcn
        #  split dataset into groups. (cross-validation).
        random_indexes = random.sample(range(0, 25), 25)
        for i in range(len(random_indexes)):
            if i < 5:
                dataset[random_indexes[i]][3] = 0
            elif 5 <= i < 10:
                dataset[random_indexes[i]][3] = 1
            elif 10 <= i < 15:
                dataset[random_indexes[i]][3] = 2
            elif 15 <= i < 20:
                dataset[random_indexes[i]][3] = 3
            elif 20 <= i < 25:
                dataset[random_indexes[i]][3] = 4

        trainer(dataset)


def createAdjacencyMatrix(planes):
    n = 0
    for i in planes:
        if i.init_state == 1:
            n += 2
        elif i.init_state == 5:
            n += 1
    a_mat = np.eye(n + 1)
    d_mat = np.sum(a_mat, axis=0)
    d_mat = np.diag(d_mat)
    normalized_a_mat = np.linalg.inv(d_mat) @ a_mat
    normalized_a_mat = np.expand_dims(normalized_a_mat, axis=0)
    normalized_a_mat = torch.tensor(normalized_a_mat).float()
    normalized_a_mat.requires_grad = True
    if torch.cuda.is_available():
        normalized_a_mat = normalized_a_mat.to(torch.device("cuda:0"))
    return normalized_a_mat


def createFeaturesMatrix(planes, n):
    planes_f = np.zeros((n, 3))
    j = 0
    for i in planes:
        if i.init_state == 1:
            planes_f[j][0] = i.sd_duration[0]
            planes_f[j][1] = i.sd_duration[1] - i.sd_duration[0]
            planes_f[j][2] = i.day_duration
            planes_f[j + 1][0] = i.m_duration[0]
            planes_f[j + 1][1] = i.m_duration[1] - i.m_duration[0]
            planes_f[j + 1][2] = i.day_duration
            j += 2
        if i.init_state == 5:
            planes_f[j][0] = i.m_duration[0]
            planes_f[j][1] = i.m_duration[1] - i.m_duration[0]
            planes_f[j][2] = i.m_duration[1] + 20
            j += 1
    planes_f = np.expand_dims(planes_f, axis=0)
    planes_f = torch.tensor(planes_f).float()
    planes_f.requires_grad = True
    if torch.cuda.is_available():
        planes_f = planes_f.to(torch.device("cuda:0"))
    return planes_f
