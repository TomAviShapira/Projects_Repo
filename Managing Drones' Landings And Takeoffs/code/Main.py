from projectB_tom.Config import fromConfigFile
from projectB_tom.Gcn import Net
from projectB_tom.Gui import fromGui


def main():

    is_config = 1

    # relevant only if is_config = 1
    gcn_mode = 0  # 0 - run exec_   ,   1 - training

    if is_config:
        fromConfigFile(gcn_mode)
    else:
        fromGui()


if __name__ == "__main__":
    main()
