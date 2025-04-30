import pygame
import os
from pygame.locals import *
import sys
from connecting import loading_maps, save_results

pygame.init()
FPS = 50
clock = pygame.time.Clock()
running_main = True
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

white = (255, 255, 255)
black = (31, 31, 31)
yellow = (245, 234, 83)
green = (113, 212, 72)
blue = (72, 156, 212)
red = (212, 72, 72)
stand = (207, 207, 207)
color_cont = {'R': red, 'G': green, 'B': blue, 'S': stand}

all_maps, map_id, map_name, map_texture = [], 0, '', ''  # данные текущей игровой карты


def load_level(texture):
    level_map = [line.strip().split('-') for line in texture.split('\n')]
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


def update_maps():
    global all_maps, map_id, map_name, map_texture
    all_maps = loading_maps()
    for maps in all_maps:
        if maps['status'] == 0:
            map_texture = maps['texture']
            map_id = maps['id']
            map_name = maps['name']
            break


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
        self.opp_move = True
        self.coll_stars = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, direct):  # перемешение игрока по карте
        if direct == 'right':
            self.image = pygame.transform.rotate(self.image, -90)
            self.directing = (self.directing + 1) % 4
        if direct == 'left':
            self.image = pygame.transform.rotate(self.image, 90)
            self.directing = (self.directing - 1) % 4
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
            self.opp_move = False
        if pygame.sprite.spritecollideany(self, stars_group):  # если коснулся звезды
            self.coll_stars += 1  # добавляем звезду в счёт
            for name in stars_group:  # перебор всех обьектов группы Stars
                name.checkout()


class Star(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(stars_group, all_sprites)
        self.image = star_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def checkout(self):
        if pygame.sprite.spritecollideany(self, player_group):  # если коснулась игрока
            Star.kill(self)


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level):
    new_player, x, y, stars = None, None, None, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x][0] == 'R':
                Road(x, y, color_cont[level[y][x][1]])
                if len(level[y][x]) > 2:
                    if level[y][x][2] == 'P':
                        new_player = Player(x, y)
                    if level[y][x][-1] == '*':
                        stars += 1
                        Star(x, y)
            elif level[y][x] == '#':
                Void(x, y)
    return new_player, x, y, stars


player = None
all_sprites = pygame.sprite.Group()
road_group = pygame.sprite.Group()
void_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()
all_stars_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def del_all_spr():
    for sprite in all_sprites:
        sprite.kill()  # Удаляет спрайт из всех групп


def start_screen():
    update_maps()
    screen_width = 700
    screen_height = 450
    screen = pygame.display.set_mode((screen_width, screen_height))
    fon = pygame.transform.scale(load_image('fon.jpg'), (screen_width, screen_height))
    screen.blit(fon, (0, 0))
    pygame.display.set_caption("CyberStep v1.0")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        start_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 - 50, 150, 50)
        pygame.draw.rect(screen, green if start_button_rect.collidepoint(mouse_pos) else white, start_button_rect)
        text_start = font.render('Начать', True, black)
        screen.blit(text_start, (start_button_rect.centerx - text_start.get_width() // 2,
                                 start_button_rect.centery - text_start.get_height() // 2))

        settings_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 10, 150, 50)
        pygame.draw.rect(screen, yellow if settings_button_rect.collidepoint(mouse_pos) else white,
                         settings_button_rect)
        text_settings = font.render('Редактор', True, black)
        screen.blit(text_settings, (settings_button_rect.centerx - text_settings.get_width() // 2,
                                    settings_button_rect.centery - text_settings.get_height() // 2))

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
    player, level_x, level_y, star_on_map = generate_level(load_level(map_texture))
    SIZE = width, height = 700, 500
    screen = pygame.display.set_mode(SIZE)
    running_game = True
    while running_game:
        screen.fill((0, 0, 0))

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        map_name_text = small_font.render(f'Карта: {map_name}', True, white)
        screen.blit(map_name_text, (530, 430))

        back_but = pygame.Rect(520, 40, 150, 50)
        pygame.draw.rect(screen, green if back_but.collidepoint(mouse_pos) else white, back_but)
        text_back = font.render('Назад', True, black)
        screen.blit(text_back, (back_but.centerx - text_back.get_width() // 2,
                                back_but.centery - text_back.get_height() // 2))

        restart_but = pygame.Rect(520, 120, 150, 50)
        pygame.draw.rect(screen, green if restart_but.collidepoint(mouse_pos) else white, restart_but)
        text_rest = font.render('Рестарт', True, black)
        screen.blit(text_rest, (restart_but.centerx - text_rest.get_width() // 2,
                                restart_but.centery - text_rest.get_height() // 2))

        if player.coll_stars == star_on_map:
            save_results(map_id)
            player.opp_move = False
            next_but = pygame.Rect(520, 200, 150, 50)
            pygame.draw.rect(screen, green if next_but.collidepoint(mouse_pos) else white, next_but)
            text_next = font.render('Следующая', True, black)
            screen.blit(text_next, (next_but.centerx - text_next.get_width() // 2,
                                    next_but.centery - text_next.get_height() // 2))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running_game = False
                del_all_spr()
            if player.opp_move:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.move('left')
                    if event.key == pygame.K_RIGHT:
                        player.move('right')
                    if event.key == pygame.K_UP:
                        player.move('go')
                    if event.key == pygame.K_DOWN:
                        pass
            if click[0]:
                if back_but.collidepoint(mouse_pos):
                    running_game = False
                    del_all_spr()
                if restart_but.collidepoint(mouse_pos):
                    del_all_spr()
                    play_game()
                    return None
                if not player.opp_move:
                    if next_but.collidepoint(mouse_pos):
                        update_maps()
                        del_all_spr()
                        play_game()
                        return None

        if not player.opp_move and player.coll_stars != star_on_map:
            if player.image.get_width() < 100:
                player.image = pygame.transform.scale(player.image,
                                                      (player.image.get_width() * 0.99,
                                                       player.image.get_height() * 0.99))
                player.image = pygame.transform.rotate(player.image, 3)
                clock.tick(100)
            else:
                player.kill()
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.update()
        player_group.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    while running_main:
        start_screen()
        play_game()
