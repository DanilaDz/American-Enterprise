import pygame
import math

colorkey = (0, 0, 0)


def set_global_colorkey(key: int):
    global colorkey
    colorkey = key


def load_map(path):
    with open(path + '.txt', 'r') as map_file:
        data = map_file.read()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


animation_frames = {}


def load_animations(path, frame_durations):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((0, 0, 0))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def collision_test(rect, tiles):
    collision_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            collision_list.append(tile)
    return collision_list


def collision_move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    collision_list = collision_test(rect, tiles)
    for tile in collision_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    collision_list = collision_test(rect, tiles)
    for tile in collision_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def flip_img(img, boolean, boolean_2):
    return pygame.transform.flip(img, boolean, boolean_2)


class Entity:
    def __init__(self, x, y, size_x, size_y, health, e_type):  # x, y, size_x, size_y, type
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.image = None
        self.animation_frame = 0
        self.flip = False
        self.type = e_type
        self.action = 'idle'
        self.health = health

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def move(self, rect, movement, tiles):
        r, collisions = collision_move(rect, movement, tiles)
        return r, collisions

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def set_flip(self, boolean):
        self.flip = boolean

    def change_action(self, new_value):
        if self.action != new_value:
            self.action = new_value
            self.animation_frame = 0
        return self.action, self.animation_frame

    def get_animation_image(self, animation_database):
        self.animation_frame += 1
        if self.animation_frame >= len(animation_database[self.action]):
            self.animation_frame = 0
        img_id = animation_database[self.action][self.animation_frame]
        image = animation_frames[img_id]
        return image


class Gun:
    def __init__(self, gun_img, x, y, bullets, flip, surf, scroll=None, mx=None, my=None):
        self.x = x
        self.y = y
        self.bullets = bullets
        self.mx = mx
        self.my = my
        self.scroll = scroll
        self.gun_img = gun_img
        self.flip = flip
        self.surf = surf
        self.surf_x = int(self.surf.get_width() / 2)
        self.surf_y = int(self.surf.get_height() / 2)
        self.gun_pos = [self.x - self.scroll[0], self.y - self.scroll[1]]

    def draw_mouse_gun(self):
        rot = -math.degrees(
            math.atan2(self.my - (int(self.y) - self.scroll[1]), self.mx - (int(self.x) - self.scroll[0])))
        self.surf.blit(pygame.transform.rotate(flip_img(self.gun_img, False, self.flip), rot), self.gun_pos[0] - self.surf_x,
                       self.gun_pos[1] - self.surf_y)


class Button:
    def __init__(self, x, y, width, height, font, font_color, text=''):
        self.color = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.font_color = font_color

    def draw(self, win, alpha_color=()):
        rect = (self.x, self.y, self.width, self.height)
        if alpha_color != ():
            self.color = alpha_color
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.color, shape_surf.get_rect())
        win.blit(shape_surf, rect)

        if self.text != '':
            text = self.font.render(self.text, True, self.font_color)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
