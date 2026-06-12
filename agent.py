import numpy as np

class QLearningAgent:

    def __init__(self):

        self.q_table = np.zeros((6, 3))

        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.2

    def choose_action(self, state):

        if np.random.random() < self.epsilon:
            return np.random.randint(3)

        return np.argmax(self.q_table[state])

    def update(self,
               state,
               action,
               reward,
               next_state):

        best_next_action = np.argmax(
            self.q_table[next_state]
        )

        td_target = reward + (
            self.discount_factor *
            self.q_table[next_state][best_next_action]
        )

        td_error = (
            td_target -
            self.q_table[state][action]
        )

        self.q_table[state][action] += (
            self.learning_rate *
            td_error
        )