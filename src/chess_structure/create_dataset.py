from chessboard import ChessBoard
from agent import Agent
import pandas as pd
import random

def create_game():
    env = ChessBoard()
    white = Agent()
    black = Agent()
    episodes = 1  # Anzahl der Spiele erhöhen für besseres Training
    
    for episode in range(episodes):
        state = env.reset()
        done = False
        print(f"\nEpisode {episode + 1}")
        # env.get_current_board()
        
        while not done:
            valid_actions = env.get_valid_actions()
            if not valid_actions:
                print("Keine gültigen Züge, Spiel vorbei!")
                break
            if env.turn == 10:
                action = white.choose_action(state, valid_actions)
                next_state, reward, done = env.step(action)
                white.update_q_value(state, action, reward, next_state, action)
                state = next_state
            elif env.turn == -10:
                action = black.choose_action(state,valid_actions)
                next_state, reward, done = env.step(action)
                black.update_q_value(state, action, reward, next_state, action)
                state = next_state
            
    print(env.bestmoves)
    pd.DataFrame(env.bestmoves).to_csv('moves.csv',index=False)



create_game()

"""TBD:
check checkmate condition
"""
