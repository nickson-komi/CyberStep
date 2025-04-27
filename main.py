import pygame
import os
from pygame.locals import *
import sys

pygame.init()
FPS = 50
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (31, 31, 31)
yellow = (245, 234, 83)
green = (113, 212, 72)
blue = (72, 156, 212)
red = (212, 72, 72)
stand = (207, 207, 207)
color_cont = {'R': red, 'G': green, 'B': blue, 'S': stand}


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip().split('-') for line in mapFile]
    return level_map


def create_image(width, color):
    image = pygame.Surface([width, width])
    image.fill(color)
    pygame.draw.line(image, tuple(255 if x * 1.25 > 255 else x * 1.25 for x in color),
                     (0, 0), (0 + width * 0.99, 0), int(width * 0.05))
    pygame.draw.line(image, tuple(255 if x * 1.25 > 255 else x * 1.25 for x in color), (0, 0), (0 + width * 0.99, 0),
                     int(width * 0.05))
    pygame.draw.line(image, tuple(255 if x * 1.25 > 255 else x * 1.25 for x in color), (0, 0), (0, 0 + width * 0.99),
                     int(width * 0.05))
    pygame.draw.line(image, tuple(x * 0.75 for x in color), (0 + width * 0.99, 0),
                     (0 + width * 0.99, 0 + width * 0.99), int(width * 0.05))
    pygame.draw.line(image, tuple(x * 0.75 for x in color), (0, 0 + width * 0.99),
                     (0 + width * 0.99, 0 + width * 0.99), int(width * 0.05))
    return image


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # image = pygame.transform.rotate(image, 90)

    # if colorkey is not None:
    # image = image.convert()
    # if colorkey == -1:
    # colorkey = image.get_at((0, 0))
    # image.set_colorkey(colorkey)
    # else:
    # image = image.convert_alpha()
    return image


tile_width = tile_height = 50
void_image = create_image(tile_width, black)  # плитка пустого поля
player_image = load_image('player.png')
star_image = load_image('star.png')


class Road(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color):
        super().__init__(road_group, all_sprites)
        self.image = create_image(tile_width, color)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Void(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(void_group, all_sprites)
        self.image = void_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direct=0):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.directing = direct
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, direct):  # перемешение игрока по карте
        if direct == 'right':
            self.image = pygame.transform.rotate(self.image, -90)
            self.directing = (self.directing + 1) % 4
        if direct == 'left':
            self.image = pygame.transform.rotate(self.image, 90)
            self.directing = (self.directing - 1) % 4
        # old_x, old_y = (player.rect[:2])
        if direct == 'go':
            if self.directing == 0:
                x, y = 1, 0
            if self.directing == 1:
                x, y = 0, 1
            if self.directing == 2:
                x, y = -1, 0
            if self.directing == 3:
                x, y = 0, -1
            self.rect.x += x * tile_width
            self.rect.y += y * tile_height

        if pygame.sprite.spritecollideany(self, void_group):  # если коснулся пустоты
            print('dsdf')
        if pygame.sprite.spritecollideany(self, stars_group):  # если коснулся звезды
            for name in stars_group:  # перебор всех обьектов группы Stars
                name.checkout()


class Star(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(stars_group, all_sprites)
        self.image = star_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def checkout(self):
        if pygame.sprite.spritecollideany(self, player_group):  # если коснулся игрока
            Star.kill(self)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x][0] == 'R':
                Road(x, y, color_cont[level[y][x][1]])
                if len(level[y][x]) > 2:
                    if level[y][x][2] == 'P':
                        new_player = Player(x, y)
                    if level[y][x][-1] == '*':
                        Star(x, y)
            elif level[y][x] == '#':
                Void(x, y)
    return new_player, x, y


player = None
all_sprites = pygame.sprite.Group()
road_group = pygame.sprite.Group()
void_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()
all_stars_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def start_screen():
    screen_width = 700
    screen_height = 450
    screen = pygame.display.set_mode((screen_width, screen_height))
    fon = pygame.transform.scale(load_image('fon.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    pygame.display.set_caption("CyberStep v1.0")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Кнопка 'Начать'
        start_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 - 50, 150, 50)
        pygame.draw.rect(screen, green if start_button_rect.collidepoint(mouse_pos) else white, start_button_rect)
        font = pygame.font.SysFont(None, 36)
        text_start = font.render('Начать', True, black)
        screen.blit(text_start, (start_button_rect.centerx - text_start.get_width() // 2,
                                 start_button_rect.centery - text_start.get_height() // 2))

        # Кнопка 'Редактор' (неактивная пока)
        settings_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 10, 150, 50)
        pygame.draw.rect(screen, yellow if settings_button_rect.collidepoint(mouse_pos) else white,
                         settings_button_rect)
        text_settings = font.render('Редактор', True, black)
        screen.blit(text_settings, (settings_button_rect.centerx - text_settings.get_width() // 2,
                                    settings_button_rect.centery - text_settings.get_height() // 2))

        # Кнопка 'Выход'
        exit_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 70, 150, 50)
        pygame.draw.rect(screen, red if exit_button_rect.collidepoint(mouse_pos) else white, exit_button_rect)
        text_exit = font.render('Выход', True, black)
        screen.blit(text_exit, (
            exit_button_rect.centerx - text_exit.get_width() // 2,
            exit_button_rect.centery - text_exit.get_height() // 2))

        if click[0]:
            if start_button_rect.collidepoint(mouse_pos):
                return
            elif exit_button_rect.collidepoint(mouse_pos):
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def play_game():
    SIZE = width, height = 700, 700
    screen = pygame.display.set_mode(SIZE)
    screen.fill((0, 0, 0))
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move('left')
                if event.key == pygame.K_RIGHT:
                    player.move('right')
                if event.key == pygame.K_UP:
                    player.move('go')
                if event.key == pygame.K_DOWN:
                    pass

        all_sprites.update()
        all_sprites.draw(screen)
        player_group.update()
        player_group.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    player, level_x, level_y = generate_level(load_level('map2.txt'))
    play_game()
