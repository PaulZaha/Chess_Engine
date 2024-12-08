import numpy as np
from layering.layer import Layer

class Normalize(Layer):
    def __init__(self):
        pass

    def forward_propagation(self, input_data):
        return input_data / 6

    def backward_propagation(self, output_error,learning_rate):
        return output_error
