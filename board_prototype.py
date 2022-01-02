from library import *


pygame.init()
screen_size = (1000, 1000)
screen = pygame.display.set_mode(screen_size)
FPS = 40
clock = pygame.time.Clock()
pygame.display.set_caption('Стрельботня')
all_sprites = pygame.sprite.Group()
field = BattleField('test_map', 90, (50, 50), screen)
field.add_unit('Cannon', 0, 0)
field.add_unit('TankSmall', 7, 2, True)
field.add_unit('Artillery', 3, 3)
field.add_unit('Cannon', 9, 9, True)
field.add_unit('TankSmall', 4, 5)
field.add_unit('TankLarge', 2, 8)
field.add_unit('TankMedium', 1, 1, True)
field.render()
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            field.tap_dispatcher(event.pos)
    field.update()
    field.render()
    clock.tick(FPS)
    pygame.display.flip()
terminate()
