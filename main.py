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

            def provercapav(f):
                if 540 <= f[0] and 620 >= f[0] and 380 <= f[1] and 420 >= f[1]:
                    return True

            clock = pygame.time.Clock()
            while True:
                all_sprites.draw(screen)
                all_sprites.update()
                string_rendered3 = font.render('Назад', 1, pygame.Color('black'))
                intro_rect3 = string_rendered3.get_rect()
                intro_rect3.top = 390
                intro_rect3.x = 550
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
                break
            else:
                f = rulscrin()
d = startscreen
d.start()
