import numpy as np



class ChessBoard():
    bestmoves = []

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
        self.board = ChessBoard.board.copy()
        self.move = ChessBoard.move

        # Turn 10 means white, turn -10 means black's turn
        self.turn = 10
        self.done = False  # Variable for game is done
        self.valid_actions = []
        

    def get_current_board(self):
        print(self.board)
        return self.board

    def make_move(self, move):
        """
        Führt einen Zug aus, wenn er legal ist.
        """
        if len(move) != 4:
            print("Ungültige Zuglänge.")
            return False

        startrow, startcol, endrow, endcol = int(move[0]), int(move[1]), int(move[2]), int(move[3])

        if not self.is_move_legal(startrow, startcol, endrow, endcol):
            print("Illegaler Zug")
            return False

        cur_piece = self.board[startrow, startcol]
        destination_piece = self.board[endrow, endcol]
        self.board[endrow, endcol] = cur_piece
        self.board[startrow, startcol] = 0

        # Prüfen auf Bauernpromotion
        if cur_piece == 1 and endrow == 0:
            self.board[endrow, endcol] = 5 

        elif cur_piece == -1 and endrow == 7:
            self.board[endrow, endcol] = -5 


        # Überprüfe, ob der König nach dem Zug existiert
        if not self.find_king(self.turn * -1):
            print("König wurde geschlagen!")
            self.done = True
            return False

        # Ändere den Zug

        self.turn = self.turn * -1
        return True
    def evaluate_board(self):
        """
        Evaluates the board based on material count.
        Positive score favors White, negative favors Black.
        """
        piece_values = {
            0: 0,
            1: 1,    # White Pawn
            2: 5,    # White Rook
            3: 3,    # White Knight
            4: 3,    # White Bishop
            5: 9,    # White Queen
            6: 100,  # White King
            -1: -1,    # Black Pawn
            -2: -5,    # Black Rook
            -3: -3,    # Black Knight
            -4: -3,    # Black Bishop
            -5: -9,    # Black Queen
            -6: -100   # Black King
        }
        return np.sum([piece_values[piece] for row in self.board for piece in row])
    def minimax(self, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or self.done:
            return self.evaluate_board()

        valid_actions = self.get_valid_actions()
        if not valid_actions:
            if self.is_king_in_check(self.turn):
                # Checkmate
                return -1000 if maximizing_player else 1000
            else:
                # Stalemate
                return 0

        if maximizing_player:
            max_eval = -np.inf
            for action in valid_actions:
                clone = self.clone()
                clone.make_move(action)
                eval = clone.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = np.inf
            for action in valid_actions:
                clone = self.clone()
                clone.make_move(action)
                eval = clone.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    def clone(self):
        """
        Creates a deep copy of the current board state.
        """
        clone = ChessBoard()
        clone.board = self.board.copy()
        clone.turn = self.turn
        clone.done = self.done
        return clone

    def reset(self):
        """Starting state for board"""
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
        self.turn = 10
        return self.board  

    def checkmate(self):
        
        if self.is_king_in_check(self.turn):
            valid_actions = self.get_valid_actions()
            if not valid_actions:
                return True 
        return False

    def is_king_in_check(self, player):
        
        king_position = self.find_king(player)
        if not king_position:
            print(f"König für Spieler {player} nicht gefunden.")
            return False 

        king_row, king_col = king_position

        #finde könig bedrohnungen
        for i in range(8):
            for j in range(8):
                piece = self.board[i, j]
                if piece != 0 and np.sign(piece) == -np.sign(player):
                    valid_moves = self.get_valid_moves_for_piece(i, j, piece)
                    for move in valid_moves:
                        if move[2] == king_row and move[3] == king_col:
                            return True

        return False  

    def is_move_legal(self, startrow, startcol, endrow, endcol):
        
        # Check boundary conditions
        if not (0 <= startrow < 8 and 0 <= startcol < 8 and 0 <= endrow < 8 and 0 <= endcol < 8):
            print("Zug außerhalb des Bretts.")
            return False

        # Check if move is to the same square
        if startrow == endrow and startcol == endcol:
            print("Zug auf das gleiche Feld.")
            return False

        # Check ownership of the starting square (color of piece)
        piece = self.board[startrow, startcol]
        if piece == 0:
            return False  # No piece to move

        player = 10 if piece > 0 else -10  # Determine player (10 = White, -10 = Black)
        if (player == 10 and piece < 0) or (player == -10 and piece > 0):
            return False  # Piece does not belong to the current player

        # Check if destination is valid (empty or opponent's piece)
        destination_piece = self.board[endrow, endcol]

        # king not allowed to be captured
        if abs(destination_piece) == 6:
            return False

        if destination_piece != 0 and np.sign(destination_piece) == np.sign(piece):
            return False  

        # Get all valid moves for the piece
        valid_moves = self.get_valid_moves_for_piece(startrow, startcol, piece)

        # Check if the requested move is in valid moves
        if [startrow, startcol, endrow, endcol] not in valid_moves:
            return False 

        # Temporarily make the move to check if the king remains safe
        original_piece = self.board[endrow, endcol]
        self.board[endrow, endcol] = piece
        self.board[startrow, startcol] = 0

        

        king_safe = not self.is_king_in_check(player)

        # Undo the move
        self.board[startrow, startcol] = piece
        self.board[endrow, endcol] = original_piece

        

        if not king_safe:
            return False  # Move is illegal because the king would be in check

        return True

    def step(self, move):
        """
        Executes a move and evaluates the resulting position.
        Logs the move and board if the position is better after 5 moves.
        
        Returns:
            tuple: (current board, reward, done)
        """
        current_evaluation = self.evaluate_board()
        move_success = self.make_move(move=move)

        if not move_success:
            print(f"Ungültiger Zug: {move}")
            return self.board, -1, False  

        # After making the move, perform the search to evaluate future position
        future_evaluation = self.minimax(depth=1, alpha=-np.inf, beta=np.inf, maximizing_player=(self.turn == -10))

        # Check if the future position is better
        if (self.turn == -10 and future_evaluation > current_evaluation) or \
           (self.turn == 10 and future_evaluation < current_evaluation):
            if self.is_move_legal(move[0],move[1],move[2],move[3]) == False:
                print("legal")
            print(future_evaluation)
            move_str = self.move_to_str(move)
            board_str = self.board_to_str()
            ChessBoard.bestmoves.append(f"{move},{board_str}")

        # Check for checkmate or draw
        if self.checkmate():
            print("Schachmatt erkannt!")
            print(self.board)
            reward = 1 if self.turn == -10 else -1  # Belohnung je nach Gewinner
            self.done = True
            return self.board, reward, self.done

        if self.check_draw():
            print("Remis!")
            print(self.board)
            reward = 0
            self.done = True
            return self.board, reward, self.done

        # No special conditions
        reward = 0
        self.done = False
        return self.board, reward, self.done

    def move_to_str(self, move):
        """
        Converts a move list to a string representation.
        """
        mapping = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        start_col = mapping[move[1]]
        end_col = mapping[move[3]]
        # Rows are 8 to 1 from top to bottom
        start_row = 8 - move[0]
        end_row = 8 - move[2]
        return f"{start_col}{start_row} to {end_col}{end_row}"

    def board_to_str(self):
        """
        Converts the board to a readable string format.
        """
        str = self.board.tostring()
        
        
        return self.board

    def str_to_board(self,str):
        board = np.fromstring(str,dtype=self.board.dtype).reshape(self.board.shape)
        return board

    def get_valid_actions(self):
        actions = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i, j]
                if piece != 0 and np.sign(piece) == np.sign(self.turn):
                    valid_moves = self.get_valid_moves_for_piece(i, j, piece)
                    for move in valid_moves:
                        startrow, startcol, endrow, endcol = move
                        
                        # Überprüfen, ob der Zug legal ist
                        if self.is_move_legal(startrow, startcol, endrow, endcol):
                            actions.append([startrow, startcol, endrow, endcol])
        
        return actions

    def get_valid_moves_for_piece(self, row, col, piece):
        valid_moves = []
        if piece == 1 or piece == -1:
            valid_moves = self.get_valid_pawn_moves(row, col, piece)
        elif piece == 2 or piece == -2:
            valid_moves = self.get_valid_rook_moves(row, col)
        elif piece == 3 or piece == -3:  
            valid_moves = self.get_valid_knight_moves(row, col)
        elif piece == 4 or piece == -4:  
            valid_moves = self.get_valid_bishop_moves(row, col)
        elif piece == 5 or piece == -5: 
            valid_moves = self.get_valid_queen_moves(row, col)
        elif piece == 6 or piece == -6: 
            valid_moves = self.get_valid_king_moves(row, col)
        return valid_moves

    def get_valid_pawn_moves(self, row, col, piece):
        valid_moves = []
        direction = -1 if piece > 0 else 1  # Weiß bewegt sich nach oben, Schwarz nach unten
        
        # Ein Feld vorwärts
        if 0 <= row + direction < 8 and self.board[row + direction, col] == 0:
            valid_moves.append([row, col, row + direction, col])
            
            # Zwei Felder vorwärts vom Startfeld
            if (row == 1 and piece < 0) or (row == 6 and piece > 0):
                if self.board[row + 2 * direction, col] == 0:
                    valid_moves.append([row, col, row + 2 * direction, col])
        
        # Diagonale Links und Rechts für Schlagen
        for dc in [-1, 1]:
            new_col = col + dc
            new_row = row + direction
            if 0 <= new_col < 8 and 0 <= new_row < 8:
                target_piece = self.board[new_row, new_col]
                if target_piece != 0 and np.sign(target_piece) != np.sign(piece):
                    # **Verhindern, dass der König geschlagen wird**
                    # Entfernen Sie diese Bedingung, um die Schach-Erkennung zu ermöglichen
                    # if abs(target_piece) != 6:
                    valid_moves.append([row, col, new_row, new_col])
        
        return valid_moves

    def get_valid_rook_moves(self, row, col):
        valid_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r, c] == 0:
                        valid_moves.append([row, col, r, c]) 
                    elif self.board[r, c] * self.board[row, col] < 0:
                        # **Entfernen Sie die Bedingung, die das Schlagen des Königs verhindert**
                        # if abs(self.board[r, c]) != 6:
                        valid_moves.append([row, col, r, c]) 
                        break
                    else:
                        break 
                else:
                    break
        return valid_moves

    def get_valid_knight_moves(self, row, col):
        valid_moves = []
        knight_moves = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.board[r, c]
                if target_piece == 0 or np.sign(target_piece) != np.sign(self.board[row, col]):
                    # **Entfernen Sie die Bedingung, die das Schlagen des Königs verhindert**
                    # if abs(target_piece) != 6:
                    valid_moves.append([row, col, r, c])
        return valid_moves

    def get_valid_bishop_moves(self, row, col):
        valid_moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r, c] == 0:
                        valid_moves.append([row, col, r, c])
                    elif self.board[r, c] * self.board[row, col] < 0:
                        # **Entfernen Sie die Bedingung, die das Schlagen des Königs verhindert**
                        # if abs(self.board[r, c]) != 6:
                        valid_moves.append([row, col, r, c]) 
                        break
                    else:
                        break 
                else:
                    break
        return valid_moves

    def get_valid_queen_moves(self, row, col):
        return self.get_valid_rook_moves(row, col) + self.get_valid_bishop_moves(row, col)

    def get_valid_king_moves(self, row, col):
        valid_moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.board[r, c]
                if target_piece == 0 or np.sign(target_piece) != np.sign(self.board[row, col]):
                    # **Zusätzliche Bedingung: Verhindern, dass der König neben dem gegnerischen König steht**
                    if not self.is_square_adjacent_to_opponent_king(r, c, self.turn):
                        valid_moves.append([row, col, r, c])
        return valid_moves

    def find_king(self, player):
        for row in range(8):
            for col in range(8):
                if (player == 10 and self.board[row, col] == 6) or (player == -10 and self.board[row, col] == -6):
                    
                    return row, col
        
        return None

    def is_square_adjacent_to_opponent_king(self, row, col, player):
        """
        Überprüft, ob das angegebene Feld (row, col) direkt neben dem gegnerischen König liegt.
        
        Args:
            row (int): Zeile des Feldes.
            col (int): Spalte des Feldes.
            player (int): Aktueller Spieler (10 für Weiß, -10 für Schwarz).
        
        Returns:
            bool: True, wenn das Feld neben dem gegnerischen König liegt, sonst False.
        """
        opponent_player = -player
        opponent_king = self.find_king(opponent_player)
        if opponent_king is None:
            return False  # Gegnerischer König wurde nicht gefunden, Spiel ist wahrscheinlich vorbei
        king_row, king_col = opponent_king
        return abs(row - king_row) <= 1 and abs(col - king_col) <= 1

    def check_draw(self):
        # tbd
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
        # tbd
        return False

    def check_insufficient_material(self):
        # tbd
        
        # Currently: only kings left
        white_pieces = np.abs(self.board[self.board > 0])
        black_pieces = np.abs(self.board[self.board < 0])
        

        
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return True
        return False

    def check_fifty_moves(self):
        # tbd
        return False

    def check_threefold_repetition(self):
        # tbd
        return False

