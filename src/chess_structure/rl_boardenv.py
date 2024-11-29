from boardsetup import ChessBoard
from movevalidity import MoveValidity
import numpy as np

class ChessEnv(ChessBoard,MoveValidity):
    """
    prepping ChessBoard for reinforcement learning
    """

    def __init__(self):
        super().__init__() 
        self.done = False  #variable for game is done
        self.valid_actions = []

    def reset(self):
        """Starting state for board

        Returns:
            _type_: _description_
        """
        self.board = np.array(
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
        )
        self.done = False  
        return self.board  

    

    def step(self, move):
        """make setup

        Args:
            move (int): len 4 with startrow,col,endrow,col

        Returns:
            current board: 
            reward (-1,0,1)
            done: state if game is done
        """

        self.make_move(move=move)
        

        reward = 0
        self.done = False
        
        if self.is_king_in_check(1):
            print("check")

        if self.is_king_in_check(0):
            print("check")


        if self.check_win():
            reward = 1  
            self.done = True
        elif self.check_draw(): 
            reward = 0  
            self.done = True

        return self.board, reward, self.done

    def check_win(self):

        if self.is_king_in_check(1):
            print("check")
            if len(self.get_valid_actions()) == 0:
                return True 

        if self.is_king_in_check(-1):
            print("check")
            if len(self.get_valid_actions()) == 0:
                return True 

        return False  

    def is_king_in_check(self, player):

        king_position = self.find_king(player)
        if not king_position:
            return False  

        king_row, king_col = king_position


        for i in range(8):
            for j in range(8):
                piece = self.board[i, j]
                if piece != 0 and np.sign(piece) == -np.sign(player):
                    valid_moves = self.get_valid_moves_for_piece(i, j, piece)
                    if any([king_row, king_col] == move[2:4] for move in valid_moves):

                        return True 

        return False 

    def find_king(self, player):

        for row in range(8):
            for col in range(8):
                if (player == 1 and self.board[row, col] == 6) or (player == -1 and self.board[row, col] == -6):
                    return row, col
        return None






    def check_draw(self):
        #tbd
        if self.check_stalemate():
            return True
        if self.check_insufficient_material():
            return True
        if self.check_fifty_moves():
            return True
        if self.check_threefold_repetition():
            return True
        return False
    

    def check_stalemate(self):
        #tbd

        return False

    def check_insufficient_material(self):
        #tbd
        
        #currently: only kings left
        white_pieces = np.abs(self.board)
        black_pieces = np.abs(self.board)
        
        if np.sum(white_pieces) == 6 and np.sum(black_pieces) == -6:
            return True
        return False

    def check_fifty_moves(self):
        #tbd
        

        return False

    def check_threefold_repetition(self):
        #tbd

        return False

