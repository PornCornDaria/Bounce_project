import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bounce 2.0')

tile_size = 50
game_over = 0
main_menu = True

sky_color = (80, 217, 254)
restart_img = pygame.image.load('assets/restart_btn.png')
start_img = pygame.image.load('assets/start_btn.png')
exit_img = pygame.image.load('assets/exit_btn.png')
start_screen = pygame.image.load('assets/start_screen.png')
game_over_screen_img = pygame.image.load('assets/game_over.png')
game_over_screen = pygame.transform.scale(game_over_screen_img, (800, 500))

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Player:
    def __init__(self, x, y):
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
        for tile in world.tile_list:
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

            if pygame.sprite.spritecollide(self, spike_group, False):
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


class World:
    def __init__(self, data):
        self.tile_list = []

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
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        spike_img = pygame.image.load('assets/spike.png')
        self.image = pygame.transform.scale(spike_img, (30, 48))
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


def load_level(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    level = []
    for row in data:
        level.append(list(row))
    return level


player = Player(50, screen_height - 130)

spike_group = pygame.sprite.Group()

world = World(load_level('levels/lvl1'))

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
            run = False
        if start_button.draw():
            main_menu = False

    else:
        screen.fill(sky_color)
        world.draw()

        spike_group.draw(screen)

        if game_over == 0:
            spike_group.update()

        game_over = player.update(game_over)

        if game_over == -1:
            screen.fill(sky_color)
            screen.blit(game_over_screen, (100, -100))
            if restart_button.draw():
                player.reset(100, screen_height - 130)
                game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
