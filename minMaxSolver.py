import copy
import random

from reflexSolver import ReflexSolver


counter = 0


class MinMaxSolver(ReflexSolver):
	def __init__(self, columnSize, lineSize):
		super().__init__(columnSize, lineSize)

		self.availableH = None
		self.availableV = None
		self.boardh = None
		self.boardv = None
		self.owner = None

	def play(self, boardh, boardv, owner):
		self.availableH = self.getAvailableHorizontal(boardh)
		self.availableV = self.getAvailableVertical(boardv)

		self.boardh = copy.deepcopy(boardh)
		self.boardv = copy.deepcopy(boardv)
		self.owner = copy.deepcopy(owner)



		#print(availableH)
		#print(availableV)

		bestResultSet = False
		bestResult = -1
		choosenPoint = (True, 0, 0) # isHorizontal, ypos, xpos

		availableH = self.getAvailableHorizontal(boardh)
		availableV = self.getAvailableVertical(boardv)

		#print(availableH)

		try:
			for available in availableH:
				result = self.calculate(available[1], available[0], True, True, copy.deepcopy(boardh), copy.deepcopy(boardv), 0)
				#print(result[0], available[0], available[1])
				if not bestResultSet:
					bestResult = result
					choosenPoint = (True, available[0], available[1])
					print("choosen point = ", choosenPoint)
					bestResultSet = True
				elif bestResult < result:
					bestResult = result
					choosenPoint = (True, available[0], available[1])
					print("choosen point = ", choosenPoint)
			for available in availableV:
				result = self.calculate(available[1], available[0], True, False, copy.deepcopy(boardh), copy.deepcopy(boardv), 0)
				#print(result[0], available[0], available[1])
				if not bestResultSet:
					bestResult = result
					choosenPoint = (False, available[0], available[1])
					print("choosen point = ", choosenPoint)
					bestResultSet = True
				elif bestResult < result:
					bestResult = result
					choosenPoint = (False, available[0], available[1])
					print(choosenPoint)
			print("minmax\n\n\n")
			return choosenPoint
		except RecursionError as e:
			print("reflex")
			return super().play(copy.deepcopy(boardh), copy.deepcopy(boardv), self.owner)

	def calculate(self, xpos, ypos, isMax, isHorizontal, boardh, boardv, depth):
		global counter
		counter += 1

		#print(depth)

		currentValue = 0

		if not isHorizontal and boardv[ypos][xpos]:
			print("already true:", boardv[ypos][xpos])


		moveResult, boardh, boardv = self.playPoint(ypos, xpos, isHorizontal, copy.deepcopy(boardh), copy.deepcopy(boardv))

		#print("move result, xpos, ypos", moveResult, xpos, ypos)
		#print(boardh)
		#print(boardv)

		if isMax:
			currentValue += moveResult
		else:
			currentValue -= moveResult

		if moveResult == 0:
			isMax = not isMax

		bestResult = -1
		choosenPoint = (True, 0, 0)  # isHorizontal, ypos, xpos

		availableH = self.getAvailableHorizontal(boardh)
		availableV = self.getAvailableVertical(boardv)



		#print(len(availableH))
		# print(len(availableV))

		availableHit = list()
		for available in availableH:
			availableHit.append((available[0], available[1], True))
		for available in availableV:
			availableHit.append((available[0], available[1], False))

		random.shuffle(availableHit)

		try:
			for available in availableHit:
				if depth < 3:
					result = self.calculate(available[1], available[0], True, available[2], copy.deepcopy(boardh), copy.deepcopy(boardv), depth+1)
				else:
					return currentValue
				# print(result, available[0], available[1])
				if bestResult < result:
					bestResult = result
					#choosenPoint = (True, available[0], available[1])
					#print("choosen point = ", choosenPoint)
			"""if (len(availableV)) > 0:
				result = self.calculate(availableV[0][1], availableV[0][0], True, False, copy.deepcopy(boardh), copy.deepcopy(boardv))
				if bestResult < result:
					bestResult = result
					#choosenPoint = (False, available[0], available[1])
					#print(choosenPoint)"""

			if isMax:
				currentValue += bestResult
			else:
				currentValue -= bestResult

		except RecursionError as e:
			print("reflex in calculate")
			return -1

		return currentValue

	def playPoint(self, ypos, xpos, isHorizontal, boardh, boardv):
		goodMove = 0


		goodMove -= self.countBoxAround(xpos, ypos, boardh, boardv)


		if isHorizontal:
			boardh[ypos][xpos] = True
		else:
			boardv[ypos][xpos] = True

		goodMove += self.countBoxAround(xpos, ypos, boardh, boardv)

		return goodMove, boardh, boardv


	def countBoxAround(self, xpos, ypos, boardh, boardv):
		result = 0

		if ypos < self.lineSize and xpos < self.columnSize:
			if boardh[ypos][xpos] == True and boardh[ypos + 1][xpos] == True and boardv[ypos][xpos] == True and boardv[ypos][xpos+1] == True:
				result += 1

		if ypos > 0 and xpos < self.columnSize:
			if boardh[ypos][xpos] == True and boardh[ypos - 1][xpos] == True and boardv[ypos-1][xpos] == True and boardv[ypos-1][xpos+1] == True:
				result += 1

		if ypos < self.lineSize and xpos < self.columnSize:
			if boardv[ypos][xpos] == True and boardv[ypos][xpos+1] == True and boardh[ypos][xpos] == True and boardh[ypos+1][xpos] == True:
				result += 1

		if ypos < self.lineSize and xpos > 0:
			if boardv[ypos][xpos] == True and boardv[ypos][xpos-1] == True and boardh[ypos][xpos-1] == True and boardh[ypos+1][xpos-1] == True:
				result += 1

		return result


