import pygame
from pygame.locals import *
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bounce 2.0')

font_score = pygame.font.SysFont(
    'sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 30)
text_color = (255, 255, 255)

ring_sound = pygame.mixer.Sound('sounds/ring_sound_2.mp3')
enemy_sound = pygame.mixer.Sound('sounds/enemy.mp3')


tile_size = 50
game_over = 0
main_menu = True
level_count = 0
all_rings_collected = False

sky_color = (80, 217, 254)
game_over_screen_img = pygame.image.load('assets/game_over.png')
game_over_screen = pygame.transform.scale(game_over_screen_img, (800, 500))
restart_img = pygame.image.load('assets/restart_btn.png')
start_img = pygame.image.load('assets/start_btn.png')
exit_img = pygame.image.load('assets/exit_btn.png')
start_screen = pygame.image.load('assets/start_screen.png')

score = 0
level = 1


def load_level(file_path):
    f = open(file_path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    level = []
    for row in data:
        level.append(list(row))
    return level


def reset_level(level_count):
    player.reset(100, screen_height - 130)

    if path.exists(f'level{level_count}_data'):
        world = World(load_level(f'assets/lvl{level_count}.txt'), all_rings)
        return world


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.score = score

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.reset(x, y)
        self.count = 1

    def update(self, game_over):
        dx = 0
        dy = 0

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
        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision
        for tile in world1.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.on_the_ground = True

        if pygame.sprite.spritecollide(player, spike_group, False):
            enemy_sound.play()
            game_over = -1
        # update player coordinates
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


class World(pygame.sprite.Sprite):
    def __init__(self, data, rings_amount, *groups):
        super().__init__(*groups)
        self.tile_list = []
        self.rings_amount = rings_amount
        wall_img = pygame.image.load('assets/wall.png')
        wall_half_img = pygame.image.load('assets/wall_half.png')
        ring_active_img = pygame.image.load('assets/ring_active.png')
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
                    img = pygame.transform.scale(wall_half_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == '3':
                    img = pygame.transform.scale(ring_active_img, (tile_size, tile_size + 100))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                if tile == '4':
                    spike = Enemy(col_count * tile_size, row_count * tile_size + 5)
                    spike_group.add(spike)

                if tile == '5':
                    spike2 = Enemy2(col_count * tile_size, row_count * tile_size - 75)
                    spike_group.add(spike2)

                if tile == '6':
                    self.rings_amount += 1
                    ring = Ring(col_count * tile_size, row_count * tile_size + 10)
                    ring_group.add(ring)

                if tile == '7':
                    door = Door(col_count * tile_size, row_count * tile_size + 15)
                    door_group.add(door)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/spike.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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

    def update(self):
        self.rect.y += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Ring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/ring_active.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size + 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class RingIcon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/ring_active.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, (tile_size + 30) // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/door_open.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size + 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - screen_width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - screen_height // 2)


player = Player(50, screen_height - 130)

spike_group = pygame.sprite.Group()
ring_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
ring_icon = RingIcon(tile_size // 2, tile_size // 2)
ring_group.add(ring_icon)
world1 = World(load_level('levels/lvl1'), all_rings)


camera = Camera()

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 + 100, 175, start_img)
exit_button = Button(screen_width // 2 - 30 + 150, 350, exit_img)

running = True
while running:

    clock.tick(fps)

    if main_menu:
        screen.fill(sky_color)
        screen.blit(start_screen, (0, 0))
        if exit_button.draw():
            running = False
        if start_button.draw():
            main_menu = False

    else:
        screen.fill(sky_color)
        world1.draw()

        if game_over == 0:
            spike_group.update()
            ring_group.update()

        if pygame.sprite.spritecollide(player, ring_group, True):
            score += 1
            ring_sound.play()
        draw_text(f'{score}/{world1.rings_amount}', font_score, text_color, 45, 10)

        spike_group.draw(screen)
        ring_group.draw(screen)
        door_group.draw(screen)

        game_over = player.update(game_over)

        if game_over == -1:
            screen.fill(sky_color)
            screen.blit(game_over_screen, (100, -100))
            if restart_button.draw():
                player.reset(100, screen_height - 130)
                game_over = 0
                score = 0
                row_count = 0
                reset_level(level_count)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
