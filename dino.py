import pygame
import random
pygame.init()

winx, winy = 800,500
win = pygame.display.set_mode((winx,winy))
pygame.display.set_caption("Trex Run")



#========================================================#
# Defining class for dino. #
#========================================================#
class dinosaur(object) :
	def __init__(self,x,y,width,height) :
		self.x = x 
		self.y = y 
		self.width = width
		self.height = height
		self.isjump = False 
		self.jumpcount = 10
		self.img = 1
		self.hitbox = (x, y, width, height)

	def draw(self,win):
		self.hitbox= (self.x, self.y, self.width, self.height+10)
		pygame.draw.rect(win, (0,0,255), self.hitbox, 2)
		if self.img == 4:
			self.img = 0 
		win.blit(dinoimg[self.img],(self.x, self.y ))
		self.img += 1

#========================================================#
# Defining class for clouds. #
#========================================================#
class clouds(object) :
	def __init__(self,x,y,width,height,img):
		self.x = x
		self.y = y 
		self.width = width 
		self.height = height
		self.img = img

	def draw(self,win,vel):
		self.move(vel)
		win.blit(self.img,(self.x, self.y))
	def move(self,vel):
		self.x -= vel
		if self.x < -self.width:
			self.x = winx + self.width

#========================================================#
# Defining class for the Ground #
#========================================================#
class ground(object) :
	def __init__(self, x, y, width, height) :
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def draw(self, win,vel):
		self.move(vel)
		win.blit(background,(self.x, self.y))

	def move(self,vel):
		self.x -= vel
		if self.x < - self.width  :
			self.x = self.width - 10

#========================================================#
# Defining class for Cactus. #
#========================================================#
class cactus(object) :
	def __init__(self,x,y,width,height,img) :
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.img = img
		self.hitbox = (self.x, self.y, self.width, self.height)
	def draw(self, win, vel):
		self.move(vel)
		win.blit(self.img, (self.x, self.y))
		self.hitbox = (self.x, self.y - 3, self.width, self.height)
		pygame.draw.rect(win, (255,0,0),self.hitbox,2)

	def move(self, vel):
		self.x -= vel 

#========================================================#
# The character and background images #
#========================================================#

# Environment velocity #
vel = 10
gameOver = False
numObs = 0
score,prevscore = 0 ,0
retry = pygame.image.load('./images/retry.png')
retx, rety = winx//2 - 30, winy//2 - 50
retw, reth = 66, 57

# Character #
dinowdth, dinohght = 46, 37
dinox, dinoy = 50, 363
dinoimg = []
for i in range (4):
	dinoimg.append(pygame.image.load('./images/dino'+str(i)+'.png'))

# Background #
bcgx, bcgy = 0, 400
bcgw, bcgh = 2400, 24
background = pygame.image.load('./images/2x-horizon.png')
bcgs = []
bcgs.append(ground(bcgx, bcgy, bcgw, bcgh))
bcgs.append(ground(bcgx + bcgw , bcgy, bcgw, bcgh))

# Clouds #
cldx, cldy, cldw, cldh = winx/2, 100, 91, 24
scldx, scldy, scldw, scldh = winx/2+20, 120, 46, 14
img = pygame.image.load('./images/2x-cloud.png')
simg = pygame.image.load('./images/1x-cloud.png')
cloud = []
cloud.append(clouds(cldx, cldy, cldw, cldh,img))
cloud.append(clouds(scldx, scldy, scldw, scldh,simg))

# Cactus #
cactuses = []
cacimg = pygame.image.load('./images/obs1.png')
cacw, cach = 25, 50
cacy = bcgy - cach + 12
lastcac = winx	
lastc = winx

#========================================================#
# Checking overlap of two hitboxes. #
#========================================================#
def checkoverlap(dino, cac) :
	l1, r1 = (dino.x,-dino.y) , (dino.x+dino.width,-(dino.y+dino.height+10))
	l2, r2 = (cac.x,-(cac.y-3)) , (cac.x+cac.width,-(cac.y+cac.height-3))
	if l1[0] > r2[0] or l2[0] > r1[0] :
		return False
	if l1[1] < r2[1] or l2[1] < r1[1] :
		return False
	return True
#========================================================#
# Message Display in Pygame window.
#========================================================#
def message_display(text,x,y) :
	font = pygame.font.Font('freesansbold.ttf', 32)
	largeText = pygame.font.Font('freesansbold.ttf',115)
	msg = font.render(text,True,(0,0,0),(255,255,255))
	textRect = msg.get_rect()
	textRect.center = (x, y)
	win.blit(msg, textRect) 

#========================================================#
# The main redraw function. #
#========================================================#
def redraw():
	global gameOver
	win.fill((255,255,255))
	dino.draw(win)
	message_display(str(int(score)), winx-40, 40)
	for cld in cloud :
		cld.draw(win,vel)
	for bcg in bcgs :
		bcg.draw(win,vel)
	for cac in cactuses :
		if cac.x < -cac.width :
			cactuses.pop(cactuses.index(cac))
		cac.draw(win,vel) 
	pygame.display.update()
	for cac in cactuses:
		if checkoverlap(dino, cac):
			gameOver = True

def gameRetry():
		win.blit(retry, (retx, rety))
		pygame.display.update()

def restart() :
	global gameOver, lastcac, lastc, score
	vel, gameOver = 10, False 
	numObs, score, prevscore = 0, 0, 0
	del cactuses[0:len(cactuses)]
	lastcac = winx	
	lastc = winx


#========================================================#
# The main loop #
#========================================================#
dino = dinosaur(dinox,dinoy,dinowdth,dinohght)
run = True 
while run :
	pygame.time.delay(10)
	for event in pygame.event.get() :
		if event.type == pygame.QUIT :
			run = False 
	# Retry button Click #
		if event.type == pygame.MOUSEBUTTONDOWN:
			if gameOver == True:
				mx,my = pygame.mouse.get_pos()
				#print(mx,my)
				if mx > retx and mx < retx + retw :
					if my > rety and my < rety + reth :
						win.fill((255,255,255))
						restart()
	#--------------------#
#========================================================#
# Increasing The Score #
#========================================================#
	score += vel/100
	if score - prevscore > 100:
		prevscore = score 
		vel += 3 


#========================================================#
# The obstacles for dino.
#========================================================#
	lastcac -= vel 
	if lastc - lastcac > 200 and len(cactuses) < 5 :
		cacx = random.randint(lastc+100, lastc + 400)
		#print(cacx - lastc)
		lastcac, lastc = cacx, cacx
		cactuses.append(cactus(cacx, cacy, cacw, cach,cacimg))

#========================================================#
# Dino Jumps #
#========================================================#
	keys = pygame.key.get_pressed()
	if keys[pygame.K_p] :
		paused = True 
		while paused :
			for event in pygame.event.get() :
				if event.type == pygame.KEYDOWN :
					if event.key == pygame.K_d :
						paused = False

	if dino.isjump == False :
		if keys[pygame.K_SPACE] :
			dino.isjump = True 
	else :
		neg = 1
		if dino.jumpcount < 1:
			neg = -1
		if dino.jumpcount >= -10 :
			dino.y -= (dino.jumpcount**2)*0.5 * neg
			dino.jumpcount-=1
		else :
			dino.isjump = False 
			dino.jumpcount = 10
	if gameOver != True:
		redraw()
	else :
		gameRetry()



pygame.QUIT

