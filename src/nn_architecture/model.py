
from layering.fc_layer import FCLayer
from layering.activation import ActivationLayer
from layering.flatten import Flatten
from layering.normalize import Normalize
from activation_funcs import *
from loss_funcs import *



class ChessNetwork():
    """The Chessnetwork itself

    Args:
        Network (_type_): _description_
    """
    def __init__(self):
        self.layers = []
        self.loss_funcs = []
        self.loss_backprops = []
        self.activation_funcs = []
        self.activation_backprops = []

        

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)


    # predict output for given input
    def predict(self, input_data):
        samples = len(input_data)
        result = []

        for i in range(samples):
            output = input_data[i]
            
            # Vorwärtsdurchlauf
            for layer in self.layers:
                output = layer.forward_propagation(output)
            
            # Skaliere zurück auf den Bereich [1, 7]
            result.append(output * 6 + 1)
        
        return np.rint(np.array(result))


    def normalize_y(self,data):
        """Normalize data from 0-7 input to 0-1 array

        Args:
            data (_type_): _description_

        Returns:
            _type_: _description_
        """
        return (data-1) / 6

    # train the network
    def fit(self, x_train, y_train, epochs, learning_rate, batch_size=1):
        samples = len(x_train)
        y_train = self.normalize_y(y_train)  # Normalisierung der Zielwerte
        for epoch in range(epochs):
            err = 0
            for j in range(0, samples, batch_size):
                x_batch = x_train[j:j+batch_size]
                y_batch = y_train[j:j+batch_size]

                # Forward propagation
                output = x_batch
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # Compute loss
                err += self.loss_funcs[0](y_batch, output)

                # Backward propagation
                error = self.loss_backprops[0](y_batch, output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            # Durchschnittlichen Fehler berechnen
            err /= samples
            print(f'Epoch {epoch+1}/{epochs}   Error={err}')

        
    def configure(self, activation_function, loss_function):
        """Set activation and loss function before training."""
        act_func, act_backprop = self.get_activation_function(activation_function)
        loss_func, loss_backprop = self.get_loss_function(loss_function)
        
        self.activation_funcs = [act_func] * 100
        self.activation_backprops = [act_backprop] * 100
        self.loss_funcs = [loss_func] * 100
        self.loss_backprops = [loss_backprop] * 100

        self.__load_modules()
        
    def __load_modules(self):
        """Loading the modules after configuration."""
        self.add(Normalize())  # Normiere Eingabedaten
        self.add(Flatten())  # Flatten der Eingabedaten

        # Fully Connected Layers
        self.add(FCLayer(input_size=64, output_size=128))
        self.add(ActivationLayer(activation_func=self.activation_funcs[0], activation_backprop=self.activation_backprops[0]))

        self.add(FCLayer(input_size=128, output_size=128))
        self.add(ActivationLayer(activation_func=self.activation_funcs[1], activation_backprop=self.activation_backprops[1]))

        self.add(FCLayer(input_size=128, output_size=128))
        self.add(ActivationLayer(activation_func=self.activation_funcs[1], activation_backprop=self.activation_backprops[1]))

        
        


        # Ausgabe für die kontinuierlichen Werte: 4 Werte für die Koordinaten (Start, Ziel)
        self.add(FCLayer(input_size=128, output_size=4))  # 4 Ausgabeschichten
        self.add(ActivationLayer(activation_func=relu, activation_backprop=relu_backprop))  # Keine Aktivierung (lineare Ausgabe)


    def get_activation_function(self,activation_function):
        """Load activation functions

        Args:
            activation_function (str): 

        Returns:
            activation_function (func): 
        """
        if activation_function == 'tanh':
            return tanh,tanh_backprop
        elif activation_function == 'softmax':
            return softmax,softmax_backprop
        elif activation_function == 'relu':
            return relu, relu_backprop

    def get_loss_function(self,loss_function):
        if loss_function == 'mse':
            return mse,mse_backprop
        elif loss_function == 'crossentropy':
            return cross_entropy,cross_entropy_backprop
