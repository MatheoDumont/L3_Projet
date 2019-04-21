# from keras.models import Model
# from keras.layers import Dense, Input
import numpy as np
import pickle


class NetworkGen:

    def __init__(self, n_input, n_output):
        self.n_neuron = 10
        self.type = 'float32'

        # Hidden Layer 1
        self.layer1 = np.random.uniform(-1, 1,
                                        (n_input, self.n_neuron)).astype(self.type)
        self.bias1 = np.random.uniform(-1, 1,
                                       (1, self.n_neuron)).astype(self.type)

        # Hidden Layer 2
        self.layer2 = np.random.uniform(-1, 1,
                                        (self.n_neuron, self.n_neuron)).astype(self.type)

        self.bias2 = np.random.uniform(-1, 1,
                                       (1, self.n_neuron)).astype(self.type)

        # Hidden Layer 3
        # self.layer3 = np.random.uniform(-1, 1,
        #                                 (self.n_neuron, self.n_neuron)).astype(self.type)

        # self.bias3 = np.random.uniform(-1, 1,
        #                                (1, self.n_neuron)).astype(self.type)
        # Prediction Layer
        self.predictions_layer = np.random.uniform(
            -1, 1, (self.n_neuron, n_output)).astype(self.type)

        self.predictions_layer_bias = np.random.uniform(
            -1, 1, (1, n_output)).astype(self.type)

    def get_weights(self):
        return np.array([self.layer1,
                         self.bias1,
                         self.layer2,
                         self.bias2,
                         # self.layer3,
                         # self.bias3,
                         self.predictions_layer,
                         self.predictions_layer_bias])

    def set_weights(self, weights):
        self.layer1 = weights[0]
        self.bias1 = weights[1]

        self.layer2 = weights[2]
        self.bias2 = weights[3]

        # self.layer3 = weights[4]
        # self.bias3 = weights[5]

        self.predictions_layer = weights[4]
        self.predictions_layer_bias = weights[5]

    def predict_on_batch(self, inputs):
        res1 = (inputs @ self.layer1) + self.bias1
        act1 = np.tanh(res1)

        res2 = (act1 @ self.layer2) + self.bias2
        act2 = np.tanh(res2)

        # res3 = (act2 @ self.layer3) + self.bias3
        # act3 = np.tanh(res3)

        res4 = (act2 @ self.predictions_layer) + self.predictions_layer_bias
        output = np.tanh(res4)

        return output

    def save_weights(self, namefile):
        """
        Documentation/aide utilisée pour pickle :
        https://stackoverflow.com/questions/35133317/numpy-save-some-arrays-at-once
        https://docs.python.org/3/library/pickle.html
        """
        with open(namefile, "wb") as workingfile:
            pickle.dump(self.get_weights(), workingfile, pickle.HIGHEST_PROTOCOL)

    def load_weights(self, namefile):
        with open(namefile, "rb") as workingfile:
            self.set_weights(pickle.load(workingfile))
