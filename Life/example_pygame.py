import pygame
from pygame import display as display
from pygame import draw as draw
from pygame import event as event
import life
import sys

def drawFieldOnSurface(surface, field):
    for cell in field.cells:
        r = (cell.x * cell_size, cell.y * cell_size, cell_size, cell_size)
        cellColor = azure2
        if cell.isAlive:
            cellColor = blueviolet
        draw.rect(surface, cellColor, r, 0)
        



fieldDimension = 30
startPopulationList = [2,5,6,9,10]

#print('init life')

myLife = life.Life(fieldDimension)
#print(life.fieldDimension())
#myLife.printField(myLife.field)
#myLife.populateField(startPopulationList)
myLife.populateAllField()

screen_height = 480
screen_width = 480
screen_caption = 'Life'

cell_size = screen_height / fieldDimension

#pygame.init()
azure2 = pygame.Color('azure3')
blueviolet = pygame.Color('blueviolet')

display.init()
if display.get_init():
    display.set_caption(screen_caption)
    screen = display.set_mode((screen_width, screen_height))
    
    screen.fill(azure2, )
    
    drawFieldOnSurface(screen, myLife.field)
    display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    stateAlives, statehash = myLife.calcStateOfField()

                    drawFieldOnSurface(screen, myLife.field)
                    display.flip()
                   

