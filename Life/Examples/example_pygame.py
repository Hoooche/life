import pygame
from pygame import display as display
from pygame import draw as draw
from pygame import event as event
#import life
import sys

fieldDimension = 10
startPopulationList = [2,5,6,9,10]

#print('init life')

#myLife = life.Life(fieldDimension)
#print(life.fieldDimension())
#myLife.printField(myLife.field)
#myLife.populateField(startPopulationList)

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
    
#    for cell in myLife.field.cells:
#        if cell.isAlive:
#            r = (cell.x * cell_size, cell.y * cell_size, cell_size, cell_size)
#            draw.rect(screen, blueviolet, r, 0)

    #display.update(r)
    display.flip()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.quit()
                sys.exit()
