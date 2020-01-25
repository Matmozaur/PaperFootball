import time

import numpy as np

from controller import config
import tensorflow.keras as keras
import tensorflow as tf

run_folder = './run/'
run_archive_folder = './run_archive/'


class Gen_model():

    def predict(self, x, pos=None):
        pass

    def fit(self, states, targets, epochs, verbose, validation_split, batch_size, shuffle):
        pass

    def convert_to_model_input(self, x, pos):
        pass

    def predict(self, input):
        pass

    def build_model(self):
        pass


class DNN(Gen_model):
    def __init__(self, params=None):
        self.model = self.build_model(params)

    def fit(self, states, targets, epochs, verbose, validation_split, batch_size, shuffle):
        self.model.fit(states, targets, epochs=epochs, verbose=verbose, batch_size=batch_size, shuffle=shuffle,
                       validation_split=validation_split)

    def convert_to_model_input(self, x, pos):
        X = x.reshape(384,)
        positions = np.array(pos)
        X = np.concatenate((X, positions), axis=0)
        return X

    def predict(self, x, pos):
        input = self.convert_to_model_input(x, pos)
        input = np.array([input])
        return self.model.predict(input)[0][0]

    def build_model(self, params=None):
        if params is None:
            params = {
                'activation_hidden': 'sigmoid', 'activation': 'sigmoid', 'optimizer': 'adam',
                'architectures': [[100, 0.0], [400, 0.000001], ['dropout', 0.1], [200, 0.000001], ['dropout', 0.2],
                                  [200, 0.000001],
                                  ['dropout', 0.3], [100, 0.0], [20, 0.0]]}
        model = keras.Sequential()
        for layer in params['architectures']:
            if layer[0] == 'dropout':
                model.add(keras.layers.Dropout(layer[1]))
            else:
                model.add(keras.layers.Dense(layer[0], activation=params['activation_hidden'],
                                             kernel_regularizer=keras.regularizers.l2(l=layer[1])))
        model.add(keras.layers.Dense(1, activation=params['activation']))
        model.compile(optimizer=params['optimizer'], loss='binary_crossentropy', metrics=['mae'])
        return model

