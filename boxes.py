import pygame
import math

class BoxesGame():
	def __init__(self):
		pass
		#1
		pygame.init()
		pygame.font.init()


		self.lineSize = 7
		self.columnSize = 6

		self.squareSize = 64
		self.separatorSize = 5

		width = self.columnSize * self.squareSize + self.separatorSize
		height = self.columnSize * self.squareSize + self.separatorSize + 100
		#2
		#initialize the screen
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Boxes")
		#3
		#initialize pygame clock
		self.clock=pygame.time.Clock()
		self.boardh = [[False for x in range(self.columnSize)] for y in range(self.lineSize)]
		self.boardv = [[False for x in range(self.lineSize)] for y in range(self.columnSize)]
		self.initGraphics()
		self.turn = True
		self.me=0
		self.ia=0
		self.didiwin=False
		self.owner = [[0 for x in range(6)] for y in range(6)]

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
		for x in range(6):
			for y in range(7):
				if not self.boardh[y][x]:
					self.screen.blit(self.normallineh, [(x)*self.squareSize+self.separatorSize, (y)*self.squareSize])
				else:
					self.screen.blit(self.bar_doneh, [(x)*self.squareSize+self.separatorSize, (y)*self.squareSize])
		for x in range(7):
			for y in range(6):
				if not self.boardv[y][x]:
					self.screen.blit(self.normallinev, [(x)*self.squareSize, (y)*self.squareSize+self.separatorSize])
				else:
					self.screen.blit(self.bar_donev, [(x)*self.squareSize, (y)*self.squareSize+self.separatorSize])
		#draw separators
		for x in range(7):
			for y in range(7):
				self.screen.blit(self.separators, [x*self.squareSize, y*self.squareSize])

	def drawOwnermap(self):
		for x in range(6):
			for y in range(6):
				if self.owner[x][y]!=0:
					if self.owner[x][y]=="win":
						self.screen.blit(self.blueplayer, (x*self.squareSize+self.separatorSize, y*self.squareSize+self.separatorSize))
					if self.owner[x][y]=="lose":
						self.screen.blit(self.greenplayer, (x*self.squareSize+self.separatorSize, y*self.squareSize+self.separatorSize))

	def drawHUD(self):
		#draw the background for the bottom:
		self.screen.blit(self.score_panel, [0, 389])

		#create font
		myfont = pygame.font.SysFont(None, 32)

		#create text surface
		label = myfont.render("Your Turn:", 1, (255,255,255))

		#draw surface
		self.screen.blit(label, (10, 400))
		self.screen.blit(self.greenindicator, (130, 395))
		#same thing here
		myfont64 = pygame.font.SysFont(None, 64)
		myfont20 = pygame.font.SysFont(None, 20)

		scoreme = myfont64.render(str(self.me), 1, (255,255,255))
		scoreother = myfont64.render(str(self.ia), 1, (255,255,255))
		scoretextme = myfont20.render("You", 1, (255,255,255))
		scoretextother = myfont20.render("IA", 1, (255,255,255))

		self.screen.blit(scoretextme, (10, 425))
		self.screen.blit(scoreme, (10, 435))
		self.screen.blit(scoretextother, (280, 425))
		self.screen.blit(scoreother, (340, 435))

	def checkCloseSquare(self, xpos, ypos, isHorizontal, isUser):
		print("checkCloseSquare xpos = ",xpos, " , ypos = ", ypos)
		"""print(self.boardv)
		print(self.boardh)
		print(self.boardh[ypos][xpos])
		print(self.boardh[ypos+1][xpos])
		print(self.boardh[ypos-1][xpos])"""

		print(isHorizontal)

		if isHorizontal:
			if self.boardh[ypos][xpos] == True and self.boardh[ypos + 1][xpos] == True and self.boardv[ypos][xpos] == True and self.boardv[ypos][xpos+1] == True:
				print("ici")
				self.fillSquare(xpos, ypos, isUser)
			if self.boardh[ypos][xpos] == True and self.boardh[ypos - 1][xpos] == True and self.boardv[ypos-1][xpos] == True and self.boardv[ypos-1][xpos+1] == True:
				print("ici2")
				self.fillSquare(xpos, ypos-1, isUser)
		else:
			if self.boardv[ypos][xpos] == True and self.boardv[ypos][xpos+1] == True and self.boardh[ypos][xpos] == True and self.boardh[ypos][xpos] and self.boardh[ypos+1][xpos]:
				print("ici")
				self.fillSquare(xpos, ypos, isUser)
			if self.boardv[ypos][xpos] == True and self.boardv[ypos][xpos-1] == True and self.boardh[ypos][xpos-1] == True and self.boardh[ypos+1][xpos-1]:
				print("ici2")
				self.fillSquare(xpos-1, ypos, isUser)



	def fillSquare(self, xpos, ypos, isUser):
		if isUser:
			self.owner[xpos][ypos] = "win"
		else:
			self.owner[xpos][ypos] = "lose"

	def update(self):
		#sleep to make the game 60 fps
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

				self.checkCloseSquare(xpos, ypos, is_horizontal, True)

		#update the screen
		pygame.display.flip()

	def finished(self):
		self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0,0))
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			pygame.display.flip()

if __name__ == "__main__":
	bg=BoxesGame() #__init__ is called right here
	while 1:
		bg.update()
