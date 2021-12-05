import pygame
from pygame import display as display
from pygame import draw as draw
from pygame import event as event
import life
import sys

def drawFieldOnSurface(surface, field, indexes_to_refresh = None):
    indexes = indexes_to_refresh
    if indexes == None:
        indexes = field.cells.keys()

    for i in indexes:

        x,y = life.Cell.get_coords_by_index(i, field.get_dimension())
        r = (x * cell_size, y * cell_size, cell_size, cell_size)

        cell = field.cells.get(i, None)

        cellColor = azure2
        if not cell == None and cell.is_alive:
            cellColor = blueviolet
            
        draw.rect(surface, cellColor, r, 0)
        



fieldDimension = 5
#startPopulationList = [2,5,6,7,9,10,12,13,17,18,20,22]

fieldDimension = 80
# R - pentamino for dimension 80
#startPopulationList = [38*80+39, 39*80+39, 39*80+40, 40*80+38, 40*80 +39]

fieldDimension = 10
# R - pentamino for dimension 10
#startPopulationList = [34,44,45,53,54]
# R - glider for dimension 10
startPopulationList = [1,12,20,21,22]

fieldDimension = 480
halfDimension = int(fieldDimension/2)
# R - pentamino for dimension 80
startPopulationList = [((halfDimension-1)*fieldDimension+halfDimension), (halfDimension*fieldDimension+halfDimension), (halfDimension*fieldDimension+halfDimension+1), ((halfDimension+1)*fieldDimension+halfDimension-1), ((halfDimension+1)*fieldDimension+halfDimension)]

print('Start position ', startPopulationList)

myLifeField = life.SquadField(fieldDimension)
myLifeField.populate(startPopulationList)

screen_height = 480
screen_width = 480
screen_caption = 'Life'

cell_size = screen_height / fieldDimension

azure2 = pygame.Color('azure3')
blueviolet = pygame.Color('blueviolet')

display.init()
if display.get_init():
    display.set_caption(screen_caption)
    screen = display.set_mode((screen_width, screen_height))
    
    screen.fill(azure2, )
    
    drawFieldOnSurface(screen, myLifeField)
    display.flip()

    states = []
    circleOfLife = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    circleOfLife = not circleOfLife

        if circleOfLife:
            new_state = myLifeField.calc_state()
            changed_indexes = myLifeField.apply_state(new_state)
            drawFieldOnSurface(screen, myLifeField, changed_indexes)

            display.set_caption(screen_caption + ': age ' + str(len(states)) + ', alives ' + str(myLifeField.get_alives()))
            
            if not (myLifeField.get_alives() > 0 and states.count(myLifeField.get_hash()) == 0):
                circleOfLife = False
            else:
                states.append(myLifeField.get_hash())                

            display.flip()

                   

