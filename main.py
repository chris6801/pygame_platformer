# libraries
import pygame, sys, random, math
from settings import *
from level import Level
from game_data import level_0
from pygame.locals import *

# Game Setups
pygame.init()
FPS = 60
screen = pygame.display.set_mode((screen_width, screen_height))
fpsClock = pygame.time.Clock()  
level = Level(level_0, screen)
test_tile = pygame.sprite.Group()

# Colors
BCKGRND = (0, 0, 0) 
RED = (255, 30, 70)
BLUE = (10, 20, 200)
GREEN = (50, 230, 40)
CHAR_COL = (255, 30, 70)

# Objects

 

pygame.display.set_caption("Test")

def main():
    looping = True

    


    # Main Loop
    while looping:
        # Get inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # Processing


        # Update display
        screen.fill(BCKGRND)
        level.run()
        pygame.display.update()
        fpsClock.tick(FPS)


main()