import pygame
import os
import random

# ISITIALIZE THE FONT
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 730

# IMPORT THE FONT
STAT_FONT = pygame.font.SysFont("comicsans", 30)

# IMPORT IMAGES -----------------------------------------------------------------------------------

# BIRD IMAGES
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird3.png")))
]

# PIPE IMAGE
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "pipe.png")))

# BASE IMAGE
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "base.png")))

# BACKGROUND IMAGE
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bg.png")))


# CREATE THE CLASSES FOR THE GAME ( 3 CLASSES ) ---------------------------------------------------

# BIRD CLASS
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -8
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

# BASE CLASS
class Base:
	VEL = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		# IF THE FIRST BASE GETOUT
		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		# IF THE SECOND BASE GETOUT
		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))

# PIPE CLASS
class Pipe:
	GAP = 200 # SPACE BETWEEN TO PIPE
	VEL = 5

	def __init__(self, x):
		self.x = x
		self.height = 0

		self.top = 0
		self.bottom = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False
		self.set_height()

	def set_height(self):
		self.height = random.randrange(70, 470)
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	def move(self):
		self.x -= self.VEL

	def draw(self, win):
		win.blit(self.PIPE_TOP, (self.x, self.top))
		win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

	def collide(self, bird):
		bird_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		t_point = bird_mask.overlap(top_mask, top_offset)
   
		if t_point or b_point or bird.y < 0 or bird.y > 660:
			return True

		return False

# DISPLAY THE CLASSES AND THE INF -----------------------------------------------------------------
def draw_window(win, bird, base, pipes, score, gen, MAX_S):
	
	# DISPLAY THE BACKGROUND
	win.blit(BG_IMG, (0, 0))

	# DISPLAY THE PIPES
	for pipe in pipes:
		pipe.draw(win)

	# DISPLAY THE BIRD
	bird.draw(win)

	# DISPLAY THE BASE
	base.draw(win)

	# DISPLAY SCORE
	score_label = STAT_FONT.render("SCORE: " + str(score), 1, (255, 255, 255))
	win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 10, 10))

	# DISPLAY THE GENERATION
	generation_label = STAT_FONT.render("GEN: " + str(gen), 1, (255, 255, 255))
	win.blit(generation_label, (10, 10))

	# DISPLAY THE MAX SCORE
	max_score = STAT_FONT.render("HIGHT SCORE: " + str(MAX_S), 1, (255, 255, 255))
	win.blit(max_score, (10, 40))


	pygame.display.update()

# MAIN FUNCTION -----------------------------------------------------------------------------------
def main():

	bird = Bird(200, 300)
	base = Base(660)
	pipes = [Pipe(600)]

	GEN = 1
	score = 0
	MAX_S = score

	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	pygame.display.set_caption("FLAPPY BIRD")
	clock = pygame.time.Clock()

	run = True
	while run:
		clock.tick(30)
		# LISTENE TO THE CLOSE EVENT
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# LISTENE TO THE SPACE AND KEY UP EVENT
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
			bird.jump()

		# TAKE CARE OF PIPE
		rem = []
		add_pipe = False

		for pipe in pipes:

			# GAME OVER
			if pipe.collide(bird):
				bird = Bird(200, 300)
				pipes = [Pipe(600)]
				if score > MAX_S:
					MAX_S = score
				score = 0
				GEN += 1

			if pipe.x + pipe.PIPE_TOP.get_width() < 0:
				rem.append(pipe)

			if not pipe.passed and pipe.x < bird.x:
				pipe.passed = True
				add_pipe = True

			pipe.move()

		if add_pipe:
			score += 1
			pipes.append(Pipe(600))

		for r in rem:
			pipes.remove(r)

		# GENELAR SETUP
		bird.move()
		base.move()
		draw_window(win, bird, base, pipes, score, GEN, MAX_S)


main()