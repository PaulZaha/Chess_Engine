import numpy as np
from movevalidity import MoveValidity

class ChessBoard(MoveValidity):
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
        super().__init__()
        self.board = ChessBoard.board
        self.move = ChessBoard.move

    def get_current_board(self):
        print(self.board)
        return self.board


    def make_move(self, move):
        """
        Input to make a move.

        Args:
            move (str): 
        """

        if len(move) != 4:
            return False
        
        startrow, startcol, endrow, endcol = int(move[0]), int(move[1]), int(move[2]), int(move[3])

        # Überprüfen, ob der Zug legal ist
        if not self.is_move_legal(startrow, startcol, endrow, endcol):
            print("illegal")
            return False
        
        # Speichere den aktuellen Zustand des Bretts und des Stücks
        cur_piece = self.board[startrow, startcol]
        self.board[endrow, endcol] = cur_piece
        self.board[startrow, startcol] = 0

        # Überprüfen, ob der König nach dem Zug im Schach ist
        if self.is_king_in_check(1 if cur_piece > 0 else -1):
            # Falls der König im Schach steht, mache den Zug rückgängig
            self.board[startrow, startcol] = cur_piece
            self.board[endrow, endcol] = 0
            return False

        # Prüfen auf Bauernpromotion
        if cur_piece == 1 and endrow == 0:
            self.board[endrow, endcol] = 5  # weißer Bauer wird zur Dame
        elif cur_piece == -1 and endrow == 7:
            self.board[endrow, endcol] = -5  # schwarzer Bauer wird zur Dame

        return True
    

    def is_king_in_check(self, player):
        # Finde den König des Spielers
        king_position = self.find_king(player)
        if not king_position:
            return False  # Kein König gefunden, keine Gefahr

        king_row, king_col = king_position

        # Finde alle möglichen Bedrohungen für den König
        for i in range(8):
            for j in range(8):
                piece = self.board[i, j]
                if piece != 0 and np.sign(piece) == -np.sign(player):  # Ein gegnerisches Stück
                    valid_moves = self.get_valid_moves_for_piece(i, j, piece)
                    if (king_row, king_col) in valid_moves:
                        return True  # Der König wird bedroht

        return False  # Der König ist nicht im Schach
    

    def is_move_legal(self, startrow, startcol, endrow, endcol):
        """
        Checks if the move is legal.
        """
        #check bounding conditions
        if not (0 <= startrow < 8 and 0 <= startcol < 8 and 0 <= endrow < 8 and 0 <= endcol < 8):
            return False

        #check move to same square
        if startrow == endrow and startcol == endcol:
            return False

        #check proprietary of starting square to color
        piece = self.board[startrow, startcol]
        if piece == 0:
            return False
        player = 1 if piece > 0 else -1 
        if (player == 1 and piece < 0) or (player == -1 and piece > 0):
            return False

        # check destination validity
        destination_piece = self.board[endrow, endcol]
        if (destination_piece != 0 and np.sign(destination_piece) == np.sign(piece)):
            return False

        # Get all valid moves
        valid_moves = self.get_valid_moves_for_piece(startrow, startcol, piece)

        # Check if the requested move is in valid moves
        if [startrow, startcol, endrow, endcol] in valid_moves:
            return True

def main():
    board = ChessBoard()

    while True:
        board.get_current_board()
        move = input('make a move')
        board.make_move(move=move)


if __name__ == '__main__':
    main()
