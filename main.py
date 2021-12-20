import os
import sys

import pygame
import random

def terminate():
    pygame.quit()
    sys.exit()


size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 50
pygame.init()
pygame.key.set_repeat(200, 70)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image



def start_screen():
    intro_text = ["ЗАСТАВКА", "",]

    fon = pygame.transform.scale(load_image('fon2.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


    sprite = pygame.sprite.Sprite()
    # определим его вид
    image = load_image("Apps launcher.png")

    sprite.image = pygame.transform.scale(image, (80, 40))
    # и размеры
    sprite.rect = sprite.image.get_rect()

    # добавим спрайт в группу
    all_sprites.add(sprite)

    sprite.rect.x = 80
    sprite.rect.y = 380

    sprite2 = pygame.sprite.Sprite()
    # определим его вид
    image1 = load_image("Apps launcher.png")

    sprite2.image = pygame.transform.scale(image1, (80, 40))
    # и размеры
    sprite2.rect = sprite.image.get_rect()

    # добавим спрайт в группу
    all_sprites.add(sprite2)

    sprite2.rect.x = 540
    sprite2.rect.y = 380

    clock = pygame.time.Clock()
    def proverca(f):
        pass

    while True:
        all_sprites.draw(screen)
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in all_sprites:
                    i.kill()
                return 1
        pygame.display.flip()
        clock.tick(FPS)



tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
t = start_screen()
# создадим спрайт
sprite = pygame.sprite.Sprite()
def arrow(k):

    # определим его вид
    sprite.image = load_image("arrow.png")
    # и размеры
    sprite.rect = sprite.image.get_rect()
    # добавим спрайт в группу
    all_sprites.add(sprite)

    sprite.rect.x = k[0]
    sprite.rect.y = k[1]

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            arrow(event.pos)
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)

pygame.quit()

terminate()
