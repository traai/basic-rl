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
        self.q_table = np.random.uniform(low=-1, high=1, size=(num_states, num_actions))
        self.epsilon = 0.3
        self.epsilon_init = 0.3
        self.epsilon_final = 0.01

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
        cart_position, pole_angle, cart_velocity, angle_rate_of_change = o
        features = [self.to_bin(cart_position, cart_position_bins),
                        self.to_bin(pole_angle, pole_angle_bins),
                        self.to_bin(cart_velocity, cart_velocity_bins),
                        self.to_bin(angle_rate_of_change, angle_rate_bins)]
        return int("".join(map(lambda feature: str(int(feature)), features)))

    def to_bin(self, value, bins):
        return np.digitize(x=[value], bins=bins)[0]

env = gym.make('CartPole-v0')
experiment_filename = './cartpole-experiment-1'
env.monitor.start(experiment_filename, force=True)
n_features = env.observation_space.shape[0]
bins = 10
n_states = bins ** n_features
n_actions = env.action_space.n
cart_position_bins = pd.cut([-2.4, 2.4], bins=10, retbins=True)[1][1:-1]
pole_angle_bins = pd.cut([-2, 2], bins=10, retbins=True)[1][1:-1]
cart_velocity_bins = pd.cut([-1, 1], bins=10, retbins=True)[1][1:-1]
angle_rate_bins = pd.cut([-3.5, 3.5], bins=10, retbins=True)[1][1:-1]

q_agent = Agent(0.075, 0.99, env, n_states, n_actions)
step = 0
for e in xrange(MAX_STEPS): 
    o = env.reset()
    s = q_agent.build_state(o)
    accum_r = 0
    for t in xrange(200):
        a = q_agent.policy(s)
        o, r, done, i = q_agent.execute_action(a)
        env.render()
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
