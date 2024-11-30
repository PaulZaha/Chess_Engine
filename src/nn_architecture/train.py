
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
    ])


#tbd: zahlen skalieren auf 0-1
"""
Am Ende brauchen wir statt einer Activation Function einen Classifier.
Nach dem Input des Board müssen aus der chessenvironment alle möglichen Züge berechnet werden.
Dann soll eine Map zwischen dem Input-Board und allen legalen Moves erstellt werden -> get best moves :)
Dieser soll für jeden möglichen Schachzug einen Wert zwischen 0 und 1 ausgeben
"""

y_train = np.array([0])

# network

net = ChessNetwork()

#configure
net.configure(activation_function='tanh',loss_function='mse')
print("start fitting")
# train
net.fit(x_train, y_train, epochs=10, learning_rate=0.1)

# test
out = net.predict(x_train)
print(out)