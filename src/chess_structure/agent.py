import random
import numpy as np

class Agent:
    """Wird ersetzt durch NN
    """
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # Discount
        self.epsilon = epsilon  # exploration percentage
        self.q_table = {}  # Q-table for saving states
    
    def choose_action(self, state, valid_actions):

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_actions)
        else:  # Exploitation
            q_values = [self.get_q_value(state, action) for action in valid_actions]
            max_q = max(q_values)
            return valid_actions[q_values.index(max_q)]
    
    def get_q_value(self, state, action):
        action = tuple(action)
        if (tuple(state.flatten()), action) not in self.q_table:
            self.q_table[(tuple(state.flatten()), action)] = 0 
        return self.q_table[(tuple(state.flatten()), action)]
    
    def update_q_value(self, state, action, reward, next_state, next_action):
        action = tuple(action)
        future_q_value = self.get_q_value(next_state, next_action)
        current_q_value = self.get_q_value(state, action)
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * future_q_value - current_q_value)
        self.q_table[(tuple(state.flatten()), action)] = new_q_value
