import os
import random
import sys
import time
import pygame


# Объявление констант
SPRITE_SIDE = 90
TILE_IMAGES = {'.': 'empty.png', '#': 'mountain.png'}
WIDTH = 700
HEIGHT = 500
SCREEN_RECT = (0, 0, WIDTH, HEIGHT)
FPS = 40
pygame.init()
artillery_sound = pygame.mixer.Sound('data/sounds/Artillery.wav')
cannon_sound = pygame.mixer.Sound('data/sounds/Cannon.wav')
tank_large_sound = pygame.mixer.Sound('data/sounds/TankLarge.wav')
tank_medium_sound = pygame.mixer.Sound('data/sounds/TankMedium.wav')
tank_small_sound = pygame.mixer.Sound('data/sounds/TankSmall.wav')
screen_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screen_size)
all_sprites = pygame.sprite.Group()


# Класс финального окна
class FinalScreen:
    def __init__(self):
        size1 = self.width1, self.height1 = 500, 300
        self.screen1 = pygame.display.set_mode(size1)
        self.FPS = 50
        pygame.init()
        pygame.key.set_repeat(200, 70)

    def win(self, score):   # Метод победы, отображает на экране переданные в него результаты
        font = pygame.font.Font(None, 30)
        fon = pygame.transform.scale(load_image('images/fail.jpg'), (self.width1, self.height1))
        self.screen1.blit(fon, (0, 0))
        clock = pygame.time.Clock()
        string_rendered3 = font.render('ПОБЕДА', 32, pygame.Color('white'))
        intro_rect3 = string_rendered3.get_rect()
        intro_rect3.top = 140
        intro_rect3.x = 200
        self.screen1.blit(string_rendered3, intro_rect3)
        string_rendered3 = font.render(f"Ваш счет {str(score)}", 32, pygame.Color('white'))
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

    def fail(self):  # Метод поражения, выводит на экран надпись о проигрыше
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


def terminate():  # Полный выход
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):  # Загрузка изображения
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


