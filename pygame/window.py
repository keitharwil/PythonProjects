import pygame

pygame.init()
screen = pygame.display.set_mode((1280,720)) 
pygame.display.set_caption("NIGGA")
clock = pygame.time.Clock() 
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("BLACK")
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()