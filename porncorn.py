import pygame
from os import listdir

# инициализируем pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

# параметры экрана
screen_width = 1750
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bounce 2.0')

# шрифт
font_score = \
    pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 30)
text_color = (255, 255, 255)

# звуки
ring_sound = pygame.mixer.Sound('sounds/ring_sound_2.mp3')
enemy_sound = pygame.mixer.Sound('sounds/enemy.mp3')

# параметры игры
tile_size = 50
game_over = 0
main_menu = True
level_num = 1
max_levels = len(listdir('levels'))
score = 0

# цвет
sky_color = (80, 217, 254)

# текстуры
restart_img = pygame.image.load('assets/restart_btn.png')
start_img = pygame.image.load('assets/start_btn.png')
exit_img = pygame.image.load('assets/exit_btn.png')
start_screen = pygame.image.load('assets/start_screen.png')


# функция сброса уровня
def reset_level(level_num):
    player.reset(100, screen_height - 130)
    spike_group.empty()
    ring_group.empty()
    door_group.empty()
    # считываем файл с уровнем
    f = open(f'levels/lvl{level_num}.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    level = []
    for row in data:
        level.append(list(row))
    world = World(level, all_rings)

    return world


# отрисовываем текст
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


# класс кнопок
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # считываем координаты мыши
        pos = pygame.mouse.get_pos()

        # проверка наведение и нажатие
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # отрисовка кнопки
        screen.blit(self.image, self.rect)

        return action


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.reset(x, y)
        self.count = 1

    # обновление координат и состояний игрока
    def update(self, game_over):
        dx = 0
        dy = 0
        # считывание нажатий клавиш
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.on_the_ground:
                self.vel_y = -15
            if not key[pygame.K_UP]:
                self.jumped = False
                self.on_the_ground = False
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5
        self.on_the_ground = False

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # проверка на коллизии
        for tile in world.tile_list:
            # проверка на коллизии в оси x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # проверка на коллизии в оси у
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.on_the_ground = True

        # обновление координат
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        elif game_over == -1:
            self.image = self.dead_image
        # draw player onto screen
        screen.blit(self.image, self.rect)

        return game_over

    # сброс при проигрыше
    def reset(self, x, y):
        img = pygame.image.load('assets/ball.png')
        dead_img = pygame.image.load('assets/pop.png')
        self.image = pygame.transform.scale(img, (40, 40))
        self.dead_image = pygame.transform.scale(dead_img, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.on_the_ground = True


all_rings = 0


# класс карты
class World(pygame.sprite.Sprite):
    def __init__(self, data, rings_amount, *groups):
        super().__init__(*groups)
        self.tile_list = []
        self.rings_amount = rings_amount
        wall_img = pygame.image.load('assets/wall.png')

        # считывание уровня
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == '1':
                    img = pygame.transform.scale(wall_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == '2':
                    spike2 = Enemy2(col_count * tile_size, row_count * tile_size + 5)
                    spike_group.add(spike2)

                if tile == '3':
                    spike = Enemy(col_count * tile_size, row_count * tile_size + 5)
                    spike_group.add(spike)

                if tile == '4':
                    self.rings_amount += 1
                    ring = Ring(col_count * tile_size, row_count * tile_size + 10)
                    ring_group.add(ring)

                if tile == '5':
                    door = Door(col_count * tile_size, row_count * tile_size + 15)
                    door_group.add(door)

                col_count += 1
            row_count += 1

    # отрисовка уровня
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# спрайт врага (шипы)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/spike.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# спрайт врага 2 (движущиеся шипы)
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spike2_img = pygame.image.load('assets/thatweirdthing.png')
        self.image = pygame.transform.scale(spike2_img, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    # движение шипов
    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


# спрайт колец
class Ring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/ring_active.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size + 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


# иконка кольца
class RingIcon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/ring_active.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, (tile_size + 30) // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


# спрайт двери
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/door_open.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size + 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


player = Player(50, screen_height - 130)

# группирем спрайты
spike_group = pygame.sprite.Group()
ring_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()

# иконка кольца
ring_icon = RingIcon(tile_size // 2, tile_size // 2)
ring_group.add(ring_icon)

# считываем уровней
f = open(f'levels/lvl{level_num}.txt', 'r')
data = f.read()
f.close()
data = data.split('\n')
level = []
for row in data:
    level.append(list(row))
world = World(level, all_rings)

# отрисовка кнопок
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 + 100, 200, start_img)
exit_button = Button(screen_width // 2 - 30 + 150, 400, exit_img)

# игровой цикл
running = True
while running:

    clock.tick(fps)

    if main_menu:
        screen.fill(sky_color)
        screen.blit(start_screen, (0, 100))
        if exit_button.draw():
            running = False
        if start_button.draw():
            main_menu = False

    else:
        screen.fill(sky_color)
        world.draw()

        if game_over == 0:
            spike_group.update()
            ring_group.update()
            door_group.update()

        # проверка на сбор колец
        if pygame.sprite.spritecollide(player, ring_group, True):
            ring_sound.play()
            score += 1
        draw_text(f'x: {score}/{world.rings_amount}', font_score, text_color, 45, 15)

        if pygame.sprite.spritecollide(player, spike_group, True):
            enemy_sound.play()
            game_over = -1

        if score == world.rings_amount:
            if pygame.sprite.spritecollide(player, door_group, True):
                game_over = 1

        # отрисовка спрайтов
        spike_group.draw(screen)
        ring_group.draw(screen)
        door_group.draw(screen)

        game_over = player.update(game_over)

        if game_over == -1:
            spike_group = pygame.sprite.Group()
            screen.fill(sky_color)
            if restart_button.draw():
                player.reset(100, screen_height - 130)

                f = open(f'levels/lvl{level_num}.txt', 'r')
                data = f.read()
                f.close()
                data = data.split('\n')
                level = []
                for row in data:
                    level.append(list(row))
                world = World(level, all_rings)

                game_over = 0
                score = 0
                row_count = 0

                for row in level:
                    col_count = 0
                    for tile in row:
                        if tile == 2:
                            spike2 = Enemy2(col_count * tile_size, row_count * tile_size + 5)
                            spike_group.add(spike2)
                        if tile == 4:
                            spike = Enemy(col_count * tile_size, row_count * tile_size + 5)
                            spike_group.add(spike)
                        if tile == 5:
                            ring = Ring(col_count * tile_size, row_count * tile_size + 10)
                            ring_group.add(ring)
                        if tile == 6:
                            door = Door(col_count * tile_size, row_count * tile_size + 15)
                            door_group.add(door)

                        col_count += 1
                    row_count += 1

        if game_over == 1:
            score = 0
            screen.fill(sky_color)
            # переход на следующий уровень
            level_num += 1
            if level_num <= max_levels:
                # сброс уровня
                level = []
                world = reset_level(level_num)
                game_over = 0
            else:
                if restart_button.draw():
                    level_num = 1
                    # сброс уровня до 1
                    level = []
                    world = reset_level(level_num)
                    game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
