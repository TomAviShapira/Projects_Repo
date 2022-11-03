from projectB_tom import Node
import math
from copy import deepcopy


def heuristic(node: Node, sel, plane_id):
    if sel == 0:  # bfs
        return 0
    elif sel == 1:  # exec by order, not parallel
        state = node.state[0:len(node.state) - 2]
        # state = [state[0], state[1]]  # order of exec
        cnt = 0
        for i in range(0, len(state)):
            if state[i] == 11:
                cnt += 1
        if cnt == len(state):
            return math.inf
        else:
            return cnt * 11 + state[cnt]
    elif sel == 2:  # exec parallel
        state = node.state[0:len(node.state) - 2]
        diff = 0
        for i in state:
            for j in state:
                if i != j:
                    diff += (abs(i - j))
        if diff == 0:
            return math.inf
        else:
            sum_t = 0
            for i in state:
                sum_t += i
            return sum_t / diff
    elif sel == 3:
        state = node.state[0:len(node.state) - 2]
        if not node.sort_planes:
            return 0

        help_list = deepcopy([i[0] for i in node.sort_planes])
        help_list = unique(help_list)
        help_list.reverse()
        a = 0
        for i in range(0, len(node.state) - 2):
            a += state[i]
        ind = help_list.index(plane_id) + a
        if state[node.sort_planes[0][0]] == 5 and node.sort_planes[0][2] == 'to':
            node.sort_planes.pop(0)
        '''
        if state[node.sort_planes[0][0]] == 9 and node.sort_planes[0][2] == 'l':
            node.sort_planes[0][1] = math.inf
            node.sort_planes.sort(key=lambda x: x[1])
        '''
        if state[node.sort_planes[0][0]] == 11 and node.sort_planes[0][2] == 'l':
            node.sort_planes.pop(0)
        return ind


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
