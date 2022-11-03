import timeit
from termcolor import colored

from projectB_tom.Node import Node
from projectB_tom.Search import search
from projectB_tom.Stn import stnCreate, stnLookUp


def exec_(num_of_planes, num_of_lanes, planes, state, chosen_lanes, is_gui, config_name, log_output,
          is_print_full_solution, max_run_time, sort_planes, predicted_sort_planes):
    if len(planes) != num_of_planes:
        print("Error: number of planes should match", file=log_output)
        exit(0)
    if num_of_lanes <= 0:
        print("Error: number of lanes should be > 0", file=log_output)
        exit(0)

    lane_cnt = 0
    airspace = 0
    state.append(airspace)
    state.append(lane_cnt)
    last_lane_list = []
    for i in range(num_of_lanes):
        last_lane_list.append([0, -1, "none"])  # [is taken, plane id, last operation]
    last_lane_list.append(0)

    chosen_var_list = []
    chosen_con_list = []
    first_start_time = timeit.default_timer()

    all_chosen_var_list = []
    all_chosen_con_list = []
    all_chosen_lane_list = []
    output_list = []
    is_solution_found = 0
    # reset
    for j in range(len(planes)):
        state[j] = planes[j].init_state
    state[-1] = 0
    state[-2] = 0
    for j in range(len(last_lane_list)):
        last_lane_list[j] = [0, -1, "none"]
    last_lane_list[-1] = 0
    for j in range(len(chosen_lanes)):
        chosen_lanes[j] = [-1, -1]
    chosen_var_list.clear()
    chosen_con_list.clear()

    init = Node(None, state, [], last_lane_list, [-1, "none"], predicted_sort_planes, chosen_lanes)
    Node.num_of_lanes = num_of_lanes
    Node.num_of_planes = num_of_planes

    start_time = timeit.default_timer()
    search_return_val = search(init, planes, start_time, is_gui, float(max_run_time))
    if not is_gui:
        print("\n\n=====================================================================", file=log_output)
        print('                            ', colored(config_name, attrs=['bold']), file=log_output)
        print("=====================================================================", file=log_output)
    if search_return_val.valid:  # solution found
        print("solution found :)", file=log_output)
        max_time = max(r[1] for r in search_return_val.chosen_var_list)
        print("max time: ", max_time, file=log_output)
        all_chosen_var_list.append([search_return_val.chosen_var_list, max_time])
        all_chosen_con_list.append([search_return_val.chosen_con_list, max_time])
        all_chosen_lane_list.append([search_return_val.chosen_lanes_list, max_time])
    else:
        print("can't find solution :(", file=log_output)
    if not is_gui:
        print("exec order (as we target): ", file=log_output)
        print([str(r[0]) + "_" + str(r[2]) for r in sort_planes], file=log_output)
    if len(all_chosen_var_list) > 0:
        is_solution_found = 1
        final_sol_ind = [r[1] for r in all_chosen_var_list].index(min(r[1] for r in all_chosen_var_list))
        final_var_list = all_chosen_var_list[final_sol_ind][0]
        final_con_list = all_chosen_con_list[final_sol_ind][0]
        final_lane_list = all_chosen_lane_list[final_sol_ind][0]

        stn = stnCreate(final_var_list, final_con_list)
        max_parent_num = max([len(k) for k in [r.parents for r in stn]])  # for a nice print
        max_childs_num = max([len(k) for k in [r.childs for r in stn]])  # for a nice print

        final_var_list = sorted(final_var_list, key=lambda x: x[1])
        exec_order = get_exec_order(final_var_list)
        print("exec order (by the algorithm): ", file=log_output)
        print([str(r[0]) + "_" + str(r[1]) for r in exec_order], file=log_output)
        print("=====================================================================", file=log_output)
        if is_print_full_solution:
            print("=====================================================================", file=log_output)
            print("final solution: ", file=log_output)
            print("=====================================================================", file=log_output)
            for i in range(len(final_lane_list)):
                print("plane", i, ":  [take off lane id, landing lane id] = ",
                      final_lane_list[i], file=log_output)
            print("=====================================================================", file=log_output)
            for i in final_var_list:
                tmp_node = stnLookUp(stn, i[0])
                print(i[0].ljust(9), ": ", str(round(i[1], 10)).ljust(10),
                      ":        parents: ", str([r.name for r in tmp_node.parents]).ljust(10 * max_parent_num + 2),
                      ":        childs: ", str([r.name for r in tmp_node.childs]).ljust(10 * max_childs_num + 2),
                      file=log_output)
            print("=====================================================================", file=log_output)
            print(*final_con_list, sep="\n", file=log_output)
            print("=====================================================================", file=log_output)
        output_list = prepareOutputToGui(final_var_list, final_lane_list)
    else:
        print("=====================================================================", file=log_output)
    if is_print_full_solution:
        print("=====================================================================", file=log_output)
        print("total run time: ", timeit.default_timer() - first_start_time, file=log_output)
        print("=====================================================================", file=log_output)

    return [is_solution_found, output_list]


