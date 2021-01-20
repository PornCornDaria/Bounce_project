import pygame

# инициалилзируем pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

# параметры окна
tile_size = 50
cols = 14
margin = 100
screen_width = 1750
screen_height = (tile_size * cols) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

# загрузка тектсур
ring = pygame.image.load('assets/ring_active.png')
wall = pygame.image.load('assets/wall.png')
spike1 = pygame.image.load('assets/spike.png')
spike2 = pygame.image.load('assets/thatweirdthing.png')
door = pygame.image.load('assets/door_open.png')
save_img = pygame.image.load('assets/save_btn.png')

# внутриигровые переменные
clicked = False
level_num = 1

# цвета
white = (255, 255, 255)

font = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold',
                           30)

# пустой список с клетками
world_data = []
for row in range(14):
    r = [0] * 35
    world_data.append(r)
# границы карты
for tile in range(14):
    world_data[tile][0] = 1
    world_data[tile][-1] = 1

for tile in range(35):
    world_data[-1][tile] = 1
    world_data[0][tile] = 1


# вывод текста на экран
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# отрисовываем сетку
def draw_grid():
    for c in range(35):
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
    for r in range(15):
        pygame.draw.line(screen, white, (0, r * tile_size), (screen_width, r * tile_size))


# отрисовываем мир
def draw_world():
    for row in range(14):
        for col in range(35):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    # стенка
                    img = pygame.transform.scale(wall, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))

                if world_data[row][col] == 2:
                    # шипы (движущиеся)
                    img = pygame.transform.scale(spike2, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))

                if world_data[row][col] == 3:
                    # шипы
                    img = pygame.transform.scale(spike1, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))

                if world_data[row][col] == 4:
                    # кольца
                    img = pygame.transform.scale(ring, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))

                if world_data[row][col] == 5:
                    # дверь
                    img = pygame.transform.scale(door, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))


# класс кнопки
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
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
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# create load and save buttons
save_button = Button(screen_width // 2, screen_height - 80, save_img)

# main game loop
run = True
while run:

    clock.tick(fps)

    # draw background
    screen.fill((80, 217, 254))

    # load and save level
    if save_button.draw():
        # save level data
        f = open(f'levels/lvl{level_num}.txt', 'w')
        for row in world_data:
            string = [str(num) for num in row]
            string = ''.join(string)
            f.write(string)
            f.write('\n')
        f.close()

    # show the grid and draw the level tiles
    draw_grid()
    draw_world()

    # text showing current level
    draw_text(f'Level: {level_num}', font, white, tile_size, screen_height - 80)
    draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # mouseclicks to change tiles
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            # check that the coordinates are within the tile area
            if x < 35 and y < 14:
                # update tile value
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > 5:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 5
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        # up and down key presses to change level number
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level_num += 1
            elif event.key == pygame.K_DOWN and level_num > 1:
                level_num -= 1

    # update game display window
    pygame.display.update()

pygame.quit()
