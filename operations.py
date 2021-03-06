from copy import deepcopy
import random

from Container import Container
from Tree import Tree


def createTree(depth, memoryLength):
	funcNodes = ['AND', 'OR', 'NOT', 'XOR']
	agents = ['P', 'O']
	tree_list = []

	# Initialize a tree
	tree = Tree()

	if depth == 1:
		# Obtain the two things needed to make a leaf
		agent = random.choice(agents)
		num = random.randrange(1, (memoryLength + 1))

		# The termination node created
		leaf = agent + str(num)

		# Set the value equal to the created leaf
		tree.add(leaf)
		tree_list.append(leaf)
	else:
		for level in range(depth):
			if level == 0:
				value = random.choice(funcNodes)

				tree.add(value)
				tree_list.append(value)
			elif level is not (depth - 1):
				for node in range(2 ** level):
					value = random.choice(funcNodes)

					tree.add(value)
					tree_list.append(value)
			else:
				for node in range(2 ** level):
					agent = random.choice(agents)
					num = random.randrange(1, (memoryLength + 1))

					leaf = agent + str(num)

					tree.add(leaf)
					tree_list.append(leaf)

	return tree, tree_list


# Make the list a preorder the list
def reorder(depth, list):
	count = 0
	num = 0
	# Holds the position of the element we want to move
	position = (2**(depth - 1) - 1)

	# We don't need to worry about these two trees
	if depth == 1 or depth == 2:
		return list
	# Worry about the rest
	else:
		# If the depth is 3 then we move the elements 1 back
		if depth == 3:
			count = 2
		# Otherwise we move the elements back by a power of 2 (in terms of the loop)
		else:
			num = depth - 2
			count += 2**num

		for level in reversed(range(count)):
			for i in range(0, 2):
				x = list[position]
				del list[position]
				list.insert(position - level, x)
				position += 1	

	return list


def evaluate(memory, memoryLength, tree, decision):
	# Holds a tree that I can change
	temp = deepcopy(tree)

	# Go through the list backwards
	for loc in reversed(range(len(temp))):
		# Determine whether it is a leaf node or not
		if temp[loc][1:].isdigit():
			# Location of the memory spot
			memoryLocation = memoryLength - int(temp[loc][1:])

			# Unpacking the memory tuple
			x, y = memory[memoryLocation]

			# If the leaf has a P in it use the x position, else use the y
			if temp[loc][0] == 'P':
				temp[loc] = x
			elif temp[loc][0] == 'O':
				temp[loc] = y
		else:
			# If the locations to the right of temp have been evaluated already
			if temp[loc+1] == 0 or temp[loc+1] == 1:
				if temp[loc] == 'NOT':
					if temp[loc+1] >= temp[loc+2]:
						t = temp[loc+1] - temp[loc+2]
					else:
						t = temp[loc+2] - temp[loc+1]

					# Does the flipping of the bit
					if t == 1:
						t = 0
					else:
						t = 1


					# Gets rid of the completely evaluated locations
					del temp[loc + 2]
					del temp[loc + 1]

					temp[loc] = t
				elif temp[loc] == 'AND':
					# Determines whether it should be a 1 or a zero
					if temp[loc+1] == 1 and temp[loc+2] == 1:
						t = 1
					else:
						t = 0

					# Gets rid of the completely evaluated locations
					del temp[loc + 2]
					del temp[loc + 1]

					temp[loc] = t
				if temp[loc] == 'OR':
					# Determines whether it should be a 1 or a zero
					if temp[loc+1] == 1 or temp[loc+2] == 1:
						t = 1
					else:
						t = 0

					# Gets rid of the completely evaluated locations
					del temp[loc + 2]
					del temp[loc + 1]

					temp[loc] = t
				if temp[loc] == 'XOR':
					# Determines whether it should be a 1 or a zero
					if temp[loc+1] == 1 and temp[loc+2] == 0:
						t = 1
					elif temp[loc+1] == 0 and temp[loc+2] == 1:
						t = 1
					else:
						t = 0

					# Gets rid of the completely evaluated locations
					del temp[loc + 2]
					del temp[loc + 1]

					temp[loc] = t

	# Determines whether the agent cooperates or defects based on the tree evaluation
	if temp[0] == 1:
		return 'cooperate'
	elif temp[0] == 0:
		return 'defect'


def yearsInJail(decisionP, decisionO):
	fitnessP = 0
	fitnessO = 0

	# If they both cooperate, they get 2 years in jail, 3 fitness point
	if decisionP == decisionO and decisionP == 'cooperate':
		fitnessP += 3
		fitnessO += 3
	# If they both defect, they get 4 years in jail, 1 fitness point
	elif decisionP == decisionO and decisionP == 'defect':
		fitnessP += 1
		fitnessO += 1
	# If they both defect, they get 4 years in jail, 1 fitness point
	elif decisionP == 'cooperate' and decisionO == 'defect':
		fitnessP += 0
		fitnessO += 5
	# If they both defect, they get 4 years in jail, 1 fitness point
	elif decisionP == 'defect' and decisionO == 'cooperate':
		fitnessP += 5
		fitnessO += 0

	return fitnessP, fitnessO



			




