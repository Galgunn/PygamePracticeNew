import pygame, sys

pygame.init()

# Declare variables

display: pygame.display
clock: pygame.time
running: bool
screen: pygame.Surface

# Initialize variables

display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True
screen = pygame.Surface((500, 500))

# Game loop

while running == True:
    
    # Event handler

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update

    screen.fill('red')
   
    # Render

    display.blit(screen, (0, 0))

    pygame.display.flip()
    clock.tick(60)