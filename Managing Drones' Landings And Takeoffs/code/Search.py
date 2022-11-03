from projectB_tom import Node
import gurobipy as gp
from queue import PriorityQueue
import math
import timeit
from copy import deepcopy
import PySimpleGUI as sg

from projectB_tom.Optimizer import optimizer, getOptimizerVars
from projectB_tom.Heuristic import heuristic


def search(init_node: Node, planes, start_time, is_gui, run_time):
    return_val = SearchReturnValue()

    open_node_cnt = 0  # debug variable

    open_Q = PriorityQueue()
    close_Q = PriorityQueue()
    entry_cnt = 0  # node ID
    init_node.entry_cnt = entry_cnt
    open_Q.put(init_node)

    m = gp.Model("bilinear")
    m.setParam("OutputFlag", 0)
    optimizer_vars = []
    optimizer_cons = []

    chosen_goal_time = math.inf
    is_goal = 0
    first_goal_time = 0
    num_of_goals = 0

    # gui - print progress bar
    layout = [[sg.Text('Running...')],
              [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')],
              [sg.Cancel()]]
    # create the window`
    window = sg.Window('Planning Arrivals and Departures', layout)
    progress_bar = window['progressbar']

    cnt = 0
    while not open_Q.empty():
        # gui - print progress bar
        if is_gui:
            # check to see if the cancel button was clicked and exit loop if clicked
            event, values = window.read(timeout=10)
            if event == 'Cancel' or event is None:
                return_val.is_cancel = 1
                window.close()
                return return_val
            # update bar with loop value +1 so that bar eventually reaches the maximum
            if cnt == 1000:
                cnt = 0
            progress_bar.UpdateBar(cnt + 1)
        cnt += 1

        current_time = timeit.default_timer()
        open_node_cnt += 1
        if not is_goal:
            if current_time - start_time > run_time:
                window.close()
                return return_val
        else:
            if current_time - first_goal_time > 0:
                window.close()
                return return_val
        node = open_Q.get()
        close_Q.put(node)

        optimizer_Sol_count = optimizer(m, node, optimizer_vars, optimizer_cons)
        if optimizer_Sol_count == 0:
            for i in range(0, len(node.constrains)):
                m.remove(m.getConstrByName(str(node.entry_cnt) + str(i)))  # problem: remove also necessary constraint
                optimizer_cons.remove(node.constrains[i])  # not needed if we use "is_con_exist" function
            m.update()
            continue

        if node.isGoal():
            num_of_goals += 1
            if not is_goal:
                first_goal_time = current_time
                is_goal = 1
            optimizer(m, node, optimizer_vars, optimizer_cons)
            m.update()
            converted_optimizer_vars = getOptimizerVars(m.getVars())
            max_time = max(r[1] for r in converted_optimizer_vars)
            if max_time < chosen_goal_time:
                chosen_goal_time = max_time
                return_val.valid = 1
                return_val.gaol_node = deepcopy(node)
                return_val.chosen_var_list = deepcopy(converted_optimizer_vars)
                return_val.chosen_con_list = deepcopy(list(set(optimizer_cons)))
                for i in node.chosen_lanes:
                    return_val.chosen_lanes_list.append(i)
            continue

        childsArr = node.getChilds(planes)
        for i in childsArr:
            i[0].priority = -heuristic(i[0], 3, i[1])  # 3 is select the heuristic !
            entry_cnt += 1
            i[0].entry_cnt = entry_cnt
        for i in childsArr:
            if (i[0] not in open_Q.queue) and (i[0] not in close_Q.queue):
                open_Q.put(i[0])

    window.close()
    return return_val


class SearchReturnValue:
    def __init__(self):
        self.valid = 0
        self.gaol_node = []
        self.chosen_var_list = []
        self.chosen_con_list = []
        self.chosen_lanes_list = []
        self.is_cancel = 0
