import pandas as pd


def get_agent_actions_table():
    path = r'C:\Users\toms6.TOM.000\Desktop\technion\תואר שני\Semester B\Digital Medical ' \
           r'Electronics\project\PiRL-main\BP\agent_actions.xlsx'
    df = pd.read_excel(path)

    action_table = {-5: df[-5].tolist(),
                    -4: df[-4].tolist(),
                    -3: df[-3].tolist(),
                    -2: df[-2].tolist(),
                    -1: df[-1].tolist(),
                    0: df[0].tolist(),
                    1: df[1].tolist(),
                    2: df[2].tolist(),
                    3: df[3].tolist(),
                    4: df[4].tolist(),
                    5: df[5].tolist()}

    return action_table
