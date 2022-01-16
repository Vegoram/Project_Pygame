from library import *


pygame.init()
screen_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screen_size)
FPS = 40
clock = pygame.time.Clock()
pygame.display.set_caption('Стрельботня')
all_sprites = pygame.sprite.Group()
field = load_game('test_map', screen)
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
        print('Победа!')
        terminate()
    field.render()
    clock.tick(FPS)
    pygame.display.flip()
terminate()

