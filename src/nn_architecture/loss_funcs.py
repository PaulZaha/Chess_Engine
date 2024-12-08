import numpy as np

# loss function and its derivative
def mse(y_true, y_pred):
    return np.mean(np.power(y_true-y_pred, 2))

def mse_backprop(y_true, y_pred):
    return 2*(y_pred-y_true)/y_true.size

def cross_entropy(y_true, y_pred):
    epsilon = 1e-15  # kleine Zahl zur Vermeidung von log(0)
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)  # Verhindert, dass y_pred 0 oder 1 wird
    return -np.sum(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)) / y_true.shape[0]


def cross_entropy_backprop(y_true, y_pred):
    return (y_pred - y_true) / y_true.shape[0]