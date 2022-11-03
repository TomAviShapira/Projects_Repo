from Agent import build_agent
from BpEnv import BpEnv
from DNN import build_model
from datetime import datetime
import numpy as np

from GUI import plot_BP

if __name__ == '__main__':
    env = BpEnv(100)
    states = env.observation_space.shape
    actions = env.action_space.n

    model = build_model(states, actions)
    model.summary()
    # for layer in model.layers:
    #     weights = layer.get_weights()
    #     print(weights)

    dqn = build_agent(model, actions)

    load = True
    if load:
        dqn.load_weights(r'checkpoints/11_06_2022_13_39_52 - final/dqn_weights.h5f')

    fit = False
    if fit:
        dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)
        date_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        dqn.save_weights(r'checkpoints/%s/dqn_weights.h5f' % date_time, overwrite=True)

    test = False
    if test:
        scores = dqn.test(env, nb_episodes=1, visualize=False)
        print('Avg Reward: %f' % np.mean(scores.history['episode_reward']))

    plot = True
    if plot:
        plot_BP(env, dqn)