class StartScreen:   # Заставка перед игрой
    pygame.display.set_caption('Война')

    def start(self):
        def start_screen():
            intro_text = ["В ПРОРЫВ!", "", ]

            fon = pygame.transform.scale(load_image('images/fon2.jpeg'), (WIDTH, HEIGHT))
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
            image = load_image('images/Apps launcher.png')
            sprite.image = pygame.transform.scale(image, (100, 40))
            sprite.rect = sprite.image.get_rect()
            all_sprites.add(sprite)
            sprite.rect.x = 80
            sprite.rect.y = 380
            sprite2 = pygame.sprite.Sprite()
            image1 = load_image('images/Apps launcher.png')
            sprite2.image = pygame.transform.scale(image1, (100, 40))
            sprite2.rect = sprite.image.get_rect()
            all_sprites.add(sprite2)
            sprite2.rect.x = 540
            sprite2.rect.y = 380

            clock = pygame.time.Clock()

            def provercapav(f):
                if 80 <= f[0] and 180 >= f[0] and 380 <= f[1] and 420 >= f[1]:
                    return True

            def provercapav2(f):
                if 540 <= f[0] and 640 >= f[0] and 380 <= f[1] and 420 >= f[1]:
                    return True

            while True:
                all_sprites.draw(screen)
                all_sprites.update()
                string_rendered2 = font.render('Играть', 1, pygame.Color('black'))
                intro_rect2 = string_rendered2.get_rect()
                intro_rect2.top = 390
                intro_rect2.x = 560
                screen.blit(string_rendered2, intro_rect2)
                string_rendered3 = font.render('Правила', 1, pygame.Color('black'))
                intro_rect3 = string_rendered2.get_rect()
                intro_rect3.top = 390
                intro_rect3.x = 90
                screen.blit(string_rendered3, intro_rect3)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for i in all_sprites:
                            i.kill()
                        if provercapav(event.pos):
                            return True
                        if provercapav2(event.pos):
                            return False

                pygame.display.flip()
                clock.tick(FPS)
        def level_screen():
            fon = pygame.transform.scale(load_image('images/fon3.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            clock = pygame.time.Clock()
            image = load_image('images/Apps launcher.png')
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.transform.scale(image, (80, 40))
            sprite.rect = sprite.image.get_rect()
            all_sprites.add(sprite)
            sprite.rect.x = 540
            sprite.rect.y = 380
            f = 0
            for i in range(3):
                sprite = pygame.sprite.Sprite()
                sprite.image = pygame.transform.scale(image, (160, 80))
                sprite.rect = sprite.image.get_rect()
                all_sprites.add(sprite)
                sprite.rect.x = 50 + f
                sprite.rect.y = 85
                f += 215
            f2 = 0
            for i in range(3):
                sprite = pygame.sprite.Sprite()
                sprite.image = pygame.transform.scale(image, (160, 80))
                sprite.rect = sprite.image.get_rect()
                all_sprites.add(sprite)
                sprite.rect.x = 50 + f2
                sprite.rect.y = 215
                f2 += 215

            string_rendered3 = font.render('Назад', 1, pygame.Color('black'))
            intro_rect3 = string_rendered3.get_rect()
            intro_rect3.top = 390
            intro_rect3.x = 550
            intro_text = ['1 уровень                   2 уровень                    3 уровень',
                          '4 уровень                   5 уровень                    6 уровень']
            def provercapav(f):
                if 540 <= f[0] and 620 >= f[0] and 380 <= f[1] and 420 >= f[1]:
                    return True

            def provercalevel(f):
                for i in range(3):
                    if 50 + i * 215 <= f[0] and 210 + i * 215 >= f[0] and 85 <= f[1] and 165 >= f[1]:
                        return i + 1
                for i in range(3):
                    if 50 + i * 215 <= f[0] and 210 + i * 215 >= f[0] and 85  + 130 <= f[1] and 165 + 130 >= f[1]:
                        return i + 4

            while True:
                all_sprites.draw(screen)
                all_sprites.update()
                screen.blit(string_rendered3, intro_rect3)
                text_coord = 0
                for line in intro_text:
                    string_rendered = font.render(line, 1, pygame.Color('black'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 110
                    intro_rect.top = text_coord
                    intro_rect.x = 80
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for i in all_sprites:
                            i.kill()
                        if provercapav(event.pos):
                            return False
                        g = provercalevel(event.pos)
                        if g:
                            return g

                pygame.display.flip()
                clock.tick(FPS)

        def rulscrin():
            intro_text = ["ПРАВИЛА",
                          "",
                          'Это тактическая игра.',
                          'Главная цель - уничтожить все юниты врага.',
                          'Дополнительные очки можно получить, завершив бой за',
                          'наименьшее кол-во ходов и сохранив как можно больше',
                          'здоровья у юнитов.',
                          'Управление: клик ПКМ по юниту выделит все возможные для',
                          'перемещения юнита клетки. Последующий клик ПКМ по одной',
                          'из выделенных клеток переместит юнит. Вместо перемещения',
                          'можно сделать выстрел нажатием ЛКМ по юниту. После этого под-',
                          'светятся все доступные для юнита цели.']
            fon = pygame.transform.scale(load_image('images/fon3.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 10
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            sprite = pygame.sprite.Sprite()
            image = load_image('images/Apps launcher.png')
            sprite.image = pygame.transform.scale(image, (80, 40))
            sprite.rect = sprite.image.get_rect()
            all_sprites.add(sprite)
            sprite.rect.x = 540
            sprite.rect.y = 380
            string_rendered3 = font.render('Назад', 1, pygame.Color('black'))
            intro_rect3 = string_rendered3.get_rect()
            intro_rect3.top = 390
            intro_rect3.x = 550

            def provercapav(f):
                if 540 <= f[0] and 620 >= f[0] and 380 <= f[1] and 420 >= f[1]:
                    return True


            clock = pygame.time.Clock()
            while True:
                all_sprites.draw(screen)
                all_sprites.update()
                screen.blit(string_rendered3, intro_rect3)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for i in all_sprites:
                            i.kill()
                        if provercapav(event.pos):
                            return True
                pygame.display.flip()
                clock.tick(FPS)
        while True:
            if not start_screen():
                k = level_screen()
                if k:
                    return k
                    break
            else:
                f = rulscrin()


class Loader:   # Класс-загрузчик, позволяет не писать длинные пути
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


# Загрузка картинок частиц
ldr = Loader()
parts = []
for imag in [ldr.load_particle('piece_1.png'), ldr.load_particle('piece_2.png'), ldr.load_particle('piece_3.png')]:
    for scal in (32, 35, 37):
        parts.append(pygame.transform.scale(imag, (scal, scal)))
PARTICLES = parts.copy()


class Unit(pygame.sprite.Sprite):  # Абстрактный класс игрового юнита
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

    def set_stats(self):  # Метод для переопределения у наследников
        pass

    def cut_sheet(self, sheet, columns, rows):  # Разрезает лист анимации на кадры
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):  # Смена кадра
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (SPRITE_SIDE, SPRITE_SIDE))

    def die(self, *groups):  # Уничтожение с вызовом частиц
        x_pos = self.rect.x
        y_pos = self.rect.y
        create_particles((x_pos, y_pos), 7, *groups)
        self.kill()

    def move(self, pos1, pos2):  # Передвижение
        self.rect.x = pos1
        self.rect.y = pos2


class Particle(pygame.sprite.Sprite):  # Класс частицы которая просто летит вниз
    def __init__(self, gravity, pos, dx, dy, *groups):
        super().__init__(*groups)
        self.image = random.choice(PARTICLES)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = gravity

    def update(self):  # Обновление с учетом гравитации
        self.velocity[1] += self.gravity  # Гравитация
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(SCREEN_RECT):
            self.kill()


def create_particles(position, particle_count, *groups):  # Метод, вызывающий частицы
    speeds_x = range(-10, 10)
    speeds_y = range(-15, -5)
    for _ in range(particle_count):
        Particle(1, position, random.choice(speeds_x), random.choice(speeds_y), *groups)


# Следующие 5 классов - наследники класса Unit, представляющие собой боевую технику
class Artillery(Unit):
    def __init__(self, x, y, is_enemy=False, *groups):
        if is_enemy:
            sheet = ldr.load_sprite_sheet('Artillery_1_enemy.png')
        else:
            sheet = ldr.load_sprite_sheet('Artillery_1.png')
        super().__init__(sheet, 4, 2, x, y, *groups)
        self.is_enemy = is_enemy

    def set_stats(self):
        self.health = 2
        self.attack = 2
        self.attack_range = 3
        self.speed = 2


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
        self.attack_range = 4
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
        self.health = 5
        self.attack = 2
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
        self.health = 4
        self.attack = 2
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
        self.health = 3
        self.attack = 1
        self.attack_range = 2
        self.speed = 4


class Tile(pygame.sprite.Sprite):  # Класс плитки
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

    def normal(self):   # Возврат плитки в стандартное состояние
        if self.kind != 'Mountain':
            self.image = pygame.transform.scale(ldr.load_tile('empty.png'), (self.tile_side, self.tile_side))

    def destroy(self):  # Переход плитки в багровую
        if self.kind != 'Mountain':
            self.image = pygame.transform.scale(ldr.load_tile('empty_destroyer.png'), (self.tile_side, self.tile_side))

    def target(self):  # Переход плитки в оранжевую
        if self.kind != 'Mountain':
            self.image = pygame.transform.scale(ldr.load_tile('empty_target.png'), (self.tile_side, self.tile_side))

    def move(self):  # Переход плитки в жёлтую
        if self.kind != 'Mountain':
            self.image = pygame.transform.scale(ldr.load_tile('empty_move.png'), (self.tile_side, self.tile_side))

    def tile_coords(self):  # Получение координат плитки
        return tuple([self.rect.x, self.rect.y])


class BattleField:  # Класс поля, внутри которого творится игра
    def __init__(self, cell_size, left_top, scr, tile_arr):
        self.data = [[None] * 10 for _ in range(10)]
        self.height = self.width = 10 * cell_size
        self.cell_size = cell_size
        self.left, self.top = left_top
        self.tiles_group = pygame.sprite.Group()
        self.units_group = pygame.sprite.Group()
        self.particles_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.atak = pygame.sprite.Group()
        self.own_surface = scr
        self.units_data = {}
        self.move = False
        self.attack = False
        self.hed1 = 0
        self.counter = 0
        self.turn = True
        self.exit = 0
        # Заполнение массива клеточками
        for line in range(len(tile_arr)):
            for column in range(len(tile_arr)):
                self.data[line][column] = Tile(tile_arr[line][column], cell_size,
                                               self.left + self.cell_size * column,
                                               self.top + self.cell_size * line,
                                               self.tiles_group, self.all_sprites)

    def render(self):  # Отрисовка
        self.all_sprites.draw(self.own_surface)
        self.atak.draw(self.own_surface)

    def normalize(self):  # Перевод всех клеточек в нормальное состояние
        for row in self.data:
            for tile in row:
                tile.normal()

    def tap_converter(self, tap_pos):  # Возвращает координаты клетки по координатам клика
        find_x = (tap_pos[0] - self.left) // self.cell_size
        find_y = (tap_pos[1] - self.top) // self.cell_size
        if find_x >= self.width or find_x < 0 or find_y >= self.height or find_y < 0:
            return None
        else:
            return tuple([find_x, find_y])

    def add_unit(self, unit_type, cell_x, cell_y, enemy=False):  # Добавление юнита на поле боя
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

    def tap_dispatcher(self, mouse_pos, type_of_press):  # Диспетчер кликов
        cell = self.tap_converter(mouse_pos)
        logic = cell and (cell in list(self.units_data.keys())) and not self.units_data[cell][0].is_enemy
        if type_of_press == 1 and not self.move and self.turn:  # Если нажата ЛКМ
            if self.attack:  # Если прицеливание выполнено, атака
                self.attacking(self.hed1, mouse_pos)
                self.attack = False
            elif logic:  # Если нет, то прицеливаться
                self.targeting(mouse_pos)
                self.attack = True
                self.hed1 = mouse_pos
        if type_of_press == 3 and not self.attack and self.turn:  # Если нажата ПКМ
            if self.move:  # Если показаны варианты хода, то двигаться
                self.moving(self.hed1, mouse_pos)
                self.move = False
            elif logic:  # Если нет, то показать
                self.move = True
                self.hed1 = mouse_pos
                self.mapping(mouse_pos)
        else:  # Если кликнули куда-то в другое место - сбросить показ вариантов движения
            self.move = False

    def mapping(self, mouse_pos):  # Раскраска клеток, на которые можно стать в жёлтые
        cell = self.tap_converter(mouse_pos)
        # Проверка на то, что в указанной клетке стоит дружественная техника
        if cell and (cell in list(self.units_data.keys()) and self.units_data[cell][1] == self.units_data[cell][2]):
            speed = self.units_data[cell][0].speed
            # Проходимся по всем клеткам в радиусе движения юнита и проверяем, свободна ли она
            for column in range(cell[0] - speed, cell[0] + speed + 1):
                for line in range(cell[1] - speed, cell[1] + speed + 1):
                    h = tuple([column, line])
                    if line < 0 or column < 0 or line > 9 or column > 9 or h == cell:
                        pass
                    else:
                        if h not in list(self.units_data.keys()):
                            self.data[line][column].move()

    def moving(self, pos1, pos2):  # Перемещает юнит на клетку
        self.normalize()
        cell1 = self.tap_converter(pos1)
        cell2 = self.tap_converter(pos2)
        if cell1 and cell2:  # Проверка того, что обе клетки на поле
            speed = self.units_data[cell1][0].speed
            pos_x = cell2[0] * self.cell_size + self.left
            pos_y = cell2[1] * self.cell_size + self.top
            # Проверка свободна ли клетка, куда хотят переместиться и того, что хотят переместить именно союзника
            if (cell2 not in list(self.units_data.keys())) and (
                    cell1 in list(self.units_data.keys()) and self.units_data[cell1][1] == self.units_data[cell1][2]) \
                    and max(abs(cell2[1] - cell1[1]), abs(cell2[0] - cell1[0])) <= speed and \
                    self.data[cell2[1]][cell2[0]].kind != 'Mountain':
                self.units_data[cell1][0].move(pos_x, pos_y)  # Передвигаем спрайт
                self.units_data[cell2] = self.units_data[cell1]  # Заводим новую позицию в словаре, а старую стираем
                del self.units_data[cell1]
                self.turn = False
                self.counter += 1
                self.ii_turn()  # Передаем ход ИИ

    def targeting(self, mouse_pos):   # Прицеливание
        self.normalize()  # Возвращаем все клетки в норму
        cell = self.tap_converter(mouse_pos)
        if cell and (cell in list(self.units_data.keys()) and self.units_data[cell][1] == self.units_data[cell][2]):
            speed = self.units_data[cell][0].attack_range
            # Перебираем все клетки и подсвечиваем врагов
            for column in range(cell[0] - speed, cell[0] + speed + 1):
                for line in range(cell[1] - speed, cell[1] + speed + 1):
                    h = tuple([column, line])
                    if line < 0 or column < 0 or line > 9 or column > 9 or h == cell:
                        pass
                    else:
                        if h in list(self.units_data.keys()) and self.units_data[h][0].is_enemy != \
                                self.units_data[cell][0].is_enemy:
                            self.data[line][column].target()
        self.data[cell[1]][cell[0]].destroy()   # Отмечаем самого стрелка

    def attacking(self, pos1, pos2):  # Атака
        self.normalize()  # Возвращаем все клетки в норму
        cell1 = self.tap_converter(pos1)
        cell2 = self.tap_converter(pos2)
        if cell1 and cell2 and cell1 != cell2:
            speed = self.units_data[cell1][0].attack_range
        # Проверка того, что друг атакует врага (не пустое место, не враг друга, не друг друга)
        if cell1 != cell2 and cell1 and cell2 and (cell2 in self.units_data.keys()) and \
                cell1 in list(self.units_data.keys()) and self.units_data[cell1][1] == self.units_data[cell1][2] \
                and max(abs(cell2[1] - cell1[1]), abs(cell2[0] - cell1[0])) <= speed and \
                self.units_data[cell1][0].is_enemy != \
                self.units_data[cell2][0].is_enemy:
            self.units_data[cell1][1] = 0
            self.units_data[cell2][0].health -= self.units_data[cell1][0].attack
            self.play_sound(self.units_data[cell1][0])
            self.turn = False
            self.counter += 1
            self.ii_turn()  # Передает ход ИИ

    def play_sound(self, unit):  # Проигрывает звук в зависимости от объекта, переданного ему
        if isinstance(unit, Cannon):
            cannon_sound.play()
        elif isinstance(unit, Artillery):
            artillery_sound.play()
        elif isinstance(unit, TankLarge):
            tank_large_sound.play()
        elif isinstance(unit, TankMedium):
            tank_medium_sound.play()
        elif isinstance(unit, TankSmall):
            tank_small_sound.play()

    def ii_turn(self):  # Ход ИИ
        self.update()
        if self.exit != 0:
            return
        enemies = []
        allies = []
        # Получает список врагов и союзников
        for key in list(self.units_data.keys()):
            if self.units_data[key][0].is_enemy:
                enemies.append(key)
            else:
                allies.append(key)
        flag = True
        # Проверяет, может ли по кому-нибудь попасть
        for enemy in enemies:
            for ally in allies:
                if max(abs(ally[0] - enemy[0]), abs(ally[1] - enemy[1])) <= self.units_data[enemy][0].attack_range:
                    self.ii_attack(enemy, ally)
                    flag = False
                    break
            if not flag:
                break
        # Если, нет то двигает рандомного
        if flag:
            try:
                self.ii_move(random.choice(enemies))
            except IndexError:  # Если врагов нет, то random вызывает IndexError
                for _ in range(30):
                    self.update()
                    self.render()
                    pygame.display.flip()
                    time.sleep(0.02)
                '''
                Подсчёт очков по критериям:
                1) За победу 10000 очков
                2) За каждого выжившего союзника 1000 очков
                3) -50 очков за каждый ход
                '''
                score = 10000 - self.counter * 50 + len(list(self.units_data.keys())) * 1000
                FinalScreen().win(score)
                terminate()
        self.turn = True

    def ii_attack(self, enemy, ally):  # Атака ИИ
        self.data[enemy[1]][enemy[0]].target()
        self.data[ally[1]][ally[0]].target()
        for _ in range(30):  # Пауза чтобы игрок заметил анимации/окраски клеток
            self.update()
            self.render()
            pygame.display.flip()
            time.sleep(0.02)
        self.normalize()
        self.play_sound(self.units_data[enemy][0])
        self.units_data[enemy][1] = 0
        self.units_data[ally][0].health -= self.units_data[enemy][0].attack

    def ii_move(self, enemy):  # Движение ИИ
        variants = []
        speed = self.units_data[enemy][0].speed
        # Проход по всем клеткам в радиусе движения
        for column in range(enemy[0] - speed, enemy[0] + speed + 1):
            for line in range(enemy[1] - speed, enemy[1] + speed + 1):
                h = tuple([column, line])
                if line < 0 or column < 0 or line > 9 or column > 9 or h == enemy:
                    pass
                else:
                    if h not in list(self.units_data.keys()) and self.data[line][column].kind != 'Mountain':
                        # Если клетка подходит, окрашиваем её и добавляем в список вариантов
                        self.data[line][column].move()
                        variants.append((column, line))
        # Пауза чтобы игрок заметил анимации/окраски клеток
        for _ in range(30):
            self.update()
            self.render()
            pygame.display.flip()
            time.sleep(0.02)
        self.normalize()
        try:  # Предохраняемся от IndexError в случае пустого списка
            pos = random.choice(variants)
            pos_x = pos[0] * self.cell_size + self.left
            pos_y = pos[1] * self.cell_size + self.top
            self.units_data[enemy][0].move(pos_x, pos_y)
            self.units_data[pos] = self.units_data[enemy]
            del self.units_data[enemy]
        except IndexError:
            pass

    def update(self):  # Обновление
        allies = 0
        if not self.move and not self.attack:  # Если ничего не происходит то нормализуем клеточки
            self.normalize()
        for key in list(self.units_data.keys()):
            # Подсчёт союзников
            if not self.units_data[key][0].is_enemy:
                allies += 1
            if self.units_data[key][0].health <= 0:
                self.units_data[key][0].die(self.particles_group, self.all_sprites)
                del self.units_data[key]
            elif self.units_data[key][1] < self.units_data[key][2]:
                self.units_data[key][1] += 1
                self.units_data[key][0].update()
        if allies == 0:
            self.exit += 1
        # Если союзников нет 35 кадров, выходим. (35 кадров для задержки, чтобы игрок успел осознать)
        if self.exit == 35:
            FinalScreen().fail()  # Экран поражения
            terminate()
        self.particles_group.update()


def load_game(map_name, surface):  # Загрузка игры из файла
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


try:
    d = StartScreen()
    mappy = d.start()
    # Расширение экрана для игры
    WIDTH, HEIGHT = 1000, 1000
    SCREEN_RECT = (0, 0, WIDTH, HEIGHT)
    screen_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Война')
    all_sprites = pygame.sprite.Group()
    field = load_game('map_' + str(mappy), screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                field.tap_dispatcher(event.pos, event.button)
        field.update()
        try:
            screen.fill((0, 0, 0))
        except pygame.error:
            terminate()
        field.render()
        clock.tick(FPS)
        pygame.display.flip()
    terminate()
except Exception:
    terminate()
