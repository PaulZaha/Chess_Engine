
from layering.fc_layer import FCLayer
from layering.activation import ActivationLayer
from layering.flatten import Flatten
from activation_funcs import *
from loss_funcs import *



class ChessNetwork():
    """The Chessnetwork itself

    Args:
        Network (_type_): _description_
    """
    def __init__(self):
        self.layers = []
        self.loss_func = None
        self.loss_backprop = None
        self.activation_func = None
        self.activation_backprop = None

        

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)


    # predict output for given input
    def predict(self, input_data):
        # sample dimension first
        samples = len(input_data)
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)

        return result

    # train the network
    def fit(self, x_train, y_train, epochs, learning_rate,batch_size=1):
        # sample dimension first
        samples = len(x_train)

        # training loop
        for i in range(epochs):
            err = 0
            for j in range(0,samples,batch_size):
                # forward propagation
                x_batch = x_train[j:j+batch_size]
                y_batch = y_train[j:j+batch_size]

                output = x_batch

                for layer in self.layers:
                    output = layer.forward_propagation(output)
                # compute loss (for display purpose only)
                err += self.loss_func(y_batch, output)

                # backward propagation
                error = self.loss_backprop(y_batch, output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            # calculate average error on all samples
            err /= samples
            print('epoch %d/%d   error=%f' % (i+1, epochs, err))
        
    def configure(self,activation_function,loss_function):
        """Set activation and loss function before training

        Args:
            activation_function (_type_): _description_
            loss_function (_type_): _description_
        """
        self.activation_func,self.activation_backprop = self.get_activation_function(activation_function=activation_function)
        self.loss_func,self.loss_backprop = self.get_loss_function(loss_function=loss_function)
        print(self.activation_func)

        self.__load_modules()
        
    def __load_modules(self):
        """Loading the modules after configuration. Private method, shouldn't be called from user.
        """
        self.add(Flatten())
        self.add(FCLayer(64, 8))
        self.add(ActivationLayer(activation_func=self.activation_func,activation_backprop=self.activation_backprop))
        self.add(FCLayer(8, 1))
        self.add(ActivationLayer(activation_func=self.activation_func,activation_backprop=self.activation_backprop))


    def get_activation_function(self,activation_function):
        """Load activation functions

        Args:
            activation_function (str): 

        Returns:
            activation_function (func): 
        """
        if activation_function == 'tanh':
            return tanh,tanh_backprop

    def get_loss_function(self,loss_function):
        if loss_function == 'mse':
            return mse,mse_backprop
