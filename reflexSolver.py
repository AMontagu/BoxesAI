from randomSolver import RandomSolver


class ReflexSolver(RandomSolver):
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

		self.boardh = boardh
		self.boardv = boardv
		self.owner = owner

		#print(availableH)
		#print(availableV)

		return self.checkPoint(0, 0)


	def checkPoint(self, xpos, ypos):

		if self.checkBoxUp(xpos, ypos, self.boardh, self.boardv):
			return self.getLastPositionBoxUp(xpos, ypos, self.boardh, self.boardv)

		if self.checkBoxDown(xpos, ypos, self.boardh, self.boardv):
			return self.getLastPositionBoxDown(xpos, ypos, self.boardh, self.boardv)

		elif self.checkBoxRight(xpos, ypos, self.boardh, self.boardv):
			return self.getLastPositionBoxRight(xpos, ypos, self.boardh, self.boardv)

		elif self.checkBoxRight(xpos, ypos, self.boardh, self.boardv):
			return self.getLastPositionBoxLeft(xpos, ypos, self.boardh, self.boardv)

		else:
			if xpos < self.columnSize:
				return self.checkPoint(xpos + 1, ypos)
			elif ypos < self.lineSize:
				return self.checkPoint(0, ypos + 1)
			else:
				return super().play(self.boardh, self.boardv, self.owner)

	def checkBoxUp(self, xpos, ypos, boardh, boardv):
		if ypos < self.lineSize and xpos < self.columnSize:
			return [boardh[ypos][xpos], boardh[ypos + 1][xpos], boardv[ypos][xpos], boardv[ypos][xpos + 1]].count(True) == 3
		else:
			return False

	def getLastPositionBoxUp(self, xpos, ypos, boardh, boardv):
		if not boardh[ypos][xpos]:
			return True, ypos, xpos
		elif not boardh[ypos + 1][xpos]:
			return True, ypos+1, xpos
		elif not boardv[ypos][xpos]:
			return False, ypos, xpos
		elif not boardv[ypos][xpos + 1]:
			return False, ypos, xpos+1
		else:
			print("ERROR")

	def checkBoxDown(self, xpos, ypos, boardh, boardv):
		if ypos > 0 and xpos < self.columnSize:
			return [boardh[ypos][xpos], boardh[ypos - 1][xpos], boardv[ypos-1][xpos], boardv[ypos-1][xpos+1]].count(True) == 3
		else:
			return False

	def getLastPositionBoxDown(self, xpos, ypos, boardh, boardv):
		if not boardh[ypos][xpos]:
			return True, ypos, xpos
		elif not boardh[ypos - 1][xpos]:
			return True, ypos-1, xpos
		elif not boardv[ypos-1][xpos]:
			return False, ypos-1, xpos
		elif not boardv[ypos-1][xpos + 1]:
			return False, ypos-1, xpos+1
		else:
			print("ERROR")

	def checkBoxRight(self, xpos, ypos, boardh, boardv):
		if ypos < self.lineSize and xpos < self.columnSize:
			return [boardv[ypos][xpos], boardv[ypos][xpos+1], boardh[ypos][xpos], boardh[ypos+1][xpos]].count(True) == 3
		return False

	def getLastPositionBoxRight(self, xpos, ypos, boardh, boardv):
		if not boardh[ypos][xpos]:
			return True, ypos, xpos
		elif not boardh[ypos+1][xpos]:
			return True, ypos+1, xpos
		elif not boardv[ypos][xpos]:
			return False, ypos, xpos
		elif not boardv[ypos][xpos + 1]:
			return False, ypos, xpos+1
		else:
			print("ERROR")

	def checkBoxLeft(self, xpos, ypos, boardh, boardv):
		if ypos < self.lineSize and xpos > 0:
			return [boardv[ypos][xpos], boardv[ypos][xpos - 1], boardh[ypos][xpos - 1], boardh[ypos + 1][xpos - 1]].count(True) == 3
		else:
			return False

	def getLastPositionBoxLeft(self, xpos, ypos, boardh, boardv):
		if not boardh[ypos][xpos-1]:
			return True, ypos, xpos-1
		elif not boardh[ypos+1][xpos-1]:
			return True, ypos+1, xpos-1
		elif not boardv[ypos][xpos]:
			return False, ypos, xpos
		elif not boardv[ypos][xpos-1]:
			return False, ypos, xpos-1
		else:
			print("ERROR")
