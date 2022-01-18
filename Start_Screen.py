
import pygame
import os
import sys

size = width, height = 700, 500
screen = pygame.display.set_mode(size)
FPS = 50
pygame.init()
pygame.key.set_repeat(200, 70)
all_sprites = pygame.sprite.Group()
text_sprites = pygame.sprite.Group()

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

class startscreen:
    def start(self):
        def start_screen():
            intro_text = ["ЗАСТАВКА", "", ]

            fon = pygame.transform.scale(load_image('images/fon2.jpeg'), (width, height))
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
            fon = pygame.transform.scale(load_image('images/fon3.png'), (width, height))
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
                          'В каждой битве случайно выбирается одна из нескольких',
                          'карт, дополнительная и основная задача.',
                          'Чем больше вы сохраните воинов в конце боя,',
                          'чем целее они будут, выполнили ли вы дополнительную',
                          'задачу, модификатор вашего уровня сложности, всё это',
                          'скажется на вашем результате.']
            fon = pygame.transform.scale(load_image('images/fon3.png'), (width, height))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50
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
                    print(k)
                    break
            else:
                f = rulscrin()
d = startscreen()
d.start()
