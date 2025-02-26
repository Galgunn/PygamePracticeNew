from scripts.utils import draw_text
import pygame, sys

pygame.init()

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.Font(None, 40)

class MainMenu():
    def __init__(self):
        self.display = pygame.Surface((WINDOW_WIDTH - 100, WINDOW_HEIGHT - 100))

    def run(self):
        while True:
            self.display.fill((255, 255, 255))
            draw_text('main menu', font, (255, 0, 0), self.display, 0, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            screen.blit(self.display, (50, 50))
            clock.tick(60)

if __name__ == '__main__':
    MainMenu().run()
