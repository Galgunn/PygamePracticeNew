import pygame, sys
pygame.init()

screen = pygame.display.set_mode((250, 250))
clock = pygame.time.Clock()
running = True
background = pygame.image.load("assets/scrolling background.png").convert_alpha()
background_rect = background.get_rect(topleft= (-125, -125))
mouse_active = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.WINDOWENTER:
              mouse_active = True
        if event.type == pygame.WINDOWLEAVE:
              mouse_active = False
        
    mouse_pos = pygame.mouse.get_pos()
    velocity = 1
    if mouse_pos[0] < 25 and mouse_active == True:
                background_rect.left += velocity
                if background_rect.left >= 0:
                      background_rect.left = 0
    if mouse_pos[0] > 225 and mouse_active == True:
                background_rect.right -= velocity
                if background_rect.right <= 250:
                      background_rect.right = 250

    if mouse_pos[1] < 25 and mouse_active == True:
                background_rect.top += velocity
                if background_rect.top >= 0:
                      background_rect.top = 0
    if mouse_pos[1] > 225 and mouse_active == True:
                background_rect.bottom -= velocity
                if background_rect.bottom <= 250:
                      background_rect.bottom = 250

    screen.blit(background, (background_rect.x, background_rect.y))
    pygame.display.flip()
    clock.tick(60)