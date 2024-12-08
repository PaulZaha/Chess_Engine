import numpy as np
from model import ChessNetwork
import os
import pandas as pd
import re
from ..chess_structure.create_dataset import create_game

net = ChessNetwork()
moves = []
boards = []

def train():

    # training data (wir nehmen an, dass load_data() hier korrekt aufgerufen wurde)
    x_train = np.array(boards)  # Diese Liste enthält alle Boards (8x8-Arrays)
    y_train = np.array(moves)   # Diese Liste enthält alle Moves (4er-Listen)

    # network
    net.configure(activation_function='relu', loss_function='mse')
    print("start fitting")
    # train
    net.fit(x_train, y_train, epochs=100, learning_rate=0.005)

def predict():
    # test (hier simulieren wir eine Eingabe für das Modell)
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

    # test
    print("testing")
    out = net.predict(x_train)
    print(out)

def load_data():
    curpath = os.path.dirname(__file__)
    logfile = os.path.relpath('../chess_structure/moves.csv', curpath)

    df = pd.read_csv(logfile)

    for index, row in df[1:].iterrows():
        # Extrahiere den Zug
        row = row[0]
        move = [int(row[1]) + 1, int(row[4]) + 1, int(row[7]) + 1, int(row[10]) + 1]
        moves.append(move)

        # Extrahiere das Schachbrett
        nums = re.findall(r'\d+', row[13:])
        nums_int = [int(zahl) for zahl in nums]
        board = np.array(nums_int).reshape(8, 8)  # Umwandlung in ein 8x8-Board
        boards.append(board)

    # Um sicherzustellen, dass wir die richtigen Dimensionen haben
    print(f"Boards shape: {np.array(boards).shape}")
    print(f"Moves shape: {np.array(moves).shape}")

def main():
    create_game()
    load_data()  # Wir laden zuerst die Daten
    train()      # Dann trainieren wir das Modell
    predict()    # Und schließlich testen wir das Modell

if __name__ == '__main__':
    main()
