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
        if cell.is_alive:
            cellColor = blueviolet
        draw.rect(surface, cellColor, r, 0)
        



fieldDimension = 5
#startPopulationList = [2,5,6,7,9,10,12,13,17,18,20,22]

fieldDimension = 10
# R - pentamino for dimension 10
#startPopulationList = [34,44,45,53,54]
# R - glider for dimension 10
#startPopulationList = [1,12,20,21,22]

fieldDimension = 80
# R - pentamino for dimension 80
startPopulationList = [38*80+39, 39*80+39, 39*80+40, 40*80+38, 40*80 +39]

fieldDimension = 480
halfDimension = int(fieldDimension/2)
# R - pentamino for dimension 80
startPopulationList = [((halfDimension-1)*fieldDimension+halfDimension), (halfDimension*fieldDimension+halfDimension), (halfDimension*fieldDimension+halfDimension+1), ((halfDimension+1)*fieldDimension+halfDimension-1), ((halfDimension+1)*fieldDimension+halfDimension)]
print(startPopulationList)
#print('init life')

myLifeField = life.SquadField(fieldDimension)
myLifeField.populate(startPopulationList)
#myLifeField.populate_all()

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
    
    drawFieldOnSurface(screen, myLifeField)
    display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    stateAlives, statehash = myLifeField.calc_state()

                    drawFieldOnSurface(screen, myLifeField)
                    display.flip()
                   

