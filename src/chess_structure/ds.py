from chessboard import ChessBoard
# Initialize the chess board
chess = ChessBoard()

# Example move: White pawn from e2 to e4 (assuming 0-indexed, e2 is (6,4), e4 is (4,4))
move = [6, 4, 4, 4]

# Make the move and evaluate
board, reward, done = chess.step(move)

# The move and board will be logged if it leads to a better position after 5 moves
