import numpy as np


class NetworkGen:

    def __init__(self, n_input, n_output):
        self.n_neuron = 10
        self.type = 'float32'

        # Hidden Layer 1
        self.layer1 = np.random.uniform(-1, 1, (n_input, self.n_neuron)).astype(self.type)
        self.bias1 = np.random.uniform(-1, 1, (1, self.n_neuron)).astype(self.type)


        # Hidden Layer 2
        self.layer2 = np.random.uniform(-1, 1, (self.n_neuron, self.n_neuron)).astype(self.type)

        self.bias2 = np.random.uniform(-1, 1, (1, self.n_neuron)).astype(self.type)


        # Prediction Layer
        self.predictions_layer = np.random.uniform(
            -1, 1, (self.n_neuron, n_output)).astype(self.type)

        self.predictions_layer_bias = np.random.uniform(-1, 1, (1, n_output)).astype(self.type)


    def get_weights(self):
        return np.array([self.layer1, self.bias1, self.layer2, self.bias2,
                         self.predictions_layer, self.predictions_layer_bias])

    def set_weights(self, weights):
        pass

    def predict_on_batch(self, inputs):
        res1 = (inputs @ self.layer1) + self.bias1
        act1 = np.tanh(res1)

        res2 = (act1 @ self.layer2) + self.bias2
        act2 = np.tanh(res2)

        res3 = (act2 @ self.predictions_layer) + self.predictions_layer_bias
        output = np.tanh(res3)

        return output

    def save(self):
        pass

    def load(self):
        pass
