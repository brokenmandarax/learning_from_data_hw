import math
import random


			
class PSim:
	def __init__(self):
		self.x_bounds = (0,1)
		self.y_bounds = (0,1)
		
	class Line:
		def __init__(self, w0 = None, w1 = None, w2 = None):
			if w0 == None:
				(x1, y1, x2, y2) = (random.random(), random.random(), random.random(), random.random())
				slope = (y2-y1) / (x2-x1)
				intercept = y1 - slope * x1
				self.w0 = -1*intercept
				self.w1 = -1*slope
				self.w2 = 1
			else:
				self.w0 = w0
				self.w1 = w1
				self.w2 = w2
		
		def slope(self):
			if w2 == 0:
				return 0
			else:
				return -1*w1/w2
		
		def intercept(self):
			if w2 == 0:
				return 0
			else:
				return -1*w0/w2
		
	class Point:
		def __init__(self, line):
			self.x = random.random()
			self.y = random.random()
			self.true_sign = self.sign(line)
			
		def sign(self, line):
			if self.x * line.slope() + line.intercept() >= self.y:
				return 1
			else:
				return -1
	
	def generate_true_line(self):
		self.true_line = self.Line();
		
	def generate_training_points(self, n):
		self.training_points = [0]*n
		for i in range(0,n):
			self.training_points[i] = self.Point()
			
	def misclassified_points(self, line):
		filter(lambda x : x.true_sign != x.sign(line), self.training_points)
			
	def run_single_experiment(self):
		trial_line = self.Line(0, 0, 0)
		num_iterations = 0
		bad_pt = random.choice(self.misclassified_points(trial_line))
		
		
	
	def run_multitrial(self, n):
		self.generate_true_line()
		self.generate_training_points(n)
		self.run_single_experiment()
		

print "initialized everything"

sim0 = PSim()
sim0.generate_true_line()
sim0.generate_training_points(100)
sim0.run_multitrial(10)