import pygame
import os
import sys


SPRITE_SIDE = 90
TILE_IMAGES = {'.': 'empty.png', '#': 'mountain.png'}


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


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def render(self):
        pass


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, *groups):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (SPRITE_SIDE, SPRITE_SIDE))
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
        
        
class Cannon(AnimatedSprite):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = load_image('images/sprites/Cannon/Cannon_enemy.png')
        else:
            sheet = load_image('images/sprites/Cannon/Cannon.png')
        super().__init__(sheet, 4, 3, x, y, *groups)
        
        
class TankLarge(AnimatedSprite):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = load_image('images/sprites/Tank_large/Tank_large_enemy.png')
        else:
            sheet = load_image('images/sprites/Tank_large/Tank_large.png')
        super().__init__(sheet, 5, 2, x, y, *groups)
        
        
class TankMedium(AnimatedSprite):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = load_image('images/sprites/Tank_medium/Tank_medium_enemy.png')
        else:
            sheet = load_image('images/sprites/Tank_medium/Tank_medium.png')
        super().__init__(sheet, 3, 3, x, y, *groups)
        
        
class TankSmall(AnimatedSprite):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = load_image('images/sprites/Tank_small/Tank_small_enemy.png')
        else:
            sheet = load_image('images/sprites/Tank_small/Tank_small.png')
        super().__init__(sheet, 4, 2, x, y, *groups)


class Tile(pygame.sprite.Sprite):
    def __init__(self, char, tile_side, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(load_image('images/tiles/' + TILE_IMAGES[char]), (tile_side, tile_side))
        self.rect = self.image.get_rect().move(x, y)


class BattleField:
    def __init__(self, map_file, cell_size, left_top, scr):
        self.data = [[None] * 10 for _ in range(10)]
        self.height = self.width = 10 * cell_size
        self.cell_size = cell_size
        self.left, self.top = left_top
        self.tiles_group = SpriteGroup()
        self.units_group = SpriteGroup()
        self.all_sprites = SpriteGroup()
        self.own_surface = scr
        self.units_data = {}

        with open('data/maps/' + map_file + '.btlm') as file:
            tile_arr = list(map(lambda x: list(x.strip()), file.readlines()))

        for line in range(len(tile_arr)):
            for column in range(len(tile_arr)):
                self.data[line][column] = Tile(tile_arr[line][column], cell_size,
                                               self.left + self.cell_size * column,
                                               self.top + self.cell_size * line,
                                               self.tiles_group, self.all_sprites)

    def render(self):
        self.all_sprites.draw(self.own_surface)

    def tap_converter(self, tap_pos):
        find_x = (tap_pos[0] - self.left) // self.cell_size
        find_y = (tap_pos[1] - self.top) // self.cell_size
        if find_x >= self.width or find_x < 0 or find_y >= self.height or find_y < 0:
            return None
        else:
            return tuple([find_x, find_y])

    def add_unit(self, unit_type, cell_x, cell_y, enemy=False):
        pos_x = cell_x * self.cell_size + self.left
        pos_y = cell_y * self.cell_size + self.top
        if unit_type == 'Artillery':
            unit = [Artillery(pos_x, pos_y, enemy, self.units_group, self.all_sprites), 8, 8]
        elif unit_type == 'Cannon':
            unit = [Cannon(pos_x, pos_y, enemy, self.units_group, self.all_sprites), 12, 12]
        elif unit_type == 'TankLarge':
            unit = [TankLarge(pos_x, pos_y, enemy, self.units_group, self.all_sprites), 10, 10]
        elif unit_type == 'TankMedium':
            unit = [TankMedium(pos_x, pos_y, enemy, self.units_group, self.all_sprites), 9, 9]
        else:
            unit = [TankSmall(pos_x, pos_y, enemy, self.units_group, self.all_sprites), 8, 8]
        self.units_data[tuple([cell_x, cell_y])] = unit

    def tap_dispatcher(self, mouse_pos):
        cell = self.tap_converter(mouse_pos)
        if cell and (cell in list(self.units_data.keys()) and self.units_data[cell][1] == self.units_data[cell][2]):
            self.units_data[cell][1] = 0

    def update(self):
        for key in list(self.units_data.keys()):
            if self.units_data[key][1] < self.units_data[key][2]:
                self.units_data[key][1] += 1
                self.units_data[key][0].update()
