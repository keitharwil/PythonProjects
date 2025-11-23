import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800,400)) #Creates window called 'screen' then set_mode' the size of the 'screen'
pygame.display.set_caption("WINDOW")
clock = pygame.time.Clock() # Clock object to control FPS for the game


test_surface = pygame.surface.fill((200,100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.blit(test_surface,(200,100))

    pygame.display.update()
    #Tells while True loop to not go above 60 fps
    clock.tick(60)
