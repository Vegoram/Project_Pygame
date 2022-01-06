import random
import pygame
import os
import sys

SPRITE_SIDE = 90
TILE_IMAGES = {'.': 'empty.png', '#': 'mountain.png', 'f': 'empty2.png'}
WIDTH = HEIGHT = 1000
SCREEN_RECT = (0, 0, WIDTH, HEIGHT)
pygame.init()
screen_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screen_size)


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


class Loader:
    def load_particle(self, name, color_key=None):
        fullname = os.path.join('data', 'images', 'particles', name)
        return self.main_load(fullname, color_key)

    def load_tile(self, name, color_key=None):
        fullname = os.path.join('data', 'images', 'tiles', name)
        return self.main_load(fullname, color_key)

    def load_sprite_sheet(self, name, color_key=None):
        fullname = os.path.join('data', 'images', 'sprites', name)
        return self.main_load(fullname, color_key)

    def main_load(self, fullname, color_key):
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


ldr = Loader()
parts = []
for imag in [ldr.load_particle('piece_1.png'), ldr.load_particle('piece_2.png'), ldr.load_particle('piece_3.png')]:
    for scal in (32, 35, 37):
        parts.append(pygame.transform.scale(imag, (scal, scal)))
PARTICLES = parts.copy()


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def render(self):
        pass


class Unit(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, *groups):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (SPRITE_SIDE, SPRITE_SIDE))
        self.rect = self.rect.move(x, y)
        self.health = None
        self.attack = None
        self.speed = None
        self.mov = None
        self.set_stats()

    def set_stats(self):
        pass

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

    def deal_damage(self, enemy):
        enemy.health -= self.attack

    def die(self, *groups):
        x_pos = self.rect.x
        y_pos = self.rect.y
        create_particles((x_pos, y_pos), 7, *groups)
        self.kill()

    def move(self, pos1, pos2):
        self.rect.x = pos1
        self.rect.y = pos2


class Particle(pygame.sprite.Sprite):
    def __init__(self, gravity, pos, dx, dy, *groups):
        super().__init__(*groups)
        self.image = random.choice(PARTICLES)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = gravity

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()


def create_particles(position, particle_count, *groups):
    speeds_x = range(-10, 10)
    speeds_y = range(-15, -5)
    for _ in range(particle_count):
        Particle(1, position, random.choice(speeds_x), random.choice(speeds_y), *groups)


