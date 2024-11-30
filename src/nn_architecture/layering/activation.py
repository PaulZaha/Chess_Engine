from layering.layer import Layer

# inherit from base class Layer
class ActivationLayer(Layer):
    def __init__(self, activation_func,activation_backprop):
        self.activation_func = activation_func
        self.activation_backprop = activation_backprop

    # returns the activated input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation_func(self.input)
        return self.output

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward_propagation(self, output_error, learning_rate):
        #Todo implement learning rate
        return self.activation_backprop(self.input) * output_error