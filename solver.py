class Solver():
	def __init__(self, columnSize, lineSize):
		self.columnSize = columnSize
		self.lineSize = lineSize

	def getAvailableHorizontal(self, boardh):
		available = list()
		for x in range(0, self.columnSize):
			for y in range(0, self.lineSize+1):
				#print("board[" + str(y) + "][" + str(x) + "]")
				if not boardh[y][x]:
					available.append((y,x))
		return available

	def getAvailableVertical(self, boardv):
		available = list()
		for x in range(0, self.columnSize+1):
			for y in range(0, self.lineSize):
				if not boardv[y][x]:
					available.append((y,x))
		return available