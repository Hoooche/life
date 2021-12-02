import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1200, 800))

r = pygame.Rect(50, 50, 100, 200)
pygame.draw.rect(screen, (255, 0, 0), r, 0)

pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
