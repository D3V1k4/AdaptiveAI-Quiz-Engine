from environment import AdaptiveQuizEnvironment
from agent import QLearningAgent
import random
import matplotlib.pyplot as plt
import numpy as np
agent = QLearningAgent()
rewards = []
for episode in range(5000):

    env = AdaptiveQuizEnvironment()
    np.save("q_table.npy", agent.q_table)

    # Random student ability
    env.student.ability = random.uniform(0.2, 0.9)

    state = env.get_state()

    action = agent.choose_action(state)

    next_state, reward, correct = env.step(action)
    rewards.append(reward)
    agent.update(
        state,
        action,
        reward,
        next_state
    )

print("\nLearned Q Table:\n")
print(agent.q_table)

moving_avg = []

window = 100

for i in range(len(rewards)):
    
    start = max(0, i - window)
    
    avg = sum(rewards[start:i+1]) / (i - start + 1)
    
    moving_avg.append(avg)

plt.plot(moving_avg)
np.save("q_table.npy", agent.q_table)
plt.title("Average Reward Over Time")
plt.xlabel("Episode")
plt.ylabel("Average Reward")

plt.show()

plt.title("RL Agent Rewards")
plt.xlabel("Episode")
plt.ylabel("Reward")

plt.show()