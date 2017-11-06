import sys
import time
import string
import random
import threading

# Personal Files
from Container import Container
from Tree import Tree
import operations
import parser


def main():
	# Holds all the config values
	container = Container()

	#obtain configs in a list format
	config = open(sys.argv[1]).read().splitlines()

	parser.setup(container, config)

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

	# Holds the highest fitness this particular run
	highest_fitness = 0

	# Places the name at the top of the list for the log file
	log_list.append(name)

	# Create the memory list for the current run
	for num in range(0, container.k):
		x = random.randrange(0, 2, 1)
		y = random.randrange(0, 2, 1)

		# Create the memory for a given run
		memory.append((x, y))

	# Fitness Evaluations begin
	for evals in range(1, container.fitness + 1):
		# Holds the values used to calculate the fitness at the end of an eval
		PfitnessValues = []
		OfitnessValues = []
		# Holds the evals fitness value
		PfitnessValue = 0
		OfitnessValue = 0
		tempP = 0
		tempO = 0

		# This is where the game is actually played
		for play in range(container.l):
			# Creates the tree and a list of the elements in the tree in order that they were created
			tree, tree_list = operations.createTree(container.d, container.k)

			# Reorders the list so that they are in the preordered form
			tree_list = operations.reorder(container.d, tree_list)

			newDecision = operations.evaluate(memory, container.k, tree_list, container.decision)

			fitnessP, fitnessO = operations.yearsInJail(newDecision, container.decision)

			# Set the new tit-for-tat decision
			container.decision = newDecision

			PfitnessValues.append(fitnessP)
			OfitnessValues.append(fitnessO)

			if fitnessP > container.solution_fitness:
				container.solution_fitness = fitnessP
				solution_log = open(container.prob_solution_file, 'w')

				for i in tree_list:
					solution_log.write(i + " ")

		for value in PfitnessValues:
			tempP += value

		for value in OfitnessValues:
			tempO += value

		PfitnessValue = tempP / len(PfitnessValues)
		OfitnessValue = tempO / len(OfitnessValues)

		if PfitnessValue > highest_fitness:
			highest_fitness = PfitnessValue
			log_list.append((evals, PfitnessValue))		

	# Inputting the results into the result log
	for i in range(len(log_list)):
		if log_list[i][0] == 'R':
			result_log.write(log_list[i] + "\n")
		else:
			evalValue, fitnessValue = log_list[i]
			result_log.write(str(evalValue) + "	" + str(fitnessValue) + "\n")
	
	result_log.write("\n")


if __name__ == "__main__":
	main()