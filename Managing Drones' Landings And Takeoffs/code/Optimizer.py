from projectB_tom import Node
from gurobipy import GRB


def optimizer(m, node: Node, optimizer_vars, optimizer_cons):
    for i in range(0, len(node.constrains)):
        optimizer_cons.append(node.constrains[i])
        con = node.constrains[i].split()
        if len(con) == 3:
            ind1 = getVarListInd(optimizer_vars, con[0], m)
            if con[1] == ">=":
                m.addConstr(optimizer_vars[ind1][1] >= float(con[2]), str(node.entry_cnt) + str(i))
            else:
                m.addConstr(optimizer_vars[ind1][1] <= float(con[2]), str(node.entry_cnt) + str(i))
        else:
            ind1 = getVarListInd(optimizer_vars, con[0], m)
            ind2 = getVarListInd(optimizer_vars, con[2], m)
            if con[3] == ">=":
                m.addConstr(optimizer_vars[ind1][1] - optimizer_vars[ind2][1] >= float(con[4]),
                            str(node.entry_cnt) + str(i))
            else:
                m.addConstr(optimizer_vars[ind1][1] - optimizer_vars[ind2][1] <= float(con[4]),
                            str(node.entry_cnt) + str(i))
        m.setObjective(1.0 * optimizer_vars[ind1][1], GRB.MINIMIZE)
    m.update()
    m.optimize()
    return m.getAttr('SolCount')


def getVarListInd(var_list, var, m):
    if var in [i[0] for i in var_list]:
        ind = [i[0] for i in var_list].index(var)
    else:
        var_list.append([var, m.addVar(name=var)])
        ind = len(var_list) - 1
    return ind


def getOptimizerVars(m_vars):
    var_list = []
    for i in m_vars:
        var_list.append([i.VarName, i.X])
    return var_list
