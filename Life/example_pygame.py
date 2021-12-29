import pygame
from pygame import Rect, display as display
from pygame import draw as draw
from pygame import event as event
import life
import sys
import logging

def drawFieldOnSurface(surface, field, indexes_to_refresh = None):
 
    indexes = indexes_to_refresh
    if indexes == None:
        indexes = field.cells.keys()

    for i in indexes:
        cell = field.cells.get(i, None)

        cellColor = azure2
        if not cell == None and cell.is_alive:
            cellColor = blueviolet

        x,y = life.Cell.get_xy_by_index(i, field.get_dimension())
        rect = Rect(x * cell_size, y * cell_size, cell_size, cell_size)

        draw.rect(surface, cellColor, rect, 0)

        
#logging.basicConfig(filename="D:\myPy\Life\log\life.log", level=logging.INFO)
logger = logging.getLogger("exampleApp")
logger.setLevel(logging.INFO)

fh = logging.FileHandler("D:\myPy\Life\log\life.log", 'w+')
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

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
#'''
pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, int(halfDimension/2),int(halfDimension/2))
myLifeField.populate(pentamino_indexes)

pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, halfDimension + int(halfDimension/2),int(halfDimension/2))
myLifeField.populate(pentamino_indexes)

pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, int(halfDimension/2),int(halfDimension/2) + halfDimension)
myLifeField.populate(pentamino_indexes)

pentamino_indexes = myLifeField.calc_figure_indexes(life.Figures.pentamino, int(halfDimension/2) + halfDimension,int(halfDimension/2) + halfDimension)
myLifeField.populate(pentamino_indexes)
#'''
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
    rects = {}

    drawFieldOnSurface(screen, myLifeField)
    display.flip()

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
            logger.info("start calc_state")
            new_state = myLifeField.calc_state(logger)
            logger.info("stop calc_state")
            logger.info("start applyable_state")
            circleOfLife = myLifeField.applyable_state(new_state)
            logger.info("stop applyable_state")
            if circleOfLife:
                logger.info("start apply_state")
                changed_indexes = myLifeField.apply_state(new_state)
                logger.info("stop apply_state")

                logger.info("start drawFieldOnSurface")
                drawFieldOnSurface(screen, myLifeField, changed_indexes)
                logger.info("stop drawFieldOnSurface")

                display.set_caption(screen_caption + ': age ' + str(myLifeField.get_history_count()) + ', alives ' + str(myLifeField.get_alives()))
                logger.info("start flip")
                
                display.flip()
                logger.info("stop flip")

                   

