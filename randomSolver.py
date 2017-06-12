import random

from solver import Solver


class RandomSolver(Solver):

	def __init__(self, columnSize, lineSize):
		super().__init__(columnSize, lineSize)

	def play(self, boardh, boardv, owner):
		availableH = self.getAvailableHorizontal(boardh)
		availableV = self.getAvailableVertical(boardv)

		#print(availableH)
		#print(availableV)

		if len(availableH) > 0 and len(availableV) > 0:
			isHorizontal = bool(random.getrandbits(1))
			if isHorizontal:
				y, x = availableH[random.randint(0, len(availableH)-1)]
			else:
				y, x = availableV[random.randint(0, len(availableV)-1)]

		elif len(availableH) > 0:
			isHorizontal = True
			y, x = availableH[random.randint(0, len(availableH)-1)]

		elif len(availableV) > 0:
			isHorizontal = False
			y, x = availableV[random.randint(0, len(availableV)-1)]

		return isHorizontal, y, x
