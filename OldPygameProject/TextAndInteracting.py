import pygame, sys

pygame.init()

screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Colliding with rects")
clock = pygame.time.Clock()
running = True

player = pygame.Rect(0, 0, 50, 50)
col = ((100, 50, 50)) # Set color
player_speed = 3

"""testing with text"""
test_font = pygame.font.Font(None, 50)
text_surface = test_font.render('E', False, 'Black')
text_rect = text_surface.get_rect()



obstacle = pygame.Rect(screen.get_width() / 2, screen.get_height() / 2, 60, 60)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        """Check that player collides with rect and interact with it"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if player.colliderect(obstacle):
                col = ('Blue')
                print('Interacting')

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.y -= player_speed
        if player.top < 0:
            player.top = 0
    if keys[pygame.K_DOWN]:
        player.y += player_speed
        if player.bottom > screen.get_height():
            player.bottom = screen.get_height()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
        if player.left < 0:
            player.left = 0
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        if player.right > screen.get_width():
            player.right = screen.get_width()

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, col, obstacle)
    pygame.draw.rect(screen, ((255, 50, 100)), player)

    """Playing around with text rendering here"""
    if player.colliderect(obstacle):
        # Align text at the bottom center of the player rectangle
        text_rect.centerx = player.centerx
        text_rect.top = player.bottom

        screen.blit(text_surface, text_rect)

    pygame.display.update()
    clock.tick(60)