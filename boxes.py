import pygame
import math

import sys

from minMaxSolver import MinMaxSolver
from randomSolver import RandomSolver
from reflexSolver import ReflexSolver

"""class Boxe():
	def __init__(self):
		self.up = False
		self.right = False
		self.down = False
		self.left = False
		
	def isFull(self):
		return self.up and self.right and self.down and self.left
		 
	
	def getAvailable(self):
		available = list()
		return available"""


class BoxesGame():
	def __init__(self, ia):
		pass
		#1
		pygame.init()
		pygame.font.init()

		self.lineSize = 2
		self.columnSize = 2

		self.squareSize = 64
		self.separatorSize = 5

		self.width = self.columnSize* self.squareSize + self.separatorSize
		self.height = self.lineSize * self.squareSize + self.separatorSize + 100
		#2
		#initialize the screen
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Boxes")
		#3
		#initialize pygame clock
		self.clock=pygame.time.Clock()
		self.boardh = [[False for x in range(self.columnSize)] for y in range(self.lineSize+1)]
		self.boardv = [[False for x in range(self.columnSize+1)] for y in range(self.lineSize)]
		self.initGraphics()
		self.userTurn = True
		self.user=0
		self.ia=0
		self.userWin=False
		self.owner = [[0 for x in range(self.columnSize)] for y in range(self.lineSize)]

		if ia == "random":
			self.solver = RandomSolver(self.columnSize, self.lineSize)

		elif ia == "reflex":
			self.solver = ReflexSolver(self.columnSize, self.lineSize)

		elif ia == "minmax":
			self.solver = MinMaxSolver(self.columnSize, self.lineSize)

		elif ia == "learning":
			pass

	def initGraphics(self):
		self.normallinev=pygame.image.load("images/normalline.png")
		self.normallineh=pygame.transform.rotate(pygame.image.load("images/normalline.png"), -90)
		self.bar_donev=pygame.image.load("images/bar_done.png")
		self.bar_doneh=pygame.transform.rotate(pygame.image.load("images/bar_done.png"), -90)
		self.hoverlinev=pygame.image.load("images/hoverline.png")
		self.hoverlineh=pygame.transform.rotate(pygame.image.load("images/hoverline.png"), -90)
		self.separators=pygame.image.load("images/separators.png")
		self.redindicator=pygame.image.load("images/redindicator.png")
		self.greenindicator=pygame.image.load("images/greenindicator.png")
		self.greenplayer=pygame.image.load("images/greenplayer.png")
		self.blueplayer=pygame.image.load("images/blueplayer.png")
		self.winningscreen=pygame.image.load("images/youwin.png")
		self.gameover=pygame.image.load("images/gameover.png")
		self.score_panel=pygame.image.load("images/score_panel.png")

	def drawBoard(self):
		for x in range(self.columnSize):
			for y in range(self.lineSize+1):
				#print("board[" + str(y) + "][" + str(x) + "]")
				if not self.boardh[y][x]:
					self.screen.blit(self.normallineh, [(x)*self.squareSize+self.separatorSize, (y)*self.squareSize])
				else:
					self.screen.blit(self.bar_doneh, [(x)*self.squareSize+self.separatorSize, (y)*self.squareSize])
		for x in range(self.columnSize+1):
			for y in range(self.lineSize):
				if not self.boardv[y][x]:
					self.screen.blit(self.normallinev, [(x)*self.squareSize, (y)*self.squareSize+self.separatorSize])
				else:
					self.screen.blit(self.bar_donev, [(x)*self.squareSize, (y)*self.squareSize+self.separatorSize])
		#draw separators
		for x in range(self.columnSize+1):
			for y in range(self.lineSize+1):
				self.screen.blit(self.separators, [x*self.squareSize, y*self.squareSize])

	def drawOwnermap(self):
		for x in range(self.columnSize):
			for y in range(self.lineSize):
				if self.owner[y][x]!=0:
					if self.owner[y][x]=="win":
						self.screen.blit(self.blueplayer, (x*self.squareSize+self.separatorSize, y*self.squareSize+self.separatorSize))
					if self.owner[y][x]=="lose":
						self.screen.blit(self.greenplayer, (x*self.squareSize+self.separatorSize, y*self.squareSize+self.separatorSize))

	def drawHUD(self):
		#draw the background for the bottom:
		self.screen.blit(self.score_panel, [0, self.height - 100])

		#create font
		myfont = pygame.font.SysFont(None, 32)

		#create text surface
		label = myfont.render("Your Turn:", 1, (255,255,255))

		#draw surface
		self.screen.blit(label, (10, self.height - 90))
		self.screen.blit(self.greenindicator, (130, self.height - 95))
		#same thing here
		myfont64 = pygame.font.SysFont(None, 64)
		myfont20 = pygame.font.SysFont(None, 20)

		scoreme = myfont64.render(str(self.user), 1, (255,255,255))
		scoreother = myfont64.render(str(self.ia), 1, (255,255,255))
		scoretextme = myfont20.render("You", 1, (255,255,255))
		scoretextother = myfont20.render("IA", 1, (255,255,255))

		self.screen.blit(scoretextme, (10, self.height - 60))
		self.screen.blit(scoreme, (10, self.height - 50))
		self.screen.blit(scoretextother, (280, self.height - 60))
		self.screen.blit(scoreother, (340, self.height - 50))

	def checkCloseSquare(self, xpos, ypos, isHorizontal):
		# print("checkCloseSquare xpos = ",xpos, " , ypos = ", ypos)
		"""print(self.boardv)
		print(self.boardh)
		print(self.boardh[ypos][xpos])
		print(self.boardh[ypos+1][xpos])
		print(self.boardh[ypos-1][xpos])"""

		if isHorizontal:
			if ypos < self.lineSize and xpos < self.columnSize:
				if self.boardh[ypos][xpos] == True and self.boardh[ypos + 1][xpos] == True and self.boardv[ypos][xpos] == True and self.boardv[ypos][xpos+1] == True:
					self.fillSquare(xpos, ypos, self.userTurn)

			if ypos > 0 and xpos < self.columnSize:
				if self.boardh[ypos][xpos] == True and self.boardh[ypos - 1][xpos] == True and self.boardv[ypos-1][xpos] == True and self.boardv[ypos-1][xpos+1] == True:
					self.fillSquare(xpos, ypos-1, self.userTurn)
		else:
			if ypos < self.lineSize and xpos < self.columnSize:
				if self.boardv[ypos][xpos] == True and self.boardv[ypos][xpos+1] == True and self.boardh[ypos][xpos] == True and self.boardh[ypos+1][xpos]:
					self.fillSquare(xpos, ypos, self.userTurn)

			if ypos < self.lineSize and xpos > 0:
				if self.boardv[ypos][xpos] == True and self.boardv[ypos][xpos-1] == True and self.boardh[ypos][xpos-1] == True and self.boardh[ypos+1][xpos-1]:
					self.fillSquare(xpos-1, ypos, self.userTurn)



	def fillSquare(self, xpos, ypos, isUser):
		#print("fill ", xpos, ypos)
		#print(self.owner)
		if isUser:
			self.owner[ypos][xpos] = "win"
			self.user += 1
		else:
			self.owner[ypos][xpos] = "lose"
			self.ia += 1

	def update(self):
		#sleep to make the game 60 fps

		if self.user + self.ia == self.lineSize * self.columnSize:
			self.userWin = True if self.user > self.ia else False
			return 1

		self.clock.tick(60)

		for event in pygame.event.get():

			# clear the screen
			self.screen.fill(0)
			# draw the board
			self.drawBoard()
			self.drawHUD()
			self.drawOwnermap()

			#quit if the quit button was pressed
			if event.type == pygame.QUIT:
				exit()

			#1
			mouse = pygame.mouse.get_pos()

			#2
			xpos = int(math.ceil((mouse[0]-32)/float(self.squareSize)))
			ypos = int(math.ceil((mouse[1]-32)/float(self.squareSize)))
			# print(xpos)
			# print(ypos)

			#3
			is_horizontal = abs(mouse[1] - ypos*self.squareSize) < abs(mouse[0] - xpos*self.squareSize)

			#4
			ypos = ypos - 1 if mouse[1] - ypos*self.squareSize < 0 and not is_horizontal else ypos
			xpos = xpos - 1 if mouse[0] - xpos*self.squareSize < 0 and is_horizontal else xpos

			#5
			board=self.boardh if is_horizontal else self.boardv
			isoutofbounds=False

			#6
			try:
				if not board[ypos][xpos]:
					if is_horizontal:
						higlight = self.hoverlineh

						higlightXPos = xpos*self.squareSize+self.separatorSize
						higlightYPos = ypos*self.squareSize
					else:
						higlight = self.hoverlinev

						higlightXPos = xpos*self.squareSize
						higlightYPos = ypos*self.squareSize+self.separatorSize

					self.screen.blit(higlight, [higlightXPos, higlightYPos])
			except:
				isoutofbounds=True
				pass
			if not isoutofbounds:
				alreadyplaced=board[ypos][xpos]
			else:
				alreadyplaced=False

			#print("alreadyPlace = ", alreadyplaced)
			#print("isoutofbounds = ", isoutofbounds)

			if pygame.mouse.get_pressed()[0] and not alreadyplaced and not isoutofbounds:
				if is_horizontal:
					self.boardh[ypos][xpos]=True
				else:
					self.boardv[ypos][xpos]=True

				self.checkCloseSquare(xpos, ypos, is_horizontal)

				if self.user + self.ia == self.lineSize * self.columnSize:
					self.userWin = True if self.user > self.ia else False
					# clear the screen
					self.screen.fill(0)
					# draw the board
					self.drawBoard()
					self.drawHUD()
					self.drawOwnermap()
					pygame.display.flip()
					return 1

				if self.userTurn:
					self.userTurn = False
					self.iaPlay()
					self.userTurn = True

		#update the screen
		pygame.display.flip()


	def iaPlay(self):
		isHorizontal, ypos, xpos = self.solver.play(self.boardh, self.boardv, self.owner)

		#print(isHorizontal, ypos, xpos)

		#print(self.boardh)

		if isHorizontal:
			self.boardh[ypos][xpos] = True
		else:
			self.boardv[ypos][xpos] = True

		self.checkCloseSquare(xpos, ypos, isHorizontal)

		pass


	def finished(self):
		self.screen.blit(self.gameover if not self.userWin else self.winningscreen, (0,0))
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			pygame.display.flip()

if __name__ == "__main__":

	sys.setrecursionlimit(15000)

	# ia = "random"
	#ia = "reflex"
	ia = "minmax"
	bg=BoxesGame(ia) #__init__ is called right here
	while 1:
		if bg.update() == 1:
			break
	bg.finished()
