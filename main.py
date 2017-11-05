import sys
import time
import string
import random
import threading

# Personal Files
from Container import Container
import operations
import parser


def main():
	# Holds all the config values
	container = Container()

	#obtain configs in a list format
	config = open(sys.argv[1]).read().splitlines()

	parser.setup(container, config)

	# Seeds the random function using a saved value that is put into the log file
	random.seed(container.seed)

	# opening the log file 
	result_log = open(container.prob_log_file, 'w')
	# initial formatting of the result log with Result Log at the top and the parameters underneath that
	result_log.write("Result Log \n")
	result_log.write("Random Seed = %s \n" % container.seed)
	result_log.write("Parameters used = {'fitness evaluations': %s, 'number of runs': %s, 'problem solution location': '%s'}\n\n"
					% (container.fitness, container.runs, container.prob_solution_file))

	for run in range(1, container.runs + 1):
		# Used in the result log
		thread_name = "Run %s" % run

		# Spins up the number of runs wanted to be executed for the program
		t = threading.Thread(target = evaluations(thread_name, container, result_log))
		t.start()

	result_log.close()

	# Write to solution log
	# figure out a way to create the correct solutino file with 30 different running threads


# The core of the program
def evaluations(name, container, result_log):
	# Memory used for the tree
	memory = []
	# Log list is used to write to the result log after the run
	log_list = []
	# Best solution found during this particular run
	solution = []
	# Best fitness found which corresponds to the best solution found
	solution_fitness = []

	# Places the name at the top of the list for the log file
	log_list.append(name)

	# Create the memory list for the current run
	for num in range(0, container.k):
		x = random.randrange(0, 2, 1)
		y = random.randrange(0, 2, 1)

		memory.append((x, y))

	for evals in range(1, container.fitness + 1):
		log_list.append((evals, 'fitness'))

	for i in range(len(log_list)):
		if log_list[i][0] == 'R':
			result_log.write(log_list[i] + "\n")
		else:
			evalValue, fitnessValue = log_list[i]
			result_log.write(str(evalValue) + "	" + str(fitnessValue) + "\n")
	
	result_log.write("\n")


if __name__ == "__main__":
	main()