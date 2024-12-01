import numpy as np

# activation function and its derivative
def tanh(x):
    return np.tanh(x)

def tanh_backprop(x):
    return 1-np.tanh(x)**2

def softmax(x):
    exps = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exps / np.sum(exps, axis=1, keepdims=True)


def softmax_backprop(x):
    # Implementieren Sie die Rückpropagation für Softmax, falls erforderlich
    return x  # Placeholder

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_backprop(x):
    return sigmoid(x) * (1-x)