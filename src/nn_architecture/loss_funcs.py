import numpy as np

# loss function and its derivative
def mse(y_true, y_pred):
    return np.mean(np.power(y_true-y_pred, 2))

def mse_backprop(y_true, y_pred):
    return 2*(y_pred-y_true)/y_true.size

def cross_entropy(y_true, y_pred):
    cross_entropy = -(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)).mean()

    return cross_entropy

def cross_entropy_backprop(y_true, y_pred):
    return (y_pred - y_true) / y_true.shape[0]