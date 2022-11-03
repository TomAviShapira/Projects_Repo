import multiprocessing
import PySimpleGUI as sg
import torch
import numpy as np

from playsound import playsound
from projectB_tom.Exec import exec_
from projectB_tom.Plane import Plane
from projectB_tom.Gcn import Net


def fromGui():
    # sg.theme_previewer()
    sg.theme("Dark Brown")

    with open('welcome.txt') as wfp:
        line = wfp.readline()
        welcome_txt = ""
        while line:
            welcome_txt += line
            line = wfp.readline()
    with open('instructions.txt') as ifp:
        line = ifp.readline()
        instructions_txt = ""
        while line:
            instructions_txt += line
            line = ifp.readline()

    layout = [[sg.Menu([['Help', 'About'], ])],
              [sg.Text(welcome_txt, size=(70, 7), font=("Any 15", 15), justification='center')],
              [sg.Image(filename='plane.PNG', key='image', pad=(240, 0))],
              [sg.Text('\n')],
              [sg.Button('Start'), sg.Button('Close All'), sg.Checkbox('Sound', default=False, key='-SOUND-')]]
    window = sg.Window('Planning Arrivals and Departures', layout)
    window2 = []

    num_of_planes = 0
    num_of_lanes = 0
    pilot_sound = -1
    shalom_sound = -1
    lo_sound = -1
    while True:  # Event Loop
        event, values = window.read()
        if event in (None, 'Exit') or event == 'Close All':
            if pilot_sound != -1:
                pilot_sound.terminate()
            if shalom_sound != -1:
                shalom_sound.terminate()
            if lo_sound != -1:
                lo_sound.terminate()
            break
        if not int(values['-SOUND-']):
            if pilot_sound != -1:
                pilot_sound.terminate()
            if shalom_sound != -1:
                shalom_sound.terminate()
            if lo_sound != -1:
                lo_sound.terminate()
        if event == 'About':
            sg.popup('Planning Arrivals and Departures\n',
                     'This software was developed by Tom Avi Shapira and Bar\nMamran'
                     ' as part of Project B in the Faculty of Electrical\nEngineering at the Technion.\n'
                     'Supervisor: Ayal Taitler\n\n'
                     'All rights reserved Ⓒ'
                     '\n\n')
        if event == 'Instructions':
            sg.popup('Planning Arrivals and Departures\n', instructions_txt)
        if event == 'Start' or event == 'Back':
            window.close()
            if event == 'Start':
                if int(values['-SOUND-']):
                    pilot_sound = multiprocessing.Process(target=playsound, args=("pilot.mp3",))
                    pilot_sound.start()
            txt = 'Please enter: \n'
            layout = [[sg.Menu([['Help', 'About'], ])],
                      [sg.Text(txt, font='Any 15')],
                      [sg.Text('Number of planes: ', size=(13, 1)), sg.Input(key='-Number of planes-')],
                      [sg.Text('Number of lanes: ', size=(13, 1)), sg.Input(key='-Number of lanes-')],
                      [sg.Text('')],
                      [sg.Button('Continue'), sg.Button('Close All'),
                       sg.Checkbox('Sound', default=bool(values['-SOUND-']), key='-SOUND-')]]
            window = sg.Window('Planning Arrivals and Departures', layout)
        if event == 'Continue':
            window.close()
            num_of_planes = int(values['-Number of planes-'])
            num_of_lanes = int(values['-Number of lanes-'])
            info_l = [[sg.Menu([['Help', ['Instructions', 'About']], ])],
                      [sg.Text('Number of planes: ' + str(num_of_planes))],
                      [sg.Text('Number of lanes: ' + str(num_of_lanes))],
                      [sg.Text('Maximum run time [seconds] (recommended): '),
                       sg.Input(str(10), size=(7, 1), key='-Max run time-')]]
            headings = ['    Plane Id', '       Start Day Min', ' Start Day Max', 'Mission Duration',
                        '    Max Fuel', '        End Day', '         [Minutes]', '           Status']
            header_l = [[sg.Text(h) for h in headings]]
            input_l = [[inputFunc(i, j)
                        for j in range(8)] for i in range(num_of_planes)]
            button_l = [[sg.Button('Back'), sg.Button('Run'), sg.Button('Close All'),
                         sg.Checkbox('Sound', default=bool(values['-SOUND-']), key='-SOUND-')]]
            layout = info_l + header_l + input_l + [[sg.Text('')]] + button_l
            window = sg.Window('Planning Arrivals and Departures', layout)
        if event == 'Run':
            max_run_time = int(values['-Max run time-'])
            planes = []
            state = []
            chosen_lanes = []
            cnt = 0
            for i in range(num_of_planes):
                start_day_min = int(values[str(i) + str(1)])
                start_day_max = int(values[str(i) + str(2)])
                mission_duration = int(values[str(i) + str(3)])
                max_fuel_time = int(values[str(i) + str(4)])
                end_day_time = int(values[str(i) + str(5)])
                init_state = values[str(i) + str(7)]
                init_state_code = getInitStateCode(init_state)
                pl = Plane(cnt, [start_day_min, start_day_max], [mission_duration, max_fuel_time],
                           end_day_time, init_state_code)
                cnt += 1
                planes.append(pl)
                state.append(pl.init_state)
                chosen_lanes.append([-1, -1])

            normalized_a_mat = createAdjacencyMatrix(planes)
            planes_f = createFeaturesMatrix(planes, normalized_a_mat.shape[1] - 1)
            lanes_f = np.expand_dims([[num_of_lanes]], axis=0)
            lanes_f = torch.tensor(lanes_f).float()
            net = Net(3, 10)
            net.load_state_dict(torch.load('saved_net.txt'))
            predicted_order = net(normalized_a_mat, [planes_f, lanes_f]).detach().numpy().squeeze()
            predicted_order_cnt = 0
            predicted_exec_order = []
            for i in planes:
                if i.init_state == 1:
                    predicted_exec_order.append([i.plane_id, predicted_order[predicted_order_cnt], "to"])
                    predicted_exec_order.append([i.plane_id, predicted_order[predicted_order_cnt + 1], "l"])
                    predicted_order_cnt += 2
                elif i.init_state == 5:
                    predicted_exec_order.append([i.plane_id, predicted_order[predicted_order_cnt], "l"])
                    predicted_order_cnt += 1
            predicted_exec_order.sort(key=lambda x: x[1])
            log_output = open('log_output.txt', mode='w')
            exec_return_val = exec_(num_of_planes, num_of_lanes, planes, state, chosen_lanes, 1, [], log_output, 1,
                                    max_run_time, None, predicted_exec_order)

            log_output.close()
            if exec_return_val[0]:
                if pilot_sound != -1:
                    pilot_sound.terminate()
                if int(values['-SOUND-']):
                    shalom_sound = multiprocessing.Process(target=playsound, args=("shalom.wav",))
                    shalom_sound.start()
                info_l = [[sg.Text('solution :\n', font='Any 15')],
                          [sg.Text('Operation', size=(12, 1)), sg.Text('Plane Id', size=(12, 1)),
                           sg.Text('Lane Id', size=(12, 1)),
                           sg.Text('Start Time', size=(12, 1)), sg.Text('Duration', size=(12, 1))],
                          [sg.Text('', size=(12, 1)), sg.Text('', size=(12, 1)),
                           sg.Text('', size=(12, 1)),
                           sg.Text('[Relatively', size=(12, 1)), sg.Text('[minutes]', size=(12, 1))],
                          [sg.Text('', size=(12, 2)), sg.Text('', size=(12, 2)),
                           sg.Text('', size=(12, 1)),
                           sg.Text('minute]', size=(12, 2)), sg.Text('', size=(12, 2))]]
                output_l = [[sg.Text(exec_return_val[1][i][j], size=(12, 1))
                             for j in range(5)] for i in range(len(exec_return_val[1]))]
                output_l = [[sg.Column(output_l, scrollable=True, size=(550, 300))]]
                layout = info_l + output_l + [[sg.Button('Re-Planning')]]
            else:
                if pilot_sound != -1:
                    pilot_sound.terminate()
                if int(values['-SOUND-']):
                    lo_sound = multiprocessing.Process(target=playsound, args=("lo.wav",))
                    lo_sound.start()
                info_l = [[sg.Text('can not find solution.')]]
                layout = info_l + [[sg.Button('Re-Planning')]]
            window2 = sg.Window('Planning Arrivals and Departures', layout)
            event, values = window2.read()
        if event == 'Re-Planning':
            if shalom_sound != -1:
                shalom_sound.terminate()
            if lo_sound != -1:
                lo_sound.terminate()
            window2.close()


def inputFunc(i, j):
    if j == 0:
        if i < 10:
            return sg.Text(str(i) + '  ', pad=(42, 3))
        else:
            return sg.Text(str(i), pad=(42, 3))
    elif j == 6:
        return sg.Text('  ', pad=(42, 3))
    elif j == 7:
        return sg.Combo(('On the ground', 'In the air'),
                        key=str(i) + str(j), default_value='On the ground', readonly=True, text_color='Dark Brown',
                        background_color='Dark Brown')
    else:
        return sg.Input(str(-1), size=(14, 1), key=str(i) + str(j), pad=(0, 3))


def getInitStateCode(argument):
    switcher = {
        "On the ground": 1,
        "In the air": 5,
    }
    return switcher.get(argument, "nothing")


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

