from copy import deepcopy


class Node:
    num_of_lanes = -1
    num_of_planes = -1

    def __init__(self, parent, state, constrains, last_lane_list, last_airspace, sort_planes, chosen_lanes):
        self.parent = parent
        self.state = state  # [pl(0), ..., pl(n-1), airspace, lane_cnt]
        self.priority = 0
        self.entry_cnt = 0
        self.constrains = constrains
        self.last_lane_list = last_lane_list  # [is taken, plane id, last operation]
        self.last_airspace = last_airspace
        self.sort_planes = sort_planes
        self.chosen_lanes = chosen_lanes  # [pl(0)[take off lane, landing lane], ...,
                                            # pl(n-1)[take off lane, landing lane]]

    def __gt__(self, other):
        if self.priority == other.priority:
            return self.entry_cnt > other.entry_cnt
        else:
            return self.priority > other.priority

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.entry_cnt < other.entry_cnt
        else:
            return self.priority < other.priority

    def __eq__(self, other):
        return self.entry_cnt == other.entry_cnt

    def sctto(self, plane_id, planes):  # state = 1
        if plane_id == 0:
            A = 1
        self.state[plane_id] += 1
        length = len(self.state)
        self.state[length - 1] += 1
        self.constrains.append("t_sctto_" + str(plane_id) + " >= " + str((planes[plane_id]).sd_duration[0]))
        self.constrains.append("t_sctto_" + str(plane_id) + " <= " + str((planes[plane_id]).sd_duration[1]))
        for i in range(len(self.last_lane_list)):
            j = (i + self.last_lane_list[-1] + 1) % self.num_of_lanes
            if self.last_lane_list[j][0] == 0:
                if self.last_lane_list[j][1] != -1:
                    self.constrains.append("t_sctto_" + str(plane_id) + " - " + self.last_lane_list[j][2] +
                                           str(self.last_lane_list[j][1]) + " >= " + str(0.001))
                self.last_lane_list[j][0] = 1
                self.last_lane_list[j][1] = plane_id
                self.chosen_lanes[plane_id][0] = j
                self.last_lane_list[-1] = j
                break

    def ectto(self, plane_id, planes):  # state = 2
        self.state[plane_id] += 1
        self.constrains.append("t_ectto_" + str(plane_id) + " - " + "t_sctto_" + str(plane_id) + " >= " + str(10))
        self.constrains.append("t_ectto_" + str(plane_id) + " - " + "t_sctto_" + str(plane_id) + " <= " + str(10.01))

    def sto(self, plane_id, planes):  # state = 3
        self.state[plane_id] += 1
        length = len(self.state)
        self.state[length - 2] = 1
        self.constrains.append("t_sto_" + str(plane_id) + " - " + "t_ectto_" + str(plane_id) + " >= " + str(0.001))
        if self.last_airspace[0] != -1:
            self.constrains.append("t_sto_" + str(plane_id) + " - " + self.last_airspace[1] + str(self.last_airspace[0])
                                   + " >= " + str(0.001))

    def eto(self, plane_id, planes):  # state = 4
        self.state[plane_id] += 1
        length = len(self.state)
        self.state[length - 2] = 0
        length = len(self.state)
        self.constrains.append("t_eto_" + str(plane_id) + " - " + "t_sto_" + str(plane_id) + " >= " + str(10))
        self.constrains.append("t_eto_" + str(plane_id) + " - " + "t_sto_" + str(plane_id) + " <= " + str(10.01))
        for i in self.last_lane_list[:-1]:
            if i[0] == 1 and i[1] == plane_id:
                i[0] = 0
                i[2] = "t_eto_"
                break
        self.state[length - 1] -= 1
        self.last_airspace[0] = plane_id
        self.last_airspace[1] = "t_eto_"

    def sm(self, plane_id, planes):  # state = 5
        self.state[plane_id] += 1
        if planes[plane_id].init_state == 1:
            self.constrains.append("t_sm_" + str(plane_id) + " - " + "t_eto_" + str(plane_id) + " >= " + str(0.001))
            self.constrains.append("t_sm_" + str(plane_id) + " - " + "t_eto_" + str(plane_id) + " <= " + str(0.01))
        elif planes[plane_id].init_state == 5:
            self.constrains.append("t_sm_" + str(plane_id) + " >= " + str(0))
            self.constrains.append("t_sm_" + str(plane_id) + " <= " + str(0.001))

    def em(self, plane_id, planes):  # state = 6
        self.state[plane_id] += 1
        self.constrains.append("t_em_" + str(plane_id) + " - " + "t_sm_" + str(plane_id) + " >= " +
                               str((planes[plane_id]).m_duration[0]))

    def sl(self, plane_id, planes):  # state = 7
        self.state[plane_id] += 1
        length = len(self.state)
        self.state[length - 2] = 1
        length = len(self.state)
        self.state[length - 1] += 1
        self.constrains.append("t_sl_" + str(plane_id) + " - " + "t_em_" + str(plane_id) + " >= " + str(0.001))
        self.constrains.append("t_sl_" + str(plane_id) + " - " + "t_sm_" + str(plane_id) + " <= "
                               + str((planes[plane_id]).m_duration[1]))
        for i in range(len(self.last_lane_list)):
            j = (i + self.last_lane_list[-1] + 1) % self.num_of_lanes
            if self.last_lane_list[j][0] == 0:
                if self.last_lane_list[j][1] != -1:
                    self.constrains.append("t_sl_" + str(plane_id) + " - " + self.last_lane_list[j][2] +
                                           str(self.last_lane_list[j][1]) + " >= " + str(0.001))
                self.last_lane_list[j][0] = 1
                self.last_lane_list[j][1] = plane_id
                self.chosen_lanes[plane_id][1] = j
                self.last_lane_list[-1] = j
                break
        if self.last_airspace[0] != -1:
            self.constrains.append("t_sl_" + str(plane_id) + " - " + self.last_airspace[1] + str(self.last_airspace[0])
                                   + " >= " + str(0.001))

    def el(self, plane_id, planes):  # state = 8
        self.state[plane_id] += 1
        length = len(self.state)
        self.state[length - 2] = 0
        self.constrains.append("t_el_" + str(plane_id) + " - " + "t_sl_" + str(plane_id) + " >= " + str(10))
        self.constrains.append("t_el_" + str(plane_id) + " - " + "t_sl_" + str(plane_id) + " <= " + str(10.01))
        self.last_airspace[0] = plane_id
        self.last_airspace[1] = "t_el_"

    def st(self, plane_id, planes):  # state = 9
        self.state[plane_id] += 1
        self.constrains.append("t_st_" + str(plane_id) + " - " + "t_el_" + str(plane_id) + " >= " + str(0.001))
        self.constrains.append("t_st_" + str(plane_id) + " - " + "t_el_" + str(plane_id) + " <= " + str(0.01))

    def et(self, plane_id, planes):  # state = 10
        self.state[plane_id] += 1
        length = len(self.state)
        self.constrains.append("t_et_" + str(plane_id) + " - " + "t_st_" + str(plane_id) + " >= " + str(10))
        self.constrains.append("t_et_" + str(plane_id) + " - " + "t_st_" + str(plane_id) + " <= " + str(10.01))
        if planes[plane_id].init_state == 1:
            self.constrains.append("t_et_" + str(plane_id) + " <= " + str(planes[plane_id].day_duration))
        for i in self.last_lane_list[:-1]:
            if i[0] == 1 and i[1] == plane_id:
                i[0] = 0
                i[2] = "t_et_"
                break
        self.state[length - 1] -= 1

    def getChilds(self, planes):
        childsArr = []
        nextActionArr = self.getNextActionArr()
        for plane_id in range(0, len(nextActionArr)):
            if nextActionArr[plane_id][1]:
                child = Node(self, deepcopy(self.state), [],  # deepcopy(self.constrains),
                             deepcopy(self.last_lane_list), deepcopy(self.last_airspace)
                             , deepcopy(self.sort_planes), deepcopy(self.chosen_lanes))
                getattr(child, nextActionArr[plane_id][0])(plane_id, planes)
                childsArr.append((child, plane_id))
        return childsArr

    def getNextActionArr(self):
        nextActionArr = []
        for i in range(0, len(self.state) - 2):
            nextActionArr.append([self.getNextAction(self.state[i]), 1])
        self.filterNextAction(nextActionArr)
        return nextActionArr

    @staticmethod
    def getNextAction(argument):
        switcher = {
            1: "sctto",
            2: "ectto",
            3: "sto",
            4: "eto",
            5: "sm",
            6: "em",
            7: "sl",
            8: "el",
            9: "st",
            10: "et",
            11: "done",
        }
        return switcher.get(argument, "nothing")

    def filterNextAction(self, nextActionArr):
        length = len(self.state)
        for i in range(0, len(nextActionArr)):
            if self.state[length - 2] == 1:
                if (nextActionArr[i][0] == 'sto') or (nextActionArr[i][0] == 'sl'):
                    nextActionArr[i][1] = 0
            if self.state[length - 1] == self.num_of_lanes:
                if (nextActionArr[i][0] == 'sctto') or (nextActionArr[i][0] == 'sl'):
                    nextActionArr[i][1] = 0
            if nextActionArr[i][0] == 'done':
                nextActionArr[i][1] = 0
        return nextActionArr

    def isGoal(self):
        goal = []
        for i in range(0, self.num_of_planes):
            goal.append(11)
        if self.state[0:self.num_of_planes] == goal:
            return True
        else:
            return False

    def printNode(self):
        length = len(self.state)
        print("state: " + str(self.state[0:length - 2]) + " : " + str(self.state[length - 2:length]))
