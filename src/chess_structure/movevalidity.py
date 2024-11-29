

class MoveValidity():
    """Checking move validty class, class extension.
    """

    def get_valid_actions(self):
        
        actions = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i, j]
                if piece != 0: #check if square is empty
                    if piece > 0: 
                        actions += self.get_valid_moves_for_piece(i, j, piece)
                    else: 
                        actions += self.get_valid_moves_for_piece(i, j, piece)
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
        direction = -1 if piece == 1 else 1 
        
        if self.board[row + direction, col] == 0:
            valid_moves.append([row, col, row + direction, col])
            
        #move twice in row 0       
        if (row == 1 and piece == -1) or (row == 6 and piece == 1):
            if self.board[row + 2 * direction, col] == 0:
                valid_moves.append([row, col, row + 2 * direction, col])
                
        #capture
        if col > 0 and self.board[row + direction, col - 1] * piece < 0:
            valid_moves.append([row, col, row + direction, col - 1])
        if col < 7 and self.board[row + direction, col + 1] * piece < 0:
            valid_moves.append([row, col, row + direction, col + 1])

        return valid_moves

    def get_valid_rook_moves(self, row, col):
        valid_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r, c = r + dr, c + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r, c] == 0:
                        valid_moves.append([row, col, r, c]) 
                    elif self.board[r, c] * self.board[row, col] < 0:
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
                if self.board[r, c] == 0 or self.board[r, c] * self.board[row, col] < 0:
                    valid_moves.append([row, col, r, c])
        return valid_moves

    def get_valid_bishop_moves(self, row, col):
        valid_moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 
        for dr, dc in directions:
            r, c = row, col
            while True:
                r, c = r + dr, c + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r, c] == 0:
                        valid_moves.append([row, col, r, c])
                    elif self.board[r, c] * self.board[row, col] < 0:
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
                if self.board[r, c] == 0 or self.board[r, c] * self.board[row, col] < 0:
                    valid_moves.append([row, col, r, c])
        return valid_moves
