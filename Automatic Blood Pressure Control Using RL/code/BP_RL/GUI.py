import random
from threading import Thread
import matplotlib.pyplot as plt
import queue
import numpy as np


def plot_BP(env, dqn):
    state = env.reset()
    state_list = [0]
    x = np.linspace(0, 200, 201)
    y = np.zeros(201)

    t_drug_1 = {}

    q = queue.Queue()

    thread2 = Thread(target=get_input, args=(q,))
    thread2.setDaemon(True)
    thread2.start()
    plt.figure(1)
    is_noise = 0
    noise_time = 12
    PID = True
    while True:
        plt.clf()
        x_ticks = [i for i in range(200) if i % 24 == 0]
        plt.xticks(x_ticks)
        plt.xticks(color='black')
        if PID:
            plt.title('PID Controller, Error: %.2f' % state)
        else:
            plt.title('DQN Agent, Error: %.2f' % state)
        plt.grid()

        BP = env.get_BP()
        t = env.get_time()

        if t % 201 == 0:
            x = np.linspace(0, 200, 201)
            y = np.zeros(201)
            t_drug_1 = {}

        if is_noise:
            if t % noise_time == 0:
                n = random.randint(-5, 5)
                BP += n
                state -= n
            else:
                n = random.randint(-1, 1)
                BP += n
                state -= n

        if not q.empty():
            input_ = q.get()
            if input_ == 0:
                is_noise = 1 - is_noise
            elif input_ == 1:
                if PID:
                    PID = False
                else:
                    PID = True
                    state_list = [0]
            elif input_ == 2:
                if noise_time == 12:
                    noise_time = 1
                else:
                    noise_time = 12
            else:
                env.set_ref_BP(input_)
                state_list = [0]

        y[t % 201] = BP

        plt.plot(x, (env.ref_BP - 3) * np.ones(201), 'r--', color='green', linewidth=1.0)
        plt.plot(x, env.ref_BP * np.ones(201), 'r--', color='green', linewidth=1.0)
        plt.plot(x, (env.ref_BP + 3) * np.ones(201), 'r--', color='green', linewidth=1.0)

        plt.plot(x, y, color='black', linewidth=1.0)
        for i in t_drug_1:
            plt.scatter(i % 201, t_drug_1.get(i), color='red', s=10)

        plt.ylim([85, 110])
        plt.xlim([0, 192])

        plt.ylabel('BP [mmHg]')
        plt.xlabel('Time [hour]')

        plt.show(block=False)
        plt.pause(0.001)

        state_list.append(state)

        if PID:
            P = state_list[-1]
            I = sum(state_list)
            D = state_list[-2] - state_list[-1]
            if 0.6934053 * 2 * P + 0.01117102 * I + 0.78402317 * D > 0.08048041:
                action = 0
            else:
                action = 1
        else:
            action = dqn.forward(state)

        if action == 1:
            t_drug_1[t] = BP

        state, _, _, _ = env.step(action)


def get_input(q):
    while True:
        print("insert new ref BP: ", end='')
        input_ = input()
        try:
            input_ = int(input_)
            q.put(int(input_))
        except ValueError as e:
            print(e)
