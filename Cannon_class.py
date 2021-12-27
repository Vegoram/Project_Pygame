import pygame
import os
import sys


SPRITE_SIDE = 200

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, *groups):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (SPRITE_SIDE, SPRITE_SIDE))


class Cannon(AnimatedSprite):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = load_image('images/sprites/Cannon/Cannon_enemy.png')
        else:
            sheet = load_image('images/sprites/Cannon/Cannon.png')
        super().__init__(sheet, 4, 3, x, y, *groups)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 220, 220
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    cannon = Cannon(10, 10, True, all_sprites)
    for _ in range(10):
        all_sprites.update()
    screen.fill(pygame.Color('#ffffff'))
    pygame.display.flip()
    clock = pygame.time.Clock()
    running = True
    counter = 10
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and counter >= 12:
                counter = 0
        if counter < 12:
            cannon.update()
            counter += 1
        screen.fill(pygame.Color('#ffffff'))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(20)
