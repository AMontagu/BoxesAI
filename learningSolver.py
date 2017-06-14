import json
import random

from randomSolver import RandomSolver


class LearningSolver(RandomSolver):

	def __init__(self, columnSize, lineSize):
		super().__init__(columnSize, lineSize)
		self.lastBoxFilled = 0
		self.lastYPos = 0
		self.lastXPos = 0
		self.lastIsHorizontal = True
		self.lastBoardV = list()
		self.lastBoardH = list()
		self.firstShot = True

	def play(self, boardh, boardv, owner):

		data = self.readData()

		print(data)
		print(data["elements"])

		if not self.firstShot:
			boxFilledIA, boxFilledUser = 0, 0
			for x in range(self.columnSize):
				for y in range(self.lineSize):
					if owner[y][x]=="lose":
						boxFilledIA += 1
					elif owner[y][x]=="win":
						boxFilledUser += 1
			self.updateData(data, self.lastBoardH, self.lastBoardV, self.lastYPos, self.lastXPos, self.lastIsHorizontal, boxFilledIA, boxFilledUser)
			self.lastBoxFilled += (boxFilledIA - boxFilledUser)

		self.firstShot = False

		for element in data["elements"]:
			print(element)
			if element["boardv"] == boardv and element["boardh"] == boardh:
				if element["point"] > 0:
					isHorizontal, ypos, xpos = element["hit"][2], element["hit"][0], element["hit"][1]
					self.lastBoardH = boardh
					self.lastBoardV = boardv
					self.lastYPos = ypos
					self.lastXPos = xpos
					self.lastIsHorizontal = isHorizontal
					return isHorizontal, ypos, xpos

		isHorizontal, ypos, xpos = super().play(boardh, boardv, owner)

		self.lastBoardH = boardh
		self.lastBoardV = boardv
		self.lastYPos = ypos
		self.lastXPos = xpos
		self.lastIsHorizontal = isHorizontal

		return isHorizontal, ypos, xpos

	def readData(self):
		datafile = open("data.json", 'r')

		data = datafile.read()

		datafile.close()

		return json.loads(data)

	def addData(self, data, boardh, boardv, ypos, xpos, isHorizontal, point):
		dict = {
			"boardv": boardv,
			"boardh": boardh,
			"hit": [ypos, xpos, isHorizontal],
			"point": point
		}

		print(dict)

		data["elements"].append(dict)

		jsonObject = json.dumps(data)

		datafile = open("data.json", 'w')

		datafile.write(jsonObject)

		datafile.close()


	def updateData(self, data, boardh, boardv, ypos, xpos, isHorizontal, pointIa, pointUser):
		find = False
		for element in data["elements"]:
			if element["boardv"] == boardv and element["boardh"] == boardh:
				if element["hit"][2] == isHorizontal and element["hit"][0] == ypos and element["hit"][1] == xpos:
					element["point"] += pointIa - pointUser
					find = True

		if not find:
			self.addData(data, boardh, boardv, ypos, xpos, isHorizontal, self.lastBoxFilled - (pointIa - pointUser))

		jsonObject = json.dumps(data)

		datafile = open("data.json", 'w')

		datafile.write(jsonObject)

		datafile.close()