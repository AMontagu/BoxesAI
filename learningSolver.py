import json
import random

from randomSolver import RandomSolver


class LearningSolver(RandomSolver):

	def __init__(self, columnSize, lineSize):
		super().__init__(columnSize, lineSize)
		self.lastWinnerNumber = 0
		self.lastYPos = 0
		self.lastXPos = 0
		self.lastBoardV = list()
		self.lastBoardH = list()

	def play(self, boardh, boardv, owner):

		for x in range(self.columnSize):
			for y in range(self.lineSize):
				if self.owner[y][x]!=0:
					if self.owner[y][x]=="win":
						self.screen.blit(self.blueplayer, (x*self.squareSize+self.separatorSize, y*self.squareSize+self.separatorSize))
					if self.owner[y][x]=="lose":
						self.screen.blit(self.greenplayer, (x*self.squareSize+self.separatorSize, y*self.squareSize+self.separatorSize))

		data = json.loads(self.readData())

		for element in data:
			if element["boardv"] == boardv and element["boardh"] == boardh:
				if element["point"] > 0:
					return element["hit"][2], element["hit"][0], element["hit"][1]

		return super().play(boardh, boardv, owner)
		#isHorizontal, ypos, xpos = super().play(boardh, boardv, owner)

		#point = sef.checkMove(ypos, xpos, isHorizontal)

		#self.addData(boardh, boardv, ypos, isHorizontal, point)

	def readData(self):
		pass

	def addData(self, data):
		pass