def getActionCode(argument):
    switcher = {
        "sd": 0,
        "sctto": 1,
        "ectto": 2,
        "sto": 3,
        "eto": 4,
        "sm": 5,
        "em": 6,
        "sl": 7,
        "el": 8,
        "st": 9,
        "et": 10,
        "done": 11,
    }
    return switcher.get(argument, "nothing")


def get_exec_order(final_var_list):
    exec_order = []
    exec_order_t = [x[0] for x in final_var_list if x[0][2:5] in ['sto', 'sl_']]
    for i in exec_order_t:
        if i[2:5] == 'sto':
            exec_order.append([i[-1], 'to'])
        else:
            exec_order.append([i[-1], 'l'])
    return exec_order


def prepareOutputToGui(final_var_list, final_lane_list):
    tmp_output_list = []
    output_list = []
    for i in final_var_list:
        tmp_output_list.append([i[0].split('_'), i[1]])
    tmp_output_list = sorted(tmp_output_list, key=lambda x: x[0][2])

    for i in range(len(tmp_output_list)):
        if tmp_output_list[i][0][1] == "sctto":
            output_list.append(["Aligning",
                                tmp_output_list[i][0][2],
                                final_lane_list[int(tmp_output_list[i][0][2])][0],
                                round(tmp_output_list[i][1]),
                                round(tmp_output_list[i + 1][1] - tmp_output_list[i][1])])
        elif tmp_output_list[i][0][1] == "sto":
            output_list.append(["Take Off",
                                tmp_output_list[i][0][2],
                                final_lane_list[int(tmp_output_list[i][0][2])][0],
                                round(tmp_output_list[i][1]),
                                round(tmp_output_list[i + 1][1] - tmp_output_list[i][1])])
        elif tmp_output_list[i][0][1] == "sm":
            output_list.append(["Mission",
                                tmp_output_list[i][0][2],
                                '',
                                round(tmp_output_list[i][1]),
                                round(tmp_output_list[i + 1][1] - tmp_output_list[i][1])])
        elif tmp_output_list[i][0][1] == "sl":
            output_list.append(["Landing",
                                tmp_output_list[i][0][2],
                                final_lane_list[int(tmp_output_list[i][0][2])][1],
                                round(tmp_output_list[i][1]),
                                round(tmp_output_list[i + 1][1] - tmp_output_list[i][1])])
        elif tmp_output_list[i][0][1] == "st":
            output_list.append(["Evacuation",
                                tmp_output_list[i][0][2],
                                final_lane_list[int(tmp_output_list[i][0][2])][1],
                                round(tmp_output_list[i][1]),
                                round(tmp_output_list[i + 1][1] - tmp_output_list[i][1])])

    output_list = sorted(output_list, key=lambda x: x[3])
    return output_list
