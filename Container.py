class Container:
	# The seed used in the current run
	seed = 0

	# Number of runs to be executed
	runs = 0
	# Number of Fitness Evaluations to be done
	fitness = 0

	# Length of Agent Memory
	k = 0
	# Tree Depth
	d = 0
	# Number of iterations to be played in a given evaluation
	l = 0
	# Holds the best fitness found for a given execution
	solution_fitness = 0

	# Holds the previous decision, starts with defect
	decision = 'defect'

	# Result Log File
	prob_log_file = 0
	# Solution File
	prob_solution_file = 0