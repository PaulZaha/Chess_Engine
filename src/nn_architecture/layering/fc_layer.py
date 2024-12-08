from layering.layer import Layer
import numpy as np


class FCLayer(Layer):
    """inherits from base layer class

    Args:
        Layer (_type_): _description_
    """
    # np.random.seed(44)
    def __init__(self,input_size,output_size):
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2. / input_size)
        self.bias = np.zeros((1, output_size))

    
    def forward_propagation(self, input_data):
        self.input_data = input_data
        self.output = np.dot(self.input_data, self.weights) + self.bias
        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, output_error, learning_rate):
        batch_size = self.input_data.shape[0]
        

        weights_error = np.dot(self.input_data.reshape(-1,1), output_error) / batch_size  # Averaging over the batch size
        bias_error = np.sum(output_error, axis=0, keepdims=True) / batch_size

        input_error = np.dot(output_error, self.weights.T)

        # Update the weights and biases using the gradients
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * bias_error
        return input_error