class Stn:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.childs = []


def stnCreate(final_var_list: list, final_con_list: list):
    stn = []
    for i in final_var_list:
        stn.append(Stn(i[0]))

    stn_con_list = []
    for i in final_con_list:
        i = i.split()
        if len(i) > 3 and i[3] == ">=":
            stn_con_list.append(i)

    for i in stn_con_list:
        node1 = stnLookUp(stn, i[0])
        node2 = stnLookUp(stn, i[2])
        if (node1.name == "-1") or (node2.name == "-1"):
            print("stnCreate Error")
            exit(1)
        node1.parents.append(node2)
        node2.childs.append(node1)

    return stn


def stnLookUp(stn, name):
    for i in stn:
        if i.name == name:
            return i
    return Stn("-1")
