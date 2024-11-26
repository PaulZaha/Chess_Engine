import numpy as np

class ChessBoard():
    """
    Board Notation:
        Empty: 0
        White Pawn: 1
        White Rook: 2
        White Knight: 3
        White Bishop: 4
        White Queen: 5
        White King: 6
        Black Pawn: -1
        Black Rook: -2
        Black Knight: -3
        Black Bishop: -4
        Black Queen: -5
        Black King: -6
        
    
    """

    #Initialize starting board
    board = np.array(
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
    move = ''

    def __init__(self):
        self.board = ChessBoard.board
        self.move = ChessBoard.move

    def get_current_board(self):
        return self.board

    def notation_to_index(self, move):
        """
        Converts chess notation like 'e2' to board indices.
        """
        start = move[:2]
        end = move[2:]

        startcolumn = ord(start[0].lower()) - ord('a')
        startrow = 8 - int(start[1])
        endcolumn = ord(end[0].lower()) - ord('a')
        endrow = 8 - int(end[1])
 
        return startrow, startcolumn, endrow, endcolumn

    def make_move(self,move):
        """
        Input to make a move.

        Args:
            move (str): Accepts str of length 4 with inputfield and outputfield concatenated together.
        """
        if len(move) != 4:
            print("Invalid move")
            return False
        startrow,startcol,endrow,endcol = self.notation_to_index(move)

        cur_piece = self.board[startrow,startcol]
        print(cur_piece)


    def make_pawn_move(self):
        self.board

def main():
    board = ChessBoard()
    board.make_move('a2a4')
    
    

if __name__ == '__main__':
    main()