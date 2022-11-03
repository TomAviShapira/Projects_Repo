from keras.layers import Convolution2D, Activation, Permute
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten


def build_model(nb_states, nb_actions):
    model = Sequential()
    model.add(Dense(128, input_shape=nb_states))
    model.add(Activation('relu'))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(32))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))

    return model
