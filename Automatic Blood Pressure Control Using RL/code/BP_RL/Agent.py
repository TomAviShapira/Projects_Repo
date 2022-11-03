from keras.callbacks import EarlyStopping
from rl.agents import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy, BoltzmannQPolicy
from rl.memory import SequentialMemory
from tensorflow.keras.optimizers import Adam


def build_agent(model, nb_actions):
    memory = SequentialMemory(limit=1000000, window_length=1)
    policy = EpsGreedyQPolicy(eps=0.2)
    nb_steps_warmup = 1000
    target_model_update = .2
    gamma = .99
    lr = .0001
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=nb_steps_warmup,
                   target_model_update=target_model_update, policy=policy, gamma=gamma)
    dqn.compile(Adam(learning_rate=lr), metrics=['mae'])

    return dqn
