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

        x,y = life.Cell.get_xy_by_index(i, field.get_dimension())
        r = (x * cell_size, y * cell_size, cell_size, cell_size)

        cell = field.cells.get(i, None)

        cellColor = azure2
        if not cell == None and cell.is_alive:
            cellColor = blueviolet
            
        draw.rect(surface, cellColor, r, 0)
        

#pentamino = {0:(0,1,0), 1:(0,1,1), 2:(1,1,0)}
#glider = {0:(0,1,0), 1:(0,0,1), 2:(1,1,1)}

fieldDimension = 360
myLifeField = life.SquareField(fieldDimension)

halfDimension = int(fieldDimension/2)

# R - galactic in center
#pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.koks_galaxy, halfDimension-4,halfDimension-4)
# R - pentamino in center
pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, halfDimension-1,halfDimension-1)
myLifeField.populate(pentamino_indexes)

pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, int(halfDimension/2),int(halfDimension/2))
myLifeField.populate(pentamino_indexes)

pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, halfDimension + int(halfDimension/2),int(halfDimension/2))
myLifeField.populate(pentamino_indexes)

pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, int(halfDimension/2),int(halfDimension/2) + halfDimension)
myLifeField.populate(pentamino_indexes)

pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, int(halfDimension/2) + halfDimension,int(halfDimension/2) + halfDimension)
myLifeField.populate(pentamino_indexes)

screen_height = 720
screen_width = 720
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

    states = set()
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
            hash_state_set = set([myLifeField.get_hash()])
            drawFieldOnSurface(screen, myLifeField, changed_indexes)

            display.set_caption(screen_caption + ': age ' + str(len(states)) + ', alives ' + str(myLifeField.get_alives()))
            
            if not (myLifeField.get_alives() > 0 and states.isdisjoint(hash_state_set)):
                circleOfLife = False
            else:
                states.add(hash_state_set.pop())                

            display.flip()

                   

