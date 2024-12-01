
import numpy as np
from model import ChessNetwork


# training data
x_train = np.array([
    [
            [-2,-3,-4,-5,-6,-4,-3,-2],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1],
            [2,3,4,5,6,4,3,2]
        ]
    
    ],
    )




y_train = np.array([[1,6,1,4]])

# network

net = ChessNetwork()

#configure
net.configure(activation_function='tanh',loss_function='crossentropy')
print("start fitting")
# train
net.fit(x_train, y_train, epochs=10, learning_rate=0.05)

# test
print("testing")
out = net.predict(x_train)
print(out)