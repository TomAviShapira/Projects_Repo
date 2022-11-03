from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
import math


class BpEnv(Env):
    def __init__(self, ref_BP):
        # Actions we can take
        self.action_space = Discrete(2)

        # Blood pressure array
        self.observation_space = Box(low=np.array([np.float32(-50.0)]), high=np.array([np.float32(50.0)]))

        # Set reference blood pressure
        self.ref_BP = ref_BP

        # Set start blood pressure
        self.rnd = 0  # random.randint(-5, 5)
        self.SBP = 140 + self.rnd
        self.DBP = 90 + self.rnd
        self.BP = self.DBP + (self.SBP - self.DBP) / 3
        self.state = self.ref_BP - self.BP
        self.pre_state = self.state

        # Set treatment length
        self.treatment_length = 192  # hours

        # Set time that has passed since the beginning of the treatment
        self.time = 0  # hours

        # set the drug vars
        self.Ka = 0.8
        self.Ke = 0.693 / 50
        self.Vd = 1498 * 10**3  # [l] -> [ml]
        self.F = 1
        self.dose_1 = 1 * 10**6  # [mg] -> [ng]
        self.dose_1_times = []
        self.Ke_values = []

    def step(self, action):

        # if self.time % 5 == 0 and self.time > 0:
        #     self.Ke = 0.693 / random.randint(40, 60)

        total_Ce_A_1 = 0
        for (dose_time, Ke) in zip(self.dose_1_times, self.Ke_values):
            total_Ce_A_1 += self.calc_Ce_A_init(Ke) * (math.exp(-self.Ke * (self.time - dose_time)) -
                                                       math.exp(-self.Ka * (self.time - dose_time)))

        total_Ce_A = total_Ce_A_1

        if action == 1:
            self.dose_1_times.append(self.time)
            self.Ke_values.append(self.Ke)

        SBP_PD_Ce_A = 0.164 * total_Ce_A / (total_Ce_A + 8.27)
        DBP_PD_Ce_A = 0.164 * total_Ce_A / (total_Ce_A + 2.97)

        new_SBP = self.SBP * (1 - SBP_PD_Ce_A)
        new_DBP = self.DBP * (1 - DBP_PD_Ce_A)

        self.BP = new_DBP + (new_SBP - new_DBP) / 3

        # Apply BP noise
        # self.BP += random.randint(-1, 1)

        self.state = self.ref_BP - self.BP

        # Calculate reward
        if abs(self.state) <= 3:
            reward = 100
        elif abs(self.state) < abs(self.pre_state):
            reward = 50
        elif self.state * self.pre_state < 0:
            reward = 20
        else:
            reward = -20

        # print(action, round(self.state, 2), round(self.BP, 2), reward, round(total_Ce_A, 2))

        # Check if treatment is done.
        if self.treatment_length <= 0:
            done = True
        else:
            done = False

        self.pre_state = self.state
        self.time += 1
        self.treatment_length -= 1

        # Set placeholder for info
        info = {}

        # Return step information
        return self.state, reward, done, info

    def render(self, mode="human"):
        pass

    def reset(self, seed=None, return_info=False, options=None):
        # Reset BP
        self.rnd = 0  # random.randint(-5, 5)
        self.SBP = 140 + self.rnd
        self.DBP = 90 + self.rnd
        self.BP = self.DBP + (self.SBP - self.DBP) / 3
        self.state = self.ref_BP - self.BP
        self.pre_state = self.state

        # reset treatment length
        self.treatment_length = 192  # hours

        # reset time that has passed since the beginning of the treatment
        self.time = 0  # hours

        # reset the drug vars
        self.dose_1_times = []
        self.Ke_values = []

        return self.state

    def get_BP(self):
        return self.BP

    def set_ref_BP(self, new_ref_BP):
        self.ref_BP = new_ref_BP

    def get_time(self):
        return self.time

    def calc_Ce_A_init(self, Ke):
        return (self.F * self.dose_1 * self.Ka) / (self.Vd * (self.Ka - Ke))
