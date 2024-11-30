from layering.layer import Layer
import numpy as np


class Flatten(Layer):
    def __init__(self):
        pass

    def forward_propagation(self,input_data):
        self.input_shape = input_data.shape
        return input_data.flatten()
    
    def backward_propagation(self,output_error,learning_rate):
        return output_error.reshape(self.input_shape)