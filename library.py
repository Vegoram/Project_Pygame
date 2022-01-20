import random
import time

import pygame
import os
import sys

SPRITE_SIDE = 90
TILE_IMAGES = {'.': 'empty.png', '#': 'mountain.png', 'f': 'empty2.png'}
WIDTH = HEIGHT = 1000
SCREEN_RECT = (0, 0, WIDTH, HEIGHT)
pygame.init()
screen_size = (WIDTH, HEIGHT)
screen1 = pygame.display.set_mode(screen_size)
h = 0


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
        self.attack_range = None
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

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.attack_range = 3
        self.speed = 3


class Cannon(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Cannon_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Cannon.png')
        super().__init__(sheet, 4, 3, x, y, *groups)
        self.is_enemy = is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.attack_range = 5
        self.speed = 1


class TankLarge(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Tank_large_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Tank_large.png')
        super().__init__(sheet, 5, 2, x, y, *groups)
        self.is_enemy = is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.attack_range = 3
        self.speed = 2


class TankMedium(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Tank_medium_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Tank_medium.png')
        super().__init__(sheet, 3, 3, x, y, *groups)
        self.is_enemy = is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.attack_range = 3
        self.speed = 3


class TankSmall(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Tank_small_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Tank_small.png')
        super().__init__(sheet, 4, 2, x, y, *groups)
        self.is_enemy = is_enemy

    def set_stats(self):
        self.health = 1
        self.attack = 1
        self.attack_range = 1
        self.speed = 4


class Tile(pygame.sprite.Sprite):
    def __init__(self, char, tile_side, x, y, *groups):
        super().__init__(*groups)
        self.tile_side = tile_side
        if char == '#':
            self.kind = 'Mountain'
            self.image = pygame.transform.scale(ldr.load_tile('mountain.png'), (self.tile_side, self.tile_side))
        else:
            self.kind = 'Empty'
            self.image = pygame.transform.scale(ldr.load_tile('empty.png'), (self.tile_side, self.tile_side))
        self.rect = self.image.get_rect().move(x, y)

    def __str__(self):
        return self.kind
        
    def normal(self):
        if self.kind != 'Mountain':
            self.image = pygame.transform.scale(ldr.load_tile('empty.png'), (self.tile_side, self.tile_side))
        
    def target(self):
        if self.kind != 'Mountain':
            self.image = pygame.transform.scale(ldr.load_tile('empty_target.png'), (self.tile_side, self.tile_side))
        
    def move(self):
        if self.kind != 'Mountain':
            self.image = pygame.transform.scale(ldr.load_tile('empty_move.png'), (self.tile_side, self.tile_side))

    def tile_coords(self):
        return tuple([self.rect.x, self.rect.y])


class BattleField:
    def __init__(self, cell_size, left_top, scr, tile_arr):
        self.data = [[None] * 10 for _ in range(10)]
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
        self.move = False
        self.attack = False
        self.hed1 = 0
        self.turn = True
        self.exit = 0
        self.hod = 0
        self.ii = 0
        for line in range(len(tile_arr)):
            for column in range(len(tile_arr)):
                self.data[line][column] = Tile(tile_arr[line][column], cell_size,
                                               self.left + self.cell_size * column,
                                               self.top + self.cell_size * line,
                                               self.tiles_group, self.all_sprites)
    def provvin(self):
        h = True
        for i in range(10):
            for u in range(10):
                if tuple([i, u]) in self.units_data.keys():
                    if not self.units_data[tuple([i, u])][0].is_enemy:
                        h = False
        if h:
            self.exit += 1
        if self.exit == 35:
            return True



    def render(self):
        self.all_sprites.draw(self.own_surface)
        self.atak.draw(self.own_surface)
        
    def normalize(self):
        for i in self.data:
            for j in i:
                j.normal()

    def tap_converter(self, tap_pos):
        find_x = (tap_pos[0] - self.left) // self.cell_size
        find_y = (tap_pos[1] - self.top) // self.cell_size
        if find_x >= self.width or find_x < 0 or find_y >= self.height or find_y < 0:
            return None
        else:
            return tuple([find_x, find_y])

    def add_unit(self, unit_type, cell_x, cell_y, enemy=False):
        if self.data[cell_y][cell_x].kind != 'Mountain':
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

    def tap_dispatcher(self, mouse_pos, type_of_press):
        a = self.tap_converter(mouse_pos)
        b = a and (a in list(self.units_data.keys())) and not self.units_data[a][0].is_enemy
        if type_of_press == 1 and not self.move and self.turn:
            if self.attack:
                self.attacking(self.hed1, mouse_pos)
                self.attack = False
            elif b:
                self.targeting(mouse_pos)
                self.attack = True
                self.hed1 = mouse_pos
        if type_of_press == 3 and not self.attack and self.turn:
            if self.move:
                self.moving(self.hed1, mouse_pos)
                self.move = False
            elif b:
                self.move = True
                self.hed1 = mouse_pos
                self.mapping(mouse_pos)
        else:
            self.move = False

    def mapping(self, mouse_pos):
        cell = self.tap_converter(mouse_pos)
        if cell and (cell in list(self.units_data.keys()) and self.units_data[cell][1] == self.units_data[cell][2]):
            speed = self.units_data[cell][0].speed
            for column in range(cell[0] - speed, cell[0] + speed + 1):
                for line in range(cell[1] - speed, cell[1] + speed + 1):
                    h = tuple([column, line])
                    if line < 0 or column < 0 or line > 9 or column > 9 or h == cell:
                        pass
                    else:
                        if h not in list(self.units_data.keys()):
                            self.data[line][column].move()

    def moving(self, pos1, pos2):
        self.normalize()
        cell1 = self.tap_converter(pos1)
        cell2 = self.tap_converter(pos2)
        if cell1 and cell2:
            speed = self.units_data[cell1][0].speed
            pos_x = cell2[0] * self.cell_size + self.left
            pos_y = cell2[1] * self.cell_size + self.top
            if(cell2 not in list(self.units_data.keys())) and (
                    cell1 in list(self.units_data.keys()) and self.units_data[cell1][1] == self.units_data[cell1][2])\
                    and max(abs(cell2[1] - cell1[1]), abs(cell2[0] - cell1[0])) <= speed and \
                    self.data[cell2[1]][cell2[0]].kind != 'Mountain':
                self.units_data[cell1][0].move(pos_x, pos_y)
                self.units_data[cell2] = self.units_data[cell1]
                del self.units_data[cell1]
                self.turn = False
                self.update()
                pygame.display.flip()
                self.ii_turn()
                self.hod += 1

    def targeting(self, mouse_pos):
        self.normalize()
        cell = self.tap_converter(mouse_pos)
        if cell and (cell in list(self.units_data.keys()) and self.units_data[cell][1] == self.units_data[cell][2]):
            speed = self.units_data[cell][0].attack_range
            for column in range(cell[0] - speed, cell[0] + speed + 1):
                for line in range(cell[1] - speed, cell[1] + speed + 1):
                    h = tuple([column, line])
                    if line < 0 or column < 0 or line > 9 or column > 9 or h == cell:
                        pass
                    else:
                        if h in list(self.units_data.keys()) and self.units_data[h][0].is_enemy != \
                                self.units_data[cell][0].is_enemy:
                            self.data[line][column].target()

    def attacking(self, pos1, pos2):
        self.normalize()
        cell1 = self.tap_converter(pos1)
        cell2 = self.tap_converter(pos2)
        if cell1 and cell2 and cell1 != cell2:
            speed = self.units_data[cell1][0].attack_range
        if cell1 != cell2 and cell1 and cell2 and (cell2 in self.units_data.keys()) and \
                cell1 in list(self.units_data.keys()) and self.units_data[cell1][1] == self.units_data[cell1][2] \
                and max(abs(cell2[1] - cell1[1]), abs(cell2[0] - cell1[0])) <= speed and \
                self.units_data[cell1][0].is_enemy != \
                self.units_data[cell2][0].is_enemy:
            self.units_data[cell1][1] = 0
            self.units_data[cell2][0].health -= self.units_data[cell1][0].attack
            self.turn = False
            self.update()
            pygame.display.flip()
            self.ii_turn()
            self.hod += 1


    def ii_turn(self):
        print()
        enemies = []
        allies = []
        for key in list(self.units_data.keys()):
            if self.units_data[key][0].is_enemy:
                enemies.append(key)
            else:
                allies.append(key)
        flag = True
        for enemy in enemies:
            for ally in allies:
                print(ally, enemy, max(abs(ally[0] - enemy[0]), abs(ally[1] - enemy[1])) <= self.units_data[enemy][0].attack_range)
                if max(abs(ally[0] - enemy[0]), abs(ally[1] - enemy[1])) <= self.units_data[enemy][0].attack_range:
                    self.ii_attack(enemy, ally)
                    flag = False
                    break
        if flag and enemies:
            self.ii_move(random.choice(enemies))
        self.turn = True

    def ii_attack(self, enemy, ally):

        self.data[enemy[0]][ally[0]].target()
        self.data[enemy[1]][ally[1]].target()
        self.normalize()
        self.units_data[ally][0].health -= self.units_data[enemy][0].attack

    def ii_move(self, enemy):
        variants = []
        speed = self.units_data[enemy][0].speed
        for column in range(enemy[0] - speed, enemy[0] + speed + 1):
            for line in range(enemy[1] - speed, enemy[1] + speed + 1):
                h = tuple([column, line])
                if line < 0 or column < 0 or line > 9 or column > 9 or h == enemy:
                    pass
                else:
                    if h not in list(self.units_data.keys()) and self.data[column][line].kind != 'Mountain':
                        self.data[line][column].move()
                        variants.append((line, column))
        self.normalize()
        pos = random.choice(variants)
        pos_x = pos[0] * self.cell_size + self.left
        pos_y = pos[1] * self.cell_size + self.top
        self.units_data[enemy][0].move(pos_x, pos_y)
        self.units_data[pos] = self.units_data[enemy]
        del self.units_data[enemy]

    def update(self):
        enemies = 0
        if not self.move and not self.attack:
            self.normalize()
        for key in list(self.units_data.keys()):
            if self.units_data[key][0].is_enemy:
                enemies += 1
            if self.units_data[key][0].health <= 0:
                self.units_data[key][0].die(self.particles_group, self.all_sprites)
                del self.units_data[key]
            elif self.units_data[key][1] < self.units_data[key][2]:
                self.units_data[key][1] += 1
                self.units_data[key][0].update()
        if enemies == 0:
            self.exit += 1
        if self.exit == 35:
            pygame.quit()
        self.particles_group.update()

    def scor(self):
        d = 10000
        for i in range(10):
            for u in range(10):
                if tuple([i, u]) in self.units_data.keys():
                    if not self.units_data[tuple([i, u])][0].is_enemy:
                        d += 2000
        return d - self.hod * 100



def load_game(map_name, surface):
    map_file = open('data/maps/' + map_name + '.btlm')
    map_info = list(map(lambda x: x.strip(), map_file.readlines()))
    map_file.close()
    tiles = map_info[:10]
    units = map_info[11:]
    field = BattleField(90, (50, 50), surface, tiles)
    for unit in units:
        unit = unit.split()
        field.add_unit(str(unit[0]), int(unit[1]), int(unit[2]), bool(int(unit[3])))
    return field
