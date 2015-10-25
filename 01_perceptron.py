import math
import random


# One simulation of the perceptron problem.			
class PSim:
	def __init__(self):
		self.x_bounds = (0,1)
		self.y_bounds = (0,1)
	
	# A traditional line is defined as y = mx + b
	class TraditionalLine:
		def __init__(self, slope, intercept):
			self.slope = slope
			self.intercept = intercept
			
		def area_under(self, start=0.0, end=1.0):
			# find x-intercept
			x_intercept = -1 * self.intercept / self.slope
			top_intercept = (1-self.intercept) / self.slope

			if x_intercept < start or x_intercept > end:
				# Line is entirely in positive quadrant
				pass
				
			else:
				# part of the line is in positive quadrant
				if (self.intercept + start*self.slope) > 0:
					# The part from start to x_intercept is positive
					end = x_intercept
				else:
					start = x_intercept
			
			if top_intercept > start and top_intercept < end:
				if top_intercept + start*self.slope > 1:
					start = top_intercept
				else:
					end = top_intercept
			if x_intercept < start and self.slope < 0:
				return 0
			if x_intercept > end and self.slope > 1:
				return 0
			print "%f intercept %f top intercept %f slope %f start %f end" % (self.intercept, top_intercept, self.slope, start, end)
			print (self.intercept + (start*self.slope + end*self.slope)/2)*(end-start)
			return (self.intercept + (start*self.slope + end*self.slope)/2)*(end-start)
			
		def area_difference(self, other, start = 0.0, end = 1.0):
			intersection = (self.intercept - other.intercept)/(other.slope - self.slope)
			if intersection < start or intersection > end:
				return abs(self.area_under(start, end) - other.area_under(start, end))
			else:
				result = abs(self.area_under(start, intersection) - other.area_under(start, intersection)) + abs(self.area_under(intersection, end) + other.area_under(intersection, end))
				#print result
				return result
	
	# A line is defined as a vector of weights [w0, w1, w2].
	class Line:
		def __init__(self, w0 = None, w1 = None, w2 = None):
			if w0 == None:
				self.w0 = random.random()
				self.w1 = random.random()
				self.w2 = random.random()
			else:
				self.w0 = w0
				self.w1 = w1
				self.w2 = w2
		
		def add(self, x0, x1, x2):
			self.w0 += x0
			self.w1 += x1
			self.w2 += x2
			
		def to_traditional_line(self):
			slope = -1 * self.w1/self.w2
			intercept = -1 * self.w0/self.w2
			return PSim.TraditionalLine(slope, intercept)
				
	class Point:
		def __init__(self, coordinates, true_sign):
			self.coordinates = coordinates
			self.true_sign = true_sign
			
		def sign(self, line):
			if line.w0 + line.w1 * self.coordinates[0] + line.w2 * self.coordinates[1] >= 0:
				return 1
			else:
				return -1
		
	def generate_training_points(self, n):
		self.training_points = [0]*n
		p1 = (random.random(), random.random())
		p2 = (random.random(), random.random())
		true_slope = (p2[1] - p1[1])/(p2[0] - p1[0])
		true_intercept = p1[1] - true_slope * p1[0]
		self.true_line = self.TraditionalLine(true_slope, true_intercept)
		for i in range(0,n):
			new_point_coords = (random.random(), random.random())
			if(new_point_coords[0] * true_slope + true_intercept > new_point_coords[1]):
				new_point_true_sign = -1
			else:
				new_point_true_sign = 1
			self.training_points[i] = self.Point(new_point_coords, new_point_true_sign)
		#print "true line: {slope}x + {intercept}".format(slope = true_slope, intercept = true_intercept)
		#print map(lambda x : self.training_points[x].true_sign, range(n))
			
	def misclassified_points(self, line):
		x = filter(lambda x : x.true_sign != x.sign(line), self.training_points)
		return x
	
	def chance_of_failure(self, trial_line):
		proxy_line = trial_line.to_traditional_line()
		return self.true_line.area_difference(proxy_line)
				
	def run_single_experiment(self):
		trial_line = self.Line()
		iterations = 0
		
		# Try to find a misclassified point
		while len(self.misclassified_points(trial_line)) > 0 and iterations < 10000 :
			iterations += 1
			bad_pt = random.choice(self.misclassified_points(trial_line))
			trial_line.add(bad_pt.true_sign, bad_pt.true_sign*bad_pt.coordinates[0], bad_pt.true_sign*bad_pt.coordinates[1])
		chance_of_failure = self.chance_of_failure(trial_line)
		#print chance_of_failure
		return (iterations, chance_of_failure)
		
	def run_multitrial(self, points = 100, trials = 1000):
		running_sum_iterations = 0
		running_sum_chance_of_failure = 0.0
		for i in range(0, trials) :
			self.generate_training_points(points)
			(iterations, chance_of_failure) = self.run_single_experiment()
			print "single trial outcome: %d/%f" % (iterations, chance_of_failure)
			running_sum_iterations += iterations
			running_sum_chance_of_failure += chance_of_failure
		print running_sum_iterations/trials
		print running_sum_chance_of_failure/trials
			
		

print "initialized everything"

sim0 = PSim()
sim0.run_multitrial(10, 10)