import pygame, sys

pygame.init()

display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    pygame.display.flip()
    clock.tick(60)