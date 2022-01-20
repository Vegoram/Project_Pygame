import pygame
import sys
import os
def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

class finalscreen():
    def __init__(self):
        size1 = self.width1, self.height1 = 500, 300
        self.screen1 = pygame.display.set_mode(size1)
        self.FPS = 50
        pygame.init()
        pygame.key.set_repeat(200, 70)
        text_sprites = pygame.sprite.Group()
    def win(self, scor):
        font = pygame.font.Font(None, 30)
        fon = pygame.transform.scale(load_image('images/fail.jpg'), (self.width1, self.height1))
        self.screen1.blit(fon, (0, 0))
        clock = pygame.time.Clock()
        string_rendered3 = font.render('ПОБЕДА', 32, pygame.Color('white'))
        intro_rect3 = string_rendered3.get_rect()
        intro_rect3.top = 140
        intro_rect3.x = 200
        self.screen1.blit(string_rendered3, intro_rect3)
        string_rendered3 = font.render(f"Ваш счет {str(scor)}", 32, pygame.Color('white'))
        intro_rect3 = string_rendered3.get_rect()
        intro_rect3.top = 170
        intro_rect3.x = 170
        self.screen1.blit(string_rendered3, intro_rect3)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    terminate()
                pygame.display.flip()
                clock.tick(self.FPS)
    def fail(self):
        font = pygame.font.Font(None, 30)
        fon = pygame.transform.scale(load_image('images/fail.jpg'), (self.width1, self.height1))
        self.screen1.blit(fon, (0, 0))
        clock = pygame.time.Clock()
        string_rendered3 = font.render('ПОРАЖЕНИЕ', 32, pygame.Color('white'))
        intro_rect3 = string_rendered3.get_rect()
        intro_rect3.top = 120
        intro_rect3.x = 180
        self.screen1.blit(string_rendered3, intro_rect3)
        string_rendered3 = font.render('Не расстраивайтесь. Попробуйте еще раз', 32, pygame.Color('white'))
        intro_rect3 = string_rendered3.get_rect()
        intro_rect3.top = 150
        intro_rect3.x = 40
        self.screen1.blit(string_rendered3, intro_rect3)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    terminate()
                pygame.display.flip()
                clock.tick(self.FPS)
