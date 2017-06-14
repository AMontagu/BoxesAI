import copy

import time

from reflexSolver import ReflexSolver


bla = True

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

		bestResult = -1
		choosenPoint = (True, 0, 0) # isHorizontal, ypos, xpos

		availableH = self.getAvailableHorizontal(boardh)
		availableV = self.getAvailableVertical(boardv)

		#print(availableH)

		try:
			for available in availableH:
				boardhWithPoint = copy.deepcopy(boardh)
				boardhWithPoint[available[0]][available[1]] = True
				result = self.calculate(available[1], available[0], True, 0, True, boardhWithPoint, copy.deepcopy(boardv))
				# print(result, available[0], available[1])
				if bestResult < result:
					bestResult = result
					choosenPoint = (True, available[0], available[1])
					print("choosen point = ", choosenPoint)
			for available in availableV:
				boardvWithPoint = copy.deepcopy(boardv)
				boardvWithPoint[available[0]][available[1]] = True
				result = self.calculate(available[1], available[0], True, 0, False, copy.deepcopy(boardh), boardvWithPoint)
				if bestResult < result:
					bestResult = result
					choosenPoint = (False, available[0], available[1])
					print(choosenPoint)
			print("minmax\n\n\n")
			return choosenPoint
		except RecursionError as e:
			print("reflex")
			return super().play(copy.deepcopy(boardh), copy.deepcopy(boardv), self.owner)

	def calculate(self, xpos, ypos, isMax, currentValue, isHorizontal, boardh, boardv):

		oldBoxFilled = self.lineSize * self.columnSize - self.owner.count(0)

		moveResult, boardh, boardv = self.playReflex(ypos, xpos, isHorizontal, boardh, boardv)

		#print("move result, xpos, ypos", moveResult, xpos, ypos)
		#print(boardh)
		#print(boardv)

		if isMax:
			currentValue += moveResult
		else:
			currentValue -= moveResult

		oldBoxFilled += moveResult

		isMax = not isMax



		"""print(len(availableH))
		print(len(availableV))
		print("\n\n\n")"""

		#while boardv.count(True) != (self.columnSize+1) * self.lineSize and boardh.count(True) != self.columnSize * (self.lineSize+1):

		if isHorizontal:
			availableH = self.getAvailableHorizontal(boardh)
			print("la", len(availableH))
			for available in availableH:
				moveResult = self.calculate(available[1], available[0], isMax, currentValue, True, copy.deepcopy(boardh), copy.deepcopy(boardv))

				if isMax:
					currentValue += moveResult
				else:
					currentValue -= moveResult

				oldBoxFilled += moveResult
				isMax = not isMax

				#print(isHorizontal)
		else:
			availableV = self.getAvailableVertical(boardv)
			print("ici", len(availableV))
			for available in availableV:
				moveResult = self.calculate(available[1], available[0], isMax, currentValue, False, copy.deepcopy(boardh), copy.deepcopy(boardv))

				if isMax:
					currentValue += moveResult
				else:
					currentValue -= moveResult

				oldBoxFilled += moveResult
				isMax = not isMax

				#print(isHorizontal)

		return currentValue

	def playReflex(self, ypos, xpos, isHorizontal, boardh, boardv):
		goodMove = 0
		moveFind = False

		if ypos < self.lineSize and xpos < self.columnSize:
				if boardh[ypos][xpos] == True and boardh[ypos + 1][xpos] == True and boardv[ypos][xpos] == True and boardv[ypos][xpos+1] == True:
					goodMove -= 1

		if ypos > 0 and xpos < self.columnSize:
			if boardh[ypos][xpos] == True and boardh[ypos - 1][xpos] == True and boardv[ypos-1][xpos] == True and boardv[ypos-1][xpos+1] == True:
				goodMove -= 1

		if ypos < self.lineSize and xpos < self.columnSize:
			if boardv[ypos][xpos] == True and boardv[ypos][xpos+1] == True and boardh[ypos][xpos] == True and boardh[ypos+1][xpos]:
				goodMove -= 1

		if ypos < self.lineSize and xpos > 0:
			if boardv[ypos][xpos] == True and boardv[ypos][xpos-1] == True and boardh[ypos][xpos-1] == True and boardh[ypos+1][xpos-1]:
				goodMove -= 1

		if self.checkBoxUp(xpos, ypos, boardh, boardv) and not moveFind:
			isHorizontalMove, y, x = self.getLastPositionBoxUp(xpos, ypos, boardh, boardv)
			if isHorizontal and isHorizontal == isHorizontalMove:
				boardh[y][x] = True
				moveFind = True
			elif isHorizontal == isHorizontalMove:
				boardv[y][x] = True
				moveFind = True

		elif self.checkBoxDown(xpos, ypos, boardh, boardv) and not moveFind:
			isHorizontalMove, y, x = self.getLastPositionBoxDown(xpos, ypos, boardh, boardv)
			if isHorizontal and isHorizontal == isHorizontalMove:
				boardh[y][x] = True
				moveFind = True
			elif isHorizontal == isHorizontalMove:
				boardv[y][x] = True
				moveFind = True

		elif self.checkBoxRight(xpos, ypos, boardh, boardv) and not moveFind:
			isHorizontalMove, y, x = self.getLastPositionBoxRight(xpos, ypos, boardh, boardv)
			if isHorizontal and isHorizontal == isHorizontalMove:
				boardh[y][x] = True
				moveFind = True
			elif isHorizontal == isHorizontalMove:
				boardv[y][x] = True
				moveFind = True

		elif self.checkBoxRight(xpos, ypos, boardh, boardv) and not moveFind:
			isHorizontalMove, y, x = self.getLastPositionBoxLeft(xpos, ypos, boardh, boardv)
			if isHorizontal and isHorizontal == isHorizontalMove:
				boardh[y][x] = True
				moveFind = True
			elif isHorizontal == isHorizontalMove:
				boardv[y][x] = True
				moveFind = True

		else:
			# super().super()
			if isHorizontal:
				availableH = self.getAvailableHorizontal(boardh)

				if len(availableH) > 0:
					# availableH[0][0] = ypos / availableH[0][1] = xpos
					boardh[availableH[0][0]][availableH[0][1]] = True
				else:
					print("error")
			else:
				availableV = self.getAvailableVertical(boardv)

				if len(availableV) > 0:
					boardv[availableV[0][0]][availableV[0][1]] = True
				else:
					print("error")

		if ypos < self.lineSize and xpos < self.columnSize:
			if boardh[ypos][xpos] == True and boardh[ypos + 1][xpos] == True and boardv[ypos][xpos] == True and boardv[ypos][xpos+1] == True:
				goodMove += 1

		if ypos > 0 and xpos < self.columnSize:
			if boardh[ypos][xpos] == True and boardh[ypos - 1][xpos] == True and boardv[ypos-1][xpos] == True and boardv[ypos-1][xpos+1] == True:
				goodMove += 1

		if ypos < self.lineSize and xpos < self.columnSize:
			if boardv[ypos][xpos] == True and boardv[ypos][xpos+1] == True and boardh[ypos][xpos] == True and boardh[ypos+1][xpos] == True:
				goodMove += 1

		if ypos < self.lineSize and xpos > 0:
			if boardv[ypos][xpos] == True and boardv[ypos][xpos-1] == True and boardh[ypos][xpos-1] == True and boardh[ypos+1][xpos-1] == True:
				goodMove += 1

		return goodMove, boardh, boardv


	def getValue(self, xpos, ypos, boardh, boardv):

		if self.checkBoxUp(xpos, ypos, boardh, boardv):
			isHorizontal, x, y = self.getLastPositionBoxUp(xpos, ypos, boardh, boardv)
			if isHorizontal:
				boardh[y][x] = True
			else:
				boardv[y][x] = True
			return 1

		elif self.checkBoxDown(xpos, ypos, boardh, boardv):
			isHorizontal, x, y = self.getLastPositionBoxDown(xpos, ypos, boardh, boardv)
			if isHorizontal:
				boardh[y][x] = True
			else:
				boardv[y][x] = True
			return 1

		elif self.checkBoxRight(xpos, ypos, boardh, boardv):
			isHorizontal, x, y = self.getLastPositionBoxRight(xpos, ypos, boardh, boardv)
			if isHorizontal:
				boardh[y][x] = True
			else:
				boardv[y][x] = True
			return 1

		elif self.checkBoxRight(xpos, ypos, boardh, boardv):
			isHorizontal, x, y = self.getLastPositionBoxLeft(xpos, ypos, boardh, boardv)
			if isHorizontal:
				boardh[y][x] = True
			else:
				boardv[y][x] = True
			return 1

		else:
			# super().super()
			availableH = self.getAvailableHorizontal(boardh)

			if len(availableH) > 0:
				# availableH[0][0] = ypos / availableH[0][1] = xpos
				boardh[availableH[0][0]][availableH[0][1]] = True
			else:
				availableV = self.getAvailableVertical(boardv)

				if len(availableV) > 0:
					boardv[availableH[0][0]][availableH[0][1]] = True
			return 0

