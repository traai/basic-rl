# Inspired by Rich Sutton's talk: https://www.youtube.com/watch?v=ggqnxyjaKe4
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

print "Welcome reinforcement learners!"
print "You will now try to play this awesome game together."
print "----------------------------------------------------"
play = raw_input("Are you up for the challenge? ")
print "\nHint: Choose actions to get as much reward as you can over time."

if 'y' in play or 'Y' in play:
	print '\n\nActions={1, 2}'
	env = Environment()
	t = 0
	while True:
		a = raw_input("\ntime="+ str(t) +",  state=" + env.s + ",  action=")
		env.act(a)
		t += 1
		r = env.r
		if r > 0:
			r = '+' + str(r)
		print "\n\t\t\t\t reward=" + str(r)
