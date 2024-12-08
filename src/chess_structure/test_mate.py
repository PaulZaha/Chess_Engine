from chessboard import ChessBoard
import numpy as np

def test_checkmate():
    env = ChessBoard()


    mate_position = np.array([
        [0, 0, 0, 0, 0, 0, 0, -6],  
        [0, 0, 0, 0, 0, 0, 0, 5], 
        [0, 0, 0, 0, 0, 0, 0, 6],  
        [0, 0, 0, 0, 0, 0, 0, 0],  
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],  
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0] 
    ])


    env.board = mate_position.copy()
    env.turn = -10  


    print("Aktuelles Brett:")
    print(env.board)
    actions = env.get_valid_actions()
    print(actions)

    if env.checkmate():
        print("Schachmatt erkannt!")
    else:
        print("Kein Schachmatt.")

test_checkmate()
