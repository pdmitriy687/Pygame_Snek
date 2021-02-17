import pygame,random

#Initialize Pygame
pygame.init()
#Global variables
WINDOW_SIZE = [500,500]
CELL_WIDTH = 25
SCORE = None

#Class definitions
class Body_Segment():
	def __init__(self,size,color,x=None,y=None):
		self.size = size
		self.color = color
		self.direction = [1,0]
		self.x = x
		self.y = y

	def draw(self,surface):
		global CELL_WIDTH

		if self.x == None or self.y == None:
			pass
		else:
			pygame.draw.rect(surface,self.color,(self.x*CELL_WIDTH,self.y*CELL_WIDTH,self.size,self.size))
			pygame.draw.rect(surface,(0,0,0),(self.x*CELL_WIDTH,self.y*CELL_WIDTH,self.size,self.size),1)

class Snake():
	body = []

	def __init__(self,x,y,length = 3):
		self.length = length
		self.x = x
		self.y = y
		self.direction = [1,0]

		for i in range(length):
			self.body.append(Body_Segment(25,(0,255,0),x-i,y))
		self.head = self.body[0]

	def draw(self,surface):
		for segment in self.body:
			if segment == self.head:
				segment.draw(surface)
				if self.direction[0] == 1:
					pygame.draw.circle(surface,(0,0,0),(segment.x*CELL_WIDTH+CELL_WIDTH-5,segment.y*CELL_WIDTH+5),2)
					pygame.draw.circle(surface,(0,0,0),(segment.x*CELL_WIDTH+CELL_WIDTH-5,segment.y*CELL_WIDTH+CELL_WIDTH-5),2)
				elif self.direction[0] == -1:
					pygame.draw.circle(surface,(0,0,0),(segment.x*CELL_WIDTH+5,segment.y*CELL_WIDTH+5),2)
					pygame.draw.circle(surface,(0,0,0),(segment.x*CELL_WIDTH+5,segment.y*CELL_WIDTH+CELL_WIDTH-5),2)
				elif self.direction[1] == -1:
					pygame.draw.circle(surface,(0,0,0),(segment.x*CELL_WIDTH+5,segment.y*CELL_WIDTH+5),2)
					pygame.draw.circle(surface,(0,0,0),(segment.x*CELL_WIDTH+CELL_WIDTH-5,segment.y*CELL_WIDTH+5),2)
				elif self.direction[1] == 1:
					pygame.draw.circle(surface,(0,0,0),(segment.x*CELL_WIDTH+5,segment.y*CELL_WIDTH+CELL_WIDTH-5),2)
					pygame.draw.circle(surface,(0,0,0),(segment.x*CELL_WIDTH+CELL_WIDTH-5,segment.y*CELL_WIDTH+CELL_WIDTH-5),2)
			else:
				segment.draw(surface)

	def move(self):
		#The idea is as follows:
		# -Chop the last piece of the tail and move it to the front with it's new position

		#Chop the last piece
		self.body.pop()
		#Change our direction according to user input
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			if self.direction[0] != -1:
				self.direction[0] = 1
				self.direction[1] = 0
		elif keys[pygame.K_LEFT]:
			if self.direction[0] != 1:
				self.direction[0] = -1
				self.direction[1] = 0
		elif keys[pygame.K_DOWN]:
			if self.direction[1] != -1:
				self.direction[0] = 0
				self.direction[1] = 1
		elif keys[pygame.K_UP]:
			if self.direction[1] != 1:
				self.direction[0] = 0
				self.direction[1] = -1
		#Create a new segment with the new position and add it to the body,as the new head of the snake
		new_segment = Body_Segment(25,(0,255,0),self.head.x+self.direction[0],self.head.y+self.direction[1])
		self.body.insert(0,new_segment)
		self.head = self.body[0]

	def add_segment(self):
		self.length += 1

		new_segment = Body_Segment(25,(0,255,0),self.head.x+self.direction[0],self.head.y+self.direction[1])
		self.body.insert(0,new_segment)
		self.head = self.body[0]

	def check_collision(self,fruit):
		global ALIVE,SCORE

		#Border collisions
		if self.head.x < 0:
			ALIVE = False
		if self.head.x+1 > WINDOW_SIZE[0]//25:
			ALIVE = False
		if self.head.y < 0:
			ALIVE = False
		if self.head.y+1 > WINDOW_SIZE[1]//25:
			ALIVE = False

		#Collisions with the fruit
		if self.head.x == fruit.x and self.head.y == fruit.y:
			SCORE += 1
			self.add_segment()

			new_fruit_x = random.randrange(WINDOW_SIZE[0]//CELL_WIDTH)
			new_fruit_y = random.randrange(WINDOW_SIZE[1]//CELL_WIDTH)
			for segment in self.body:
				if new_fruit_x == segment.x and new_fruit_y == segment.y:
					new_fruit_x = random.randrange(WINDOW_SIZE[0]//CELL_WIDTH)
					new_fruit_y = random.randrange(WINDOW_SIZE[1]//CELL_WIDTH)
			fruit.x = new_fruit_x
			fruit.y = new_fruit_y

		#Body collisions
		for segment in self.body:
			if (segment != self.head) and (segment.x == self.head.x and segment.y == self.head.y):
				ALIVE = False

class Fruit():
	def __init__(self,size,color,x,y):
		self.size = size
		self.color = color
		self.x = x
		self.y = y

	def draw(self,surface):
		pygame.draw.rect(surface,self.color,(self.x*CELL_WIDTH,self.y*CELL_WIDTH,self.size,self.size))
		pygame.draw.rect(surface,(0,0,0),(self.x*CELL_WIDTH,self.y*CELL_WIDTH,self.size,self.size),1)

#Function definitions
def draw_grid(surface,color=(255,255,255)):
	global CELL_WIDTH

	for x in range(WINDOW_SIZE[0]):
		pygame.draw.line(surface,color,(x*CELL_WIDTH,0),(x*CELL_WIDTH,WINDOW_SIZE[1]))
	for y in range(WINDOW_SIZE[1]):
		pygame.draw.line(surface,color,(0,y*CELL_WIDTH),(WINDOW_SIZE[0],y*CELL_WIDTH))

def start_screen(surface):
	global SCORE

	if SCORE == None:
		font = pygame.font.Font(None, 35)
		text = font.render(str("Press SPACE to play"),1,(255,255,255))
		surface.blit(text,(125,220))
	else:
		font = pygame.font.Font(None, 40)
		text = font.render(str("You scored: " + str(SCORE)),1,(255,0,0))
		surface.blit(text,(150,200))

		font = pygame.font.Font(None, 20)
		text = font.render(str("Press SPACE to play"),1,(255,0,0))
		surface.blit(text,(175,230))

def play_game(surface):
	global ALIVE,GAME_OVER,SCORE

	#Define a clock
	clock = pygame.time.Clock()
	#Define objects
	Snek = Snake(10,10)
	Apple = Fruit(25,(255,0,0),random.randrange(WINDOW_SIZE[0]//CELL_WIDTH),random.randrange(WINDOW_SIZE[1]//CELL_WIDTH))
	SCORE = 0
	#Game loop
	ALIVE = True
	while ALIVE:
		#Lock the framerate to 15:
		clock.tick(10)
		#Check for user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GAME_OVER = True
				pygame.quit()
		#Update the game state
		Snek.move()
		Snek.check_collision(Apple)
		#Draw the new frame
		surface.fill((0,0,0))

		draw_grid(surface)
		Snek.draw(surface)
		Apple.draw(surface)

		pygame.display.update()
	Snek.body.clear()

#That's the main function
def main():
	#Create the window
	window = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Snek")

	#Main game loop
	GAME_OVER = False
	while not GAME_OVER:
		#Check for user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GAME_OVER = True
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					#Play Snake
					play_game(window)

		#While the user is not playing, show the "start game" screen
		start_screen(window)
		pygame.display.update()
#The program starts here
main()