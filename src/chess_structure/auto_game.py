from rl_boardenv import ChessEnv
from qagent import QLearningAgent

def train():
    
    env = ChessEnv()
    agent = QLearningAgent()
    episodes = 10  #num of games
    
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            # env.get_current_board()
            valid_actions = env.get_valid_actions()
            action = agent.choose_action(state, valid_actions) 
            next_state, reward, done = env.step(action) 
            
            next_action = agent.choose_action(next_state, valid_actions)
            agent.update_q_value(state, action, reward, next_state, next_action)
            state = next_state

    print("completed")

train()

"""TBD:
check checkmate condition
"""