class Artillery(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Artillery_1_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Artillery_1.png')
        super().__init__(sheet, 4, 2, x, y, *groups)
        self.is_enemy = is_enemy

    def get_enemi(self):
        return self.is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.speed = 0
        self.dal = 2


class Cannon(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Cannon_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Cannon.png')
        super().__init__(sheet, 4, 3, x, y, *groups)
        self.is_enemy = is_enemy

    def get_enemi(self):
        return self.is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.speed = 0
        self.dal = 2


class TankLarge(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Tank_large_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Tank_large.png')
        super().__init__(sheet, 5, 2, x, y, *groups)
        self.is_enemy = is_enemy

    def get_enemi(self):
        return self.is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.speed = 0
        self.dal = 2


class TankMedium(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Tank_medium_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Tank_medium.png')
        super().__init__(sheet, 3, 3, x, y, *groups)
        self.is_enemy = is_enemy

    def get_enemi(self):
        return self.is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.speed = 0
        self.dal = 2


class TankSmall(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Tank_small_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Tank_small.png')
        super().__init__(sheet, 4, 2, x, y, *groups)
        self.is_enemy = is_enemy

    def get_enemi(self):
        return self.is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.speed = 0
        self.dal = 2


class Tile(pygame.sprite.Sprite):
    def __init__(self, char, tile_side, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(ldr.load_tile(TILE_IMAGES[char]), (tile_side, tile_side))
        self.rect = self.image.get_rect().move(x, y)


class Tile2(pygame.sprite.Sprite):
    def __init__(self, tile_side, x, y, *groups):
        self.x = x
        self.y = y
        super().__init__(*groups)
        self.image = pygame.transform.scale(ldr.load_tile('ramka_red.png'), (tile_side, tile_side))
        self.rect = self.image.get_rect().move(x, y)

    def get_cor(self):
        return tuple([self.x, self.y])


class BattleField:
    def __init__(self, map_file, cell_size, left_top, scr):
        self.data = [[None] * 10 for _ in range(10)]
        self.data2 = [[None] * 10 for _ in range(10)]
        self.height = self.width = 10 * cell_size
        self.cell_size = cell_size
        self.left, self.top = left_top
        self.tiles_group = SpriteGroup()
        self.units_group = SpriteGroup()
        self.particles_group = SpriteGroup()
        self.all_sprites = SpriteGroup()
        self.atak = SpriteGroup()
        self.own_surface = scr
        self.units_data = {}

        with open('data/maps/' + map_file + '.btlm') as file:
            self.tile_arr = list(map(lambda x: list(x.strip()), file.readlines()))
        self.atakdat = self.tile_arr[:]

        for line in range(len(self.tile_arr)):
            for column in range(len(self.tile_arr)):
                self.data[line][column] = Tile(self.tile_arr[line][column], cell_size,
                                               self.left + self.cell_size * column,
                                               self.top + self.cell_size * line,
                                               self.tiles_group, self.all_sprites)

    def render(self):
        self.all_sprites.draw(self.own_surface)
        self.atak.draw(self.own_surface)

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

    def tap_dispatcher(self, mouse_pos, type):
        for i in self.atak:
            i.kill()

    def mox(self, mouse_pos):
        cell = self.tap_converter(mouse_pos)
        if cell and (cell in list(self.units_data.keys()) and self.units_data[cell][1] == self.units_data[cell][2]):
            dal = self.units_data[cell][0].dal
            self.units_data[cell][1] = 0
            for column in range(cell[0] - dal, cell[0] + dal + 1):
                for line in range(cell[1] - dal, cell[1] + dal + 1):
                    h = tuple([column, line])
                    if line < 0 or column < 0 or line > 9 or column > 9 or h == cell:
                        pass
                    else:
                        if h not in list(self.units_data.keys()):
                            self.data2[line][column] = Tile2(self.cell_size,
                                                             self.left + self.cell_size * column,
                                                             self.top + self.cell_size * line,
                                                             self.tiles_group, self.atak)

    def moving(self, pos1, pos2):
        for i in self.atak:
            i.kill()
        cell1 = self.tap_converter(pos1)
        cell2 = self.tap_converter(pos2)
        if cell1 and cell2:
            dal = self.units_data[cell1][0].dal
        pos_x = cell2[0] * self.cell_size + self.left
        pos_y = cell2[1] * self.cell_size + self.top
        if cell1 and cell2 and (not cell2 in self.units_data.keys()) and (
                cell1 in list(self.units_data.keys()) and self.units_data[cell1][1] == self.units_data[cell1][2])\
                and max(abs(cell2[1] - cell1[1]), abs(cell2[0] - cell1[0])) <= dal:
            self.units_data[cell1][0].move(pos_x, pos_y)
            self.units_data[cell2] = self.units_data[cell1]
            del self.units_data[cell1]

    def pricel(self, mouse_pos):
        cell = self.tap_converter(mouse_pos)
        if cell and (cell in list(self.units_data.keys()) and self.units_data[cell][1] == self.units_data[cell][2]):
            dal = self.units_data[cell][0].dal
            for column in range(cell[0] - dal, cell[0] + dal + 1):
                for line in range(cell[1] - dal, cell[1] + dal + 1):
                    h = tuple([column, line])
                    if line < 0 or column < 0 or line > 9 or column > 9 or h == cell:
                        pass
                    else:
                        if h in list(self.units_data.keys()) and self.units_data[h][0].get_enemi() != \
                                self.units_data[cell][0].get_enemi():
                            self.data2[line][column] = Tile2(self.cell_size,
                                                             self.left + self.cell_size * column,
                                                             self.top + self.cell_size * line,
                                                             self.tiles_group, self.atak)
    def atacing(self, pos1, pos2):
        for i in self.atak:
            i.kill()
        cell1 = self.tap_converter(pos1)
        cell2 = self.tap_converter(pos2)
        if cell1 and cell2 and cell1 != cell2:
            dal = self.units_data[cell1][0].dal
        print(max(abs(cell2[1] - cell1[1]), abs(cell2[0] - cell1[0])))
        if cell1 != cell2 and cell1 and cell2 and (cell2 in self.units_data.keys()) and \
                cell1 in list(self.units_data.keys()) and self.units_data[cell1][1] == self.units_data[cell1][2] \
                and max(abs(cell2[1] - cell1[1]), abs(cell2[0] - cell1[0])) <= dal and self.units_data[cell1][0].get_enemi() != \
                                self.units_data[cell2][0].get_enemi():
            self.units_data[cell1][1] = 0
            self.units_data[cell2][0].health = 0

    def update(self):
        for key in list(self.units_data.keys()):
            if self.units_data[key][0].health <= 0:
                self.units_data[key][0].die(self.particles_group, self.all_sprites)
                del self.units_data[key]
            elif self.units_data[key][1] < self.units_data[key][2]:
                self.units_data[key][1] += 1
                self.units_data[key][0].update()
        self.particles_group.update()
