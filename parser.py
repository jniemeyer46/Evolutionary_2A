import string
import time

def setup(container, config):
	# setting up variables using config file
	for rules in config:
		# split the rules into words
		info = rules.split(" ")


		if info[0] == "runs":
			container.runs = int(info[2])
		elif info[0] == "fitness":
			container.fitness = int(info[2])
		elif info[0] == "k":
			container.k = int(info[2])
		elif info[0] == "d":
			container.d = int(info[2])
		elif info[0] == "l":
			container.l = int(info[2])
		elif info[0] == "prob_log_file":
			container.prob_log_file = info[2]
		elif info[0] == "prob_solution_file":
			container.prob_solution_file = info[2]
		elif info[0] == "newSeed":
			if info[2] == '1':
				container.seed = time.time()
				break
			else:
				obtained_seed = open(container.prob_log_file).read().splitlines(2)
				for lines in obtained_seed:
					line = lines.split(" ")
					if line[0] == "Random":
						container.seed = line[3]
						break
