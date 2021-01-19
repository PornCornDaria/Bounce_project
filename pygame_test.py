import pygame
from pygame import *
from player import *
from blocks import *


WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = (100, 190, 255)


def main():
	pygame.init()
	screen = pygame.display.set_mode(DISPLAY)
	pygame.display.set_caption("Bounce 2.0")
	bg = Surface((WIN_WIDTH, WIN_HEIGHT))
	bg.fill(BACKGROUND_COLOR)
	
	hero = Player(55, 55)
	left = right = False
	up = False
	
	entities = pygame.sprite.Group()
	platforms = []
	entities.add(hero)
	
	level = [
		"--------------------------",
		"-         --            - -",
		"-                   --    - -",
		"-                       - -",
		"-             --        - --",
		"-                       -",
		"--                      -",
		"-           ---            - ",
		"- -                   --- -",
		"-                        - --",
		"-                       -",
		"-      ---              -",
		"- -                       -",
		"-   -----------      -  - ",
		"-                       -",
		"-                -      -",
		"-                   --  -",
		"-    --                   -",
		"-                       -",
		"-------------------------"
	]
	
	timer = pygame.time.Clock()
	
	while 1:
		timer.tick(100)
		screen.blit(bg, (0, 0))
		for e in pygame.event.get():
			if e.type == QUIT:
				raise SystemExit
			if e.type == KEYDOWN and e.key == K_LEFT:
				left = True
			if e.type == KEYDOWN and e.key == K_RIGHT:
				right = True
			if e.type == KEYUP and e.key == K_RIGHT:
				right = False
			if e.type == KEYUP and e.key == K_LEFT:
				left = False
			if e.type == KEYDOWN and e.key == K_UP:
				up = True
			if e.type == KEYUP and e.key == K_UP:
				up = False
		x = y = 0
		for row in level:
			for col in row:
				if col == "-":
					pf = Platform(x, y)
					entities.add(pf)
					platforms.append(pf)
				
				x += PLATFORM_WIDTH
			y += PLATFORM_HEIGHT
			x = 0
		hero.update(left, right, up, platforms)
		entities.draw(screen)
		pygame.display.update()
		pygame.display.flip()


if __name__ == "__main__":
	main()
