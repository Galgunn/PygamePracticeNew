import pygame

def draw_text(surf, font, text, color, pos):
    text_surf = font.render(text, True, color)
    #text_surf.set_colorkey((0, 0, 0))
    text_rect = text_surf.get_rect()
    print(f'first rect:', text_rect)
    text_rect.topleft = pos
    print(f'second:', text_rect)
    surf.blit(text_surf, text_rect)