import time

import numpy as np
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense

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
        X = x.reshape(384, )
        positions = np.array(pos)
        X = np.concatenate((X, positions), axis=0)
        return X

    def predict(self, x, pos):
        input = self.convert_to_model_input(x, pos)
        input = np.array([input])
        sc = self.model.predict(input)[0][0]
        return sc

    def build_model(self, params=None):
        if params is None:
            params = config.PARAMS_DNN
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

    class DNN(Gen_model):
        def __init__(self, params=None):
            self.model = self.build_model(params)

        def fit(self, states, targets, epochs, verbose, validation_split, batch_size, shuffle):
            self.model.fit(states, targets, epochs=epochs, verbose=verbose, batch_size=batch_size, shuffle=shuffle,
                           validation_split=validation_split)

        def convert_to_model_input(self, x, pos):
            X = x.reshape(384, )
            positions = np.array(pos)
            X = np.concatenate((X, positions), axis=0)
            return X

        def predict(self, x, pos):
            input = self.convert_to_model_input(x, pos)
            input = np.array([input])
            sc = self.model.predict(input)[0][0]
            return sc

        def build_model(self, params=None):
            if params is None:
                params = config.PARAMS_DNN
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


class ResidualCNN(Gen_model):
    def __init__(self, params=None):
        self.model = self.build_model(params)

    def fit(self, states, targets, epochs, verbose, validation_split, batch_size, shuffle):
        self.model.fit(states, targets, epochs=epochs, verbose=verbose, batch_size=batch_size, shuffle=shuffle,
                       validation_split=validation_split)

    def convert_to_model_input(self, x, pos):
        x = np.array(tf.cast(x, tf.float32))
        pos = np.array(tf.cast(pos, tf.float32))
        X = x.reshape(48,8,1)
        return X, pos

    def predict(self, x, pos):
        input1, input2 = self.convert_to_model_input(x, pos)
        input1 = np.array([input1])
        input2 = np.array([input2])
        sc = self.model.predict([input1, input2])[0][0]
        return sc

    def build_model(self, params=None):
        if params is None:
            main_input = Input(shape=(48, 8, 1), name='main_input')

            x = Conv2D(384, (12, 3), padding='same', activation='relu')(main_input)
            x = Conv2D(384, (8, 2), padding='same', activation='relu',
                       kernel_regularizer=keras.regularizers.l2(l=0.0001))(x)
            x = MaxPooling2D((4, 1))(x)
            x = Dropout(0.1)(x)
            x = Conv2D(96, (3, 3), padding='same', activation='relu',
                       kernel_regularizer=keras.regularizers.l2(l=0.0001))(x)
            x = Dropout(0.1)(x)
            x = Flatten()(x)
            auxiliary_input = Input(shape=(2,), name='aux_input')
            x = Dense(300, activation='elu', kernel_regularizer=keras.regularizers.l2(l=0.0001))(x)
            x = Dropout(0.2)(x)
            x = Dense(400, activation='elu', kernel_regularizer=keras.regularizers.l2(l=0.0001))(x)
            x = Dropout(0.2)(x)
            x = Dense(200, activation='elu', kernel_regularizer=keras.regularizers.l2(l=0.0001))(x)
            main_output = Dense(1, activation='sigmoid', name='main_output')(x)
            model = Model(inputs=[main_input, auxiliary_input], outputs=[main_output])

            model.compile(optimizer='adam', loss='binary_crossentropy', metric=['mae'])
        else:
            pass
        return model
