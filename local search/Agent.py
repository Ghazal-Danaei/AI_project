import Sensor
import random
import numpy as np
from numpy.random import rand
# simulated annealing algorithm
def simulated_annealing(n_iterations, step_size, temp):
	# generate an initial point
	best = random.uniform(-60, 61)
	# evaluate the initial point
	best_eval = Sensor.evaluateState(best)
	# current working solution
	curr, curr_eval = best, best_eval
	# run the algorithm
	for i in range(n_iterations):
		# take a step
		candidate = curr + random.uniform(2, 10)*0.01
		# evaluate candidate point
		candidate_eval = Sensor.evaluateState(candidate)
		# check for new best solution
		if candidate_eval > best_eval:
			# store new best point
			best, best_eval = candidate, candidate_eval
			# report progress
			print('>%d f(%s) = %.5f' % (i, best, best_eval))
		# difference between candidate and current point evaluation
		diff = candidate_eval - curr_eval
		# calculate temperature for current epoch
		t = temp / float(i + 1)
		# calculate metropolis acceptance criterion
		metropolis = np.exp(-diff / t)
		# check if we should keep the new point
		if diff > 0 or rand() < metropolis:
			# store the new current point
			curr, curr_eval = candidate, candidate_eval
	return [best, best_eval]

#you can access to value of objective function in the desired input, using Sensor.evaluate
#remember , the domain of your inputs shall be between [-60,60]


print(simulated_annealing(10, 0.01, 100))






