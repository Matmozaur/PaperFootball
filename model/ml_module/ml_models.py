from controller import config
from controller.loss import softmax_cross_entropy_with_logits

run_folder = './run/'
run_archive_folder = './run_archive/'

class DNN():
    def __init__(self, reg_const, learning_rate, input_dim, model = None):
        self.model = model
        self.reg_const = reg_const
        self.learning_rate = learning_rate
        self.input_dim = input_dim

    def predict(self, x, pos=None):
        return self.model.predict(x)

    def fit(self, states, targets, epochs, verbose, validation_split, batch_size):
        return self.model.fit(states, targets, epochs=epochs, verbose=verbose, validation_split=validation_split,
                              batch_size=batch_size, shuffle=False)

