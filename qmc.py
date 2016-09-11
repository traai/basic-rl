import gym
import pandas as pd
import numpy as np
import random

MAX_STEPS = 50000
MAX_EPSILON_RED_STEPS = 5000

class Agent(object):
    def __init__(self, eta, gamma, env, num_states, num_actions):
        self.eta = eta
        self.gamma = gamma
        self.actions = [i for i in xrange(num_actions)]
        self.env = env
        # self.q_table = np.random.uniform(low=-1, high=1, size=(num_states, num_actions))
        self.q_table = np.zeros(shape=(num_states, num_actions))
        self.epsilon = 0.5
        self.epsilon_init = 0.5
        self.epsilon_final = 0.3

    def execute_action(self, action):
        return self.env.step(action) # observation, reward, done, info

    def maxQ(self, s):
        return max(self.q_table[s])

    def argmaxQ(self, s):
        return self.q_table[s].argsort()[-1]

    def updateQ(self, s, a, r, new_s):
        self.q_table[s][a] += self.eta * (r + self.gamma * self.maxQ(new_s) - self.q_table[s][a])

    def update_epsilon(self, t):
        if self.epsilon > self.epsilon_final:
            self.epsilon -= (self.epsilon_init - self.epsilon_final) / MAX_EPSILON_RED_STEPS

    def policy(self, s):
        epsilon = random.uniform(0, 1)
        if epsilon <= 0.1:
            action = random.choice(self.actions)
        else:
            action = self.argmaxQ(s)
        return action
    
    def build_state(self, o):
        position, velocity = o
        features = [self.to_bin(position, position_bins), 
                        self.to_bin(velocity, velocity_bins)]
        return int("".join(map(lambda feature: str(int(feature)), features)))

    def to_bin(self, value, bins):
        return np.digitize(x=[value], bins=bins)[0]

env = gym.make('MountainCar-v0')
experiment_filename = './mountaincar-experiment-1'
env.monitor.start(experiment_filename, force=True)
n_features = env.observation_space.shape[0]
bins = 10
n_states = bins ** n_features
n_actions = env.action_space.n
position_bins = pd.cut([-1.2, 0.6], bins=bins, retbins=True)[1][1:-1]
velocity_bins = pd.cut([-0.07, 0.07], bins=bins, retbins=True)[1][1:-1]

q_agent = Agent(0.05, 0.99, env, n_states, n_actions)
step = 0
for e in xrange(50000): 
    o = env.reset()
    s = q_agent.build_state(o)
    accum_r = 0
    for t in xrange(200):
        a = q_agent.policy(s)
        o, r, done, i = q_agent.execute_action(a)
        # env.render()
        new_s = q_agent.build_state(o)
        q_agent.updateQ(s, a, r, new_s)
        s = new_s
        accum_r += r
        step += 1
        if done:
            print "Episode=" + str(e) + ", Total episodic reward=" + str(accum_r)
            break
env.monitor.close()
print q_agent.q_table
