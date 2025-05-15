# this allows us to use code from
# the open-source pygame library
# throughout this file
from constants import *
import pygame
def main():
	pygame.init
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
		screen.fill((0, 0, 0))
		pygame.display.flip()
if __name__ == "__main__":
	main()
