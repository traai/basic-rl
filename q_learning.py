import random

class Environment(object):
	def __init__(self):
		self.s = 'A'
		self.r = 0

	def transition(self, a):
		if self.s == 'A':
			if a == '1':
				self.s = 'A'
				self.r = 10 + random.randint(-3, 3)
			if a == '2':
				if random.uniform(0, 1) <= 0.99:
					self.s = 'B'
				else:
					self.s = 'A'
				self.r = -10 + random.randint(-3, 3)
		elif self.s == 'B':
			if random.uniform(0, 1) <= 0.99:
				self.s = 'A'
			else:
				self.s = 'B'
			if a == '1':
				self.r = 40 + random.randint(-3, 3)
			if a == '2':
				self.r = 20 + random.randint(-3, 3)

	def act(self, a):
		self.transition(a)
		return self.r, self.s

class Agent(object):
	def __init__(self, eta, gamma, env):
		self.q_table = {'A': {'1': 0, '2': 0}, 'B': {'1': 0, '2': 0}}
		self.eta = eta
		self.gamma = gamma
		self.actions = ['1', '2']
		self.env = env

	def execute_action(self, action):
		return self.env.act(action)

	def maxQ(self, s):
		return max([v for _, v in self.q_table[s].items()])

	def argmaxQ(self, s):
		return max(self.q_table[s], key=lambda x: self.q_table[s][x[0]])

	def updateQ(self, s, a, r, new_s):
		self.q_table[s][a] += self.eta * (r + self.gamma * self.maxQ(new_s) - self.q_table[s][a])

	def policy(self, s):
		epsilon = random.uniform(0, 1)
		if epsilon <= 0.2:
			if random.uniform(0, 1) <= 0.5:
				action = '1'
			else:
				action = '2'
		else:
			action = self.argmaxQ(s)
		return action
	def current_policy(self):
		return {'A': self.argmaxQ('A'), 
			'B': self.argmaxQ('B')}

env = Environment()
q_agent = Agent(0.1, 0.9, env)
s = env.s
for t in xrange(0, 5000):
	a = q_agent.policy(s)
	print "time=" + str(t) + ",  state=" + s + ",  action=" + a
	r, new_s = q_agent.execute_action(a)
	print "\n\t\t\t\t reward=" + str(r)
	q_agent.updateQ(s, a, r, new_s)
	s = new_s

print "\n\n-------------------------------------------" 
print "After some exploration, agent figured this:" 
print "\nLong term action values:"
print "(A, 1):", q_agent.q_table['A']['1']
print "(A, 2):", q_agent.q_table['A']['2']
print "(B, 1):", q_agent.q_table['B']['1']
print "(B, 2):", q_agent.q_table['B']['2']
print "\nPolicy to choose actions:" 
policy = q_agent.current_policy()
print "A:", policy['A']
print "B:", policy['B']
print "-------------------------------------------" 
print "-------------------------------------------" 
