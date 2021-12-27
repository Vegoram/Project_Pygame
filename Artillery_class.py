import pygame
import os
import sys


SPRITE_SIDE = 100

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


class Artillery(AnimatedSprite):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = load_image('images/sprites/Artillery_1/Artillery_1_enemy.png')
        else:
            sheet = load_image('images/sprites/Artillery_1/Artillery_1.png')
        super().__init__(sheet, 4, 2, x, y, *groups)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 120, 120
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    artillery = Artillery(10, 10, True, all_sprites)
    screen.fill(pygame.Color('#ffffff'))
    pygame.display.flip()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        artillery.update()
        screen.fill(pygame.Color('#ffffff'))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(20)
