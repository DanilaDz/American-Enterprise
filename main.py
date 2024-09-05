import pygame
import sys
import os
import engine
import random
import time

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

# =========================Initialization of images, fonts, etc.=========================

pygame.display.set_caption('American Enterprise')

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display = pygame.Surface((600, 400))
icon = pygame.image.load("images/icon.png")
icon.set_colorkey((255, 255, 255))
pygame.display.set_icon(icon)

tfont = pygame.font.Font('fonts/titlefont.otf', 60)
font = pygame.font.Font('fonts/titlefont.otf', 36)
sfont = pygame.font.Font('fonts/titlefont.otf', 24)
vsfont = pygame.font.Font('fonts/titlefont.otf', 17)
stock_font = pygame.font.Font('fonts/font.ttf', 14)

white = (255, 255, 255)

sfx_button = engine.Button(display.get_width() // 2 - 100 // 2, 100, 100, 25, sfont, (0, 0, 0), 'SFX: On')
music_button = engine.Button(display.get_width() // 2 - 130 // 2, 160, 130, 25, sfont, (0, 0, 0), 'Music: On')
speech_button = engine.Button(display.get_width() // 2 - 130 // 2, 220, 145, 25, sfont, (0, 0, 0), 'Speech: On')

timer = pygame.time.Clock()

tempbg = pygame.image.load('images/background.png').convert_alpha()
main_menu_bg = pygame.image.load("images/main_menu_bg.png").convert_alpha()
pause_menu_bg = pygame.image.load("images/pause_menu_bg.png").convert_alpha()
minigame_1_bg = pygame.image.load('images/minigame1_bg.png').convert_alpha()
minigame_2_bg = pygame.image.load('images/minigame_2_bg.png').convert_alpha()
minigame_3_bg = pygame.image.load('images/minigame3_bg.png').convert_alpha()
continued_bg = pygame.image.load('images/background.png').convert_alpha()
win_screen_bg = pygame.image.load('images/win_screen_bg.png').convert_alpha()
lose_screen_bg = pygame.image.load('images/lose_screen_bg.png').convert_alpha()

temp_text_box = pygame.image.load('images/temptextboxpng.png').convert_alpha()
speech_box_img = pygame.image.load('images/speech_box.png').convert_alpha()
speech_box_img.set_colorkey((255, 0, 0))
level_box_img = pygame.image.load('images/level_box.png').convert_alpha()
level_box_img.set_colorkey(white)

select_man_img = pygame.image.load('images/man_player.png').convert_alpha()
select_man_img.set_colorkey(white)
select_woman_img = pygame.image.load('images/woman_player.png').convert_alpha()
select_woman_img.set_colorkey(white)
customer_img = pygame.image.load('images/customer.png').convert_alpha()
customer_img.set_colorkey(white)
enemy_img = pygame.image.load('images/enemy.png').convert_alpha()
enemy_img.set_colorkey(white)

chair_img = pygame.image.load('images/chair.png').convert_alpha()
table_img = pygame.image.load('images/table.png').convert_alpha()
couch_img = pygame.image.load('images/couch.png').convert_alpha()
chair_img.set_colorkey(white)
table_img.set_colorkey(white)
couch_img.set_colorkey(white)

store_front = pygame.image.load('images/store_front.png').convert_alpha()
enemy_store = pygame.image.load('images/enemy_store.png').convert_alpha()

road_image = pygame.image.load('images/road.png').convert_alpha()
top_road_image = pygame.image.load('images/top_road.png').convert_alpha()
bottom_road_image = pygame.image.load('images/bottom_road.png').convert_alpha()
building_block = pygame.image.load('images/brick_block_1.png').convert_alpha()
TILE_SIZE = road_image.get_width()

true_scroll = [0, 0]
last_time = time.time()
start_time = None

previous_rect = pygame.Rect(1000, 400, 1, 1)

animation_frames = {}


def load_animations(path, frame_durations):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((251, 251, 251))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


animation_database = {'run_man': load_animations('images/player_animations/run', [12, 12]),
                      'idle_man': load_animations('images/player_animations/idle', [40, 40]),
                      'run_woman': load_animations('images/player2_animations/run2', [12, 12]),
                      'idle_woman': load_animations('images/player2_animations/idle2', [40, 40])}


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


pygame.mixer.music.set_volume(.2)
pygame.mixer.music.load("sounds/main_menu_music.mp3")
pygame.mixer.music.play(-1)


def main_menu(sound=False):
    run = True

    play_button = engine.Button(display.get_width() // 2 - 90 // 2, 170, 90, 35, font, (0, 0, 0), 'Play')
    settings_button = engine.Button(display.get_width() // 2 - 150 // 2, 225, 150, 35, font, (0, 0, 0), 'Settings')
    exit_button = engine.Button(display.get_width() // 2 - 90 // 2, 280, 90, 35, font, (0, 0, 0), 'Exit')

    if sound:
        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.load("sounds/main_menu_music.mp3")
        pygame.mixer.music.play(-1)

    while run:

        display.fill((0, 0, 0))
        display.blit(main_menu_bg, (0, 0))

        w = screen.get_size()[0] / 600
        h = screen.get_size()[1] / 400

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0] / w
        mpos[1] = mpos[1] / h
        text = tfont.render('American Enterprise', True, (0, 0, 0))
        display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 80))

        if play_button.is_over(mpos):
            play_button.draw(display, (100, 100, 100, 90))
        else:
            play_button.draw(display, (50, 50, 50, 0))
        if settings_button.is_over(mpos):
            settings_button.draw(display, (100, 100, 100, 90))
        else:
            settings_button.draw(display, (50, 50, 50, 0))
        if exit_button.is_over(mpos):
            exit_button.draw(display, (100, 100, 100, 90))
        else:
            exit_button.draw(display, (50, 50, 50, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_1:
                    game_over_win(1000, 900)
                if event.key == pygame.K_2:
                    game_over_lose(870, 900)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_over(mpos):
                    character_selection()
                if settings_button.is_over(mpos):
                    settings()
                if exit_button.is_over(mpos):
                    sys.exit()

        surf = pygame.transform.scale(display, screen.get_size())
        screen.blit(surf, (0, 0))
        pygame.display.update()


def settings():
    run = True
    title = font.render('Settings', True, (0, 0, 0))

    res_button = engine.Button(display.get_width() // 2 - 140 // 2, 100, 140, 25, sfont, (0, 0, 0), 'Resolution')
    sound_button = engine.Button(display.get_width() // 2 - 80 // 2, 160, 80, 25, sfont, (0, 0, 0), 'Sound')
    back_button = engine.Button(display.get_width() // 2 - 100 // 2, 220, 100, 25, sfont, (0, 0, 0), '< Back')

    while run:

        display.fill((0, 0, 0))
        display.blit(main_menu_bg, (0, 0))

        display.blit(title, (display.get_width() // 2 - title.get_width() // 2, 30))

        w = screen.get_size()[0] / 600
        h = screen.get_size()[1] / 400

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0] / w
        mpos[1] = mpos[1] / h

        if res_button.is_over(mpos):
            res_button.draw(display, (100, 100, 100, 90))
        else:
            res_button.draw(display, (50, 50, 50, 0))
        if sound_button.is_over(mpos):
            sound_button.draw(display, (100, 100, 100, 90))
        else:
            sound_button.draw(display, (50, 50, 50, 0))
        if back_button.is_over(mpos):
            back_button.draw(display, (100, 100, 100, 90))
        else:
            back_button.draw(display, (50, 50, 50, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if res_button.is_over(mpos):
                    resolution_settings()
                if sound_button.is_over(mpos):
                    sound_settings()
                if back_button.is_over(mpos):
                    main_menu()

        surf = pygame.transform.scale(display, screen.get_size())
        screen.blit(surf, (0, 0))
        pygame.display.update()


# Done
def resolution_settings():
    run = True
    title = font.render('Resolution', True, (0, 0, 0))

    res1_button = engine.Button(display.get_width() // 2 - 120 // 2, 100, 120, 25, sfont, (0, 0, 0), '600, 400')
    res2_button = engine.Button(display.get_width() // 2 - 120 // 2, 130, 120, 25, sfont, (0, 0, 0), '900, 600')
    res3_button = engine.Button(display.get_width() // 2 - 125 // 2, 160, 125, 25, sfont, (0, 0, 0), '1200, 800')
    res4_button = engine.Button(display.get_width() // 2 - 130 // 2, 190, 130, 25, sfont, (0, 0, 0), '1500, 1000')
    back_button = engine.Button(display.get_width() // 2 - 120 // 2, 220, 100, 25, sfont, (0, 0, 0), '< Back')

    while run:

        display.fill((0, 0, 0))
        display.blit(main_menu_bg, (0, 0))

        display.blit(title, (display.get_width() // 2 - title.get_width() // 2, 30))

        w = screen.get_size()[0] / 600
        h = screen.get_size()[1] / 400

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0] / w
        mpos[1] = mpos[1] / h

        if res1_button.is_over(mpos):
            res1_button.draw(display, (100, 100, 100, 90))
        else:
            res1_button.draw(display, (50, 50, 50, 0))
        if res2_button.is_over(mpos):
            res2_button.draw(display, (100, 100, 100, 90))
        else:
            res2_button.draw(display, (50, 50, 50, 0))
        if res3_button.is_over(mpos):
            res3_button.draw(display, (100, 100, 100, 90))
        else:
            res3_button.draw(display, (50, 50, 50, 0))
        if res4_button.is_over(mpos):
            res4_button.draw(display, (100, 100, 100, 90))
        else:
            res4_button.draw(display, (50, 50, 50, 0))
        if back_button.is_over(mpos):
            back_button.draw(display, (100, 100, 100, 90))
        else:
            back_button.draw(display, (50, 50, 50, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if res1_button.is_over(mpos):
                    pygame.display.set_mode((600, 400), pygame.RESIZABLE)
                if res2_button.is_over(mpos):
                    pygame.display.set_mode((900, 600), pygame.RESIZABLE)
                if res3_button.is_over(mpos):
                    pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
                if res4_button.is_over(mpos):
                    pygame.display.set_mode((1500, 1000), pygame.RESIZABLE)
                if back_button.is_over(mpos):
                    settings()

        surf = pygame.transform.scale(display, screen.get_size())
        screen.blit(surf, (0, 0))
        pygame.display.update()


# Needs updating once music gets added
def sound_settings():
    run = True
    title = font.render('Sound', True, (0, 0, 0))
    back_button = engine.Button(display.get_width() // 2 - 100 // 2, 280, 100, 25, sfont, (0, 0, 0), '< Back')
    global music_button, sfx_button, speech_button

    while run:

        display.fill((0, 0, 0))
        display.blit(main_menu_bg, (0, 0))

        display.blit(title, (display.get_width() // 2 - title.get_width() // 2, 30))

        w = screen.get_size()[0] / 600
        h = screen.get_size()[1] / 400

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0] / w
        mpos[1] = mpos[1] / h

        if sfx_button.is_over(mpos):
            sfx_button.draw(display, (100, 100, 100, 90))
        else:
            sfx_button.draw(display, (50, 50, 50, 0))
        if music_button.is_over(mpos):
            music_button.draw(display, (100, 100, 100, 90))
        else:
            music_button.draw(display, (50, 50, 50, 0))
        if speech_button.is_over(mpos):
            speech_button.draw(display, (100, 100, 100, 90))
        else:
            speech_button.draw(display, (50, 50, 50, 0))
        if back_button.is_over(mpos):
            back_button.draw(display, (100, 100, 100, 90))
        else:
            back_button.draw(display, (50, 50, 50, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sfx_button.is_over(mpos):
                    if sfx_button.text == 'SFX: On':
                        sfx_button.text = 'SFX: Off'
                    else:
                        sfx_button.text = 'SFX: On'
                if music_button.is_over(mpos):
                    if music_button.text == 'Music: On':
                        music_button.text = 'Music: Off'
                        pygame.mixer.music.set_volume(0)
                    else:
                        music_button.text = 'Music: On'
                        pygame.mixer.music.set_volume(.2)
                if speech_button.is_over(mpos):
                    if speech_button.text == 'Speech: On':
                        speech_button.text = 'Speech: Off'
                    else:
                        speech_button.text = 'Speech: On'
                if back_button.is_over(mpos):
                    settings()

        surf = pygame.transform.scale(display, screen.get_size())
        screen.blit(surf, (0, 0))
        pygame.display.update()


def character_selection():
    run = True

    char1_button = engine.Button(130, 137, 90, 140, font, (0, 0, 0))
    char2_button = engine.Button(380, 137, 90, 140, font, (0, 0, 0))
    back_button = engine.Button(display.get_width() // 2 - 110 // 2, 280, 110, 35, font, (0, 0, 0), '< Back')

    while run:
        display.fill((0, 0, 0))
        display.blit(main_menu_bg, (0, 0))

        w = screen.get_size()[0] / 600
        h = screen.get_size()[1] / 400

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0] / w
        mpos[1] = mpos[1] / h

        text = tfont.render('Character Selection', True, (0, 0, 0))
        display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 80))

        if char1_button.is_over(mpos):
            char1_button.draw(display, (100, 100, 100, 90))
        else:
            char1_button.draw(display, (50, 50, 50, 0))
        if char2_button.is_over(mpos):
            char2_button.draw(display, (100, 100, 100, 90))
        else:
            char2_button.draw(display, (50, 50, 50, 0))
        if back_button.is_over(mpos):
            back_button.draw(display, (100, 100, 100, 90))
        else:
            back_button.draw(display, (50, 50, 50, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if char1_button.is_over(mpos):
                    game_intro('man')
                if char2_button.is_over(mpos):
                    game_intro('woman')
                if back_button.is_over(mpos):
                    main_menu()

        display.blit(select_man_img, (150, 140))
        display.blit(select_woman_img, (400, 140))

        surf = pygame.transform.scale(display, screen.get_size())
        screen.blit(surf, (0, 0))
        pygame.display.update()


def game_intro(selected_char):
    run = True

    start_button = engine.Button(480, 345, 90, 35, vsfont, (0, 0, 0), 'START')

    game_intro_message = 'You find yourself at the beginning of an exciting journey as the owner of a thriving new furniture business. However, you face challenges ahead. You compete with another thriving furniture business in the city. Gain more points than your competitor through minigames to successfully grow your business and become the best furniture-selling store in the city! Use your business leadership and money management skills to beat your opponent. Good Luck!'
    counter = 0
    counter_2 = 350
    counter_3 = 720
    counter_4 = 1075
    counter_5 = 1410
    counter_6 = 1760
    counter_7 = 2115
    speed = 5
    done = False
    done_2 = False
    done_3 = False
    done_4 = False
    done_5 = False
    done_6 = False
    done_7 = False

    while run:
        display.fill((0, 0, 0))
        display.blit(tempbg, (0, 0))
        # text_display.fill((150, 150, 150))
        # text_display.set_colorkey((150, 150, 150))

        w = screen.get_size()[0] / 600
        h = screen.get_size()[1] / 400

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0] / w
        mpos[1] = mpos[1] / h

        temp_text_box.set_colorkey((100, 101, 99))
        display.blit(temp_text_box, (0, 200))

        if counter < speed * 70:
            counter += 1
        elif counter >= speed * 70:
            done = True

        if done:
            if counter_2 < speed * 144:
                counter_2 += 1
            elif counter_2 >= speed * 144:
                done_2 = True

        if done_2:
            if counter_3 < speed * 215:
                counter_3 += 1
            elif counter_3 >= speed * 215:
                done_3 = True

        if done_3:
            if counter_4 < speed * 282:
                counter_4 += 1
            elif counter_4 >= speed * 282:
                done_4 = True

        if done_4:
            if counter_5 < speed * 352:
                counter_5 += 1
            elif counter_5 >= speed * 352:
                done_5 = True

        if done_5:
            if counter_6 < speed * 423:
                counter_6 += 1
            elif counter_6 >= speed * 423:
                done_6 = True

        if done_6:
            if counter_7 < speed * 449:
                counter_7 += 1
            elif counter_7 >= speed * 449:
                done_7 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_over(mpos):
                    lobby(selected_char, 0, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_9:
                    lobby(selected_char, 0, 0)

        snip = vsfont.render(game_intro_message[0:counter // speed], True, (0, 0, 0))
        display.blit(snip, (20, 220))
        # text_display.blit(snip, (20, 220))
        if done:
            snip_2 = vsfont.render(game_intro_message[71:counter_2 // speed], True, (0, 0, 0))
            display.blit(snip_2, (20, 240))
        if done_2:
            snip_3 = vsfont.render(game_intro_message[145:counter_3 // speed], True, (0, 0, 0))
            display.blit(snip_3, (20, 260))
        if done_3:
            snip_4 = vsfont.render(game_intro_message[216:counter_4 // speed], True, (0, 0, 0))
            display.blit(snip_4, (20, 280))
        if done_4:
            snip_5 = vsfont.render(game_intro_message[283:counter_5 // speed], True, (0, 0, 0))
            display.blit(snip_5, (20, 300))
        if done_5:
            snip_6 = vsfont.render(game_intro_message[353:counter_6 // speed], True, (0, 0, 0))
            display.blit(snip_6, (20, 320))
        if done_6:
            snip_7 = vsfont.render(game_intro_message[424:counter_7 // speed], True, (0, 0, 0))
            display.blit(snip_7, (20, 340))
        if done_7:
            if start_button.is_over(mpos):
                start_button.draw(display, (255, 255, 255, 100))
            else:
                start_button.draw(display, (50, 50, 50, 0))

        surf = pygame.transform.scale(display, screen.get_size())
        screen.blit(surf, (0, 0))
        # surf = pygame.transform.smoothscale(text_display, screen.get_size())
        # screen.blit(surf, (0, 0))
        pygame.display.update()


def lobby(selected_char, minigames_completed, points):
    run = True

    continue_button = engine.Button(display.get_width() // 2 - 110 // 2, 100, 110, 35, sfont, white, 'Continue')
    settings_button = engine.Button(display.get_width() // 2 - 110 // 2, 160, 110, 35, sfont, white, 'Settings')
    main_menu_button = engine.Button(display.get_width() // 2 - 150 // 2, 220, 150, 35, sfont, white, 'Main Menu')
    title = font.render('Settings', True, (255, 255, 255))
    res_button = engine.Button(display.get_width() // 2 - 140 // 2, 100, 140, 25, sfont, white, 'Resolution')
    sound_button = engine.Button(display.get_width() // 2 - 80 // 2, 160, 80, 25, sfont, white, 'Sound')
    back_button = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    title_2 = font.render('Resolution', True, (255, 255, 255))
    res1_button = engine.Button(display.get_width() // 2 - 120 // 2, 100, 120, 25, sfont, white, '600, 400')
    res2_button = engine.Button(display.get_width() // 2 - 120 // 2, 130, 120, 25, sfont, white, '900, 600')
    res3_button = engine.Button(display.get_width() // 2 - 125 // 2, 160, 125, 25, sfont, white, '1200, 800')
    res4_button = engine.Button(display.get_width() // 2 - 130 // 2, 190, 130, 25, sfont, white, '1500, 1000')
    back_button_2 = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    title_3 = font.render('Sound', True, (255, 255, 255))
    back_button_3 = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    sfx_button = engine.Button(display.get_width() // 2 - 100 // 2, 100, 100, 25, sfont, white, 'SFX: On')
    music_button = engine.Button(display.get_width() // 2 - 130 // 2, 140, 130, 25, sfont, white, 'Music: On')
    speech_button = engine.Button(display.get_width() // 2 - 130 // 2, 180, 145, 25, sfont, white, 'Speech: On')
    minigame_1_button = engine.Button(272, 150, 55, 35, vsfont, white, 'Level 1')
    minigame_2_button = engine.Button(272, 190, 55, 35, vsfont, white, 'Level 2')
    minigame_3_button = engine.Button(272, 230, 55, 35, vsfont, white, 'Level 3')

    moving_right = False
    moving_left = False

    player = engine.Entity(700, 284, 20, 53, 0, 'player')
    player_rect = player.rect()

    flip = False
    player_frame = 0

    interact_text = vsfont.render('Press E to Interact', True, white)
    arrow_text = vsfont.render('Use Left and Right Arrow Keys to Move', True, white)

    e_pressed = False
    e_pressed_count = 1

    current_points = points
    enemy_points = 0

    final_game_state = ''

    if minigames_completed == 1:
        enemy_points = 15
    if minigames_completed == 2:
        enemy_points = 915
    if minigames_completed == 3:
        enemy_points = 1050

    global last_time

    game_map = engine.load_map("maps/lobby_map")

    player_action = 0

    if selected_char == 'man':
        player_action = 'idle_man'
        player = engine.Entity(700, 284, 20, 53, 0, 'player')
        player_rect = player.rect()
    if selected_char == 'woman':
        player_action = 'idle_woman'
        player = engine.Entity(700, 289, 20, 48, 0, 'player')
        player_rect = player.rect()

    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.load("sounds/lobby_music.mp3")
    pygame.mixer.music.play(-1)
    run_sound = pygame.mixer.Sound('sounds/walking sound.mp3')
    run_sound.set_volume(.5)
    run_sound_timer = 0

    gamestate = 'game'

    while run:
        if gamestate == 'game':

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            timer.tick(120)

            true_scroll[0] += 1
            true_scroll[0] += (player_rect.x - true_scroll[0] - 300) / 20
            true_scroll[1] += (player_rect.y - true_scroll[1] - 280) / 20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            display.fill((0, 0, 0))
            display.blit(continued_bg, (-400 - scroll[0] * .15, 0 - scroll[1] * .15))
            display.blit(tempbg, (200 - scroll[0] * .15, 0 - scroll[1] * .15))
            display.blit(continued_bg, (800 - scroll[0] * .15, 0 - scroll[1] * .15))

            if minigames_completed == 3 and current_points > enemy_points:
                final_game_state = 'win'
            if minigames_completed == 3 and current_points <= enemy_points:
                final_game_state = 'lose'

            if minigames_completed == 3 and final_game_state == 'win':
                game_over_win(current_points, enemy_points)
            if minigames_completed == 3 and final_game_state == 'lose':
                game_over_lose(current_points, enemy_points)

            tile_rects = []
            y = 0
            for row in game_map:
                x = 0
                for tile in row:
                    if tile == '1':
                        display.blit(road_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '2':
                        display.blit(top_road_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '3':
                        display.blit(bottom_road_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile == '4':
                        display.blit(building_block, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                    if tile != '0' and tile != '1':
                        tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    x += 1
                y += 1

            player_movement = [0, 0]
            if moving_right:
                player_movement[0] += 1
                flip = False
            if moving_left:
                player_movement[0] -= 1
                flip = True

            if run_sound_timer > 0:
                run_sound_timer -= 1
            if player_movement[0] != 0:
                if run_sound_timer == 0:
                    run_sound_timer = 30
                    run_sound.play()
            if player_movement[0] == 0:
                run_sound.stop()

            if selected_char == 'man':
                if player_movement[0] > 0:
                    player_action, player_frame = change_action(player_action, player_frame, 'run_man')
                if player_movement[0] == 0:
                    player_action, player_frame = change_action(player_action, player_frame, 'idle_man')
                if player_movement[0] < 0:
                    player_action, player_frame = change_action(player_action, player_frame, 'run_man')
            if selected_char == 'woman':
                if player_movement[0] > 0:
                    player_action, player_frame = change_action(player_action, player_frame, 'run_woman')
                if player_movement[0] == 0:
                    player_action, player_frame = change_action(player_action, player_frame, 'idle_woman')
                if player_movement[0] < 0:
                    player_action, player_frame = change_action(player_action, player_frame, 'run_woman')

            player_rect, collisions = engine.collision_move(player_rect, player_movement, tile_rects)

            display.blit(store_front, (1000 - true_scroll[0], 137 - true_scroll[1]))
            display.blit(enemy_store, (1800 - true_scroll[0], 137 - true_scroll[1]))
            display.blit(enemy_img, (1750 - true_scroll[0], 272 - true_scroll[1]))

            player_frame += 1
            if player_frame >= len(animation_database[player_action]):
                player_frame = 0
            player_img_id = animation_database[player_action][player_frame]
            player_img = animation_frames[player_img_id]
            display.blit(pygame.transform.flip(player_img, flip, False),
                         (player_rect.x - true_scroll[0], player_rect.y - true_scroll[1]))

            if e_pressed_count % 2 == 0:
                display.blit(level_box_img, (225, 100))
                level_text = vsfont.render('Level Picker', True, white)
                display.blit(level_text, (255, 120))
                if minigames_completed == 0:
                    if minigame_1_button.is_over(mpos):
                        minigame_1_button.draw(display, (255, 255, 255, 100))
                    else:
                        minigame_1_button.draw(display, (50, 50, 50, 0))
                if minigames_completed == 1:
                    if minigame_1_button.is_over(mpos):
                        minigame_1_button.draw(display, (255, 255, 255, 100))
                    else:
                        minigame_1_button.draw(display, (50, 50, 50, 0))
                    if minigame_2_button.is_over(mpos):
                        minigame_2_button.draw(display, (255, 255, 255, 100))
                    else:
                        minigame_2_button.draw(display, (50, 50, 50, 0))
                if minigames_completed == 2:
                    if minigame_1_button.is_over(mpos):
                        minigame_1_button.draw(display, (255, 255, 255, 100))
                    else:
                        minigame_1_button.draw(display, (50, 50, 50, 0))
                    if minigame_2_button.is_over(mpos):
                        minigame_2_button.draw(display, (255, 255, 255, 100))
                    else:
                        minigame_2_button.draw(display, (50, 50, 50, 0))
                    if minigame_3_button.is_over(mpos):
                        minigame_3_button.draw(display, (255, 255, 255, 100))
                    else:
                        minigame_3_button.draw(display, (50, 50, 50, 0))

            if 0 <= player_rect.x <= 800:
                display.blit(arrow_text, (display.get_width() // 2 - arrow_text.get_width() // 2, 380))
            if 1000 <= player_rect.x <= 1400:
                display.blit(interact_text, (250, 380))

            points_text = sfont.render('Points: ' + str(points), True, (0, 0, 0))
            display.blit(points_text, (10, 10))
            enemy_points_text = sfont.render('Enemy Points: ' + str(enemy_points), True, (0, 0, 0))
            display.blit(enemy_points_text, (380, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if minigame_1_button.is_over(mpos):
                        minigame1(selected_char)
                    if minigame_2_button.is_over(mpos):
                        minigame2(selected_char, current_points)
                    if minigame_3_button.is_over(mpos):
                        minigame3(selected_char, current_points)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'pause'
                    if event.key == pygame.K_RIGHT:
                        moving_right = True
                    if event.key == pygame.K_LEFT:
                        moving_left = True
                    if event.key == pygame.K_8:
                        minigame2(selected_char, current_points)
                    if event.key == pygame.K_7:
                        minigame3(selected_char, current_points)
                    if event.key == pygame.K_e and 1000 <= player_rect.x <= 1400:
                        e_pressed = True
                        e_pressed_count += 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        moving_right = False
                    if event.key == pygame.K_LEFT:
                        moving_left = False

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()

        if gamestate == 'pause':
            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))
            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if continue_button.is_over(mpos):
                continue_button.draw(display, (255, 255, 255, 100))
            else:
                continue_button.draw(display, (50, 50, 50, 0))
            if settings_button.is_over(mpos):
                settings_button.draw(display, (255, 255, 255, 100))
            else:
                settings_button.draw(display, (50, 50, 50, 0))
            if main_menu_button.is_over(mpos):
                main_menu_button.draw(display, (255, 255, 255, 100))
            else:
                main_menu_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    gamestate = 'game'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_button.is_over(mpos):
                        main_menu()
                    if continue_button.is_over(mpos):
                        gamestate = 'game'
                    if settings_button.is_over(mpos):
                        gamestate = 'settings'
            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()  # update display

        if gamestate == 'settings':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title, (display.get_width() // 2 - title.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if res_button.is_over(mpos):
                res_button.draw(display, (255, 255, 255, 100))
            else:
                res_button.draw(display, (50, 50, 50, 0))
            if sound_button.is_over(mpos):
                sound_button.draw(display, (255, 255, 255, 100))
            else:
                sound_button.draw(display, (50, 50, 50, 0))
            if back_button.is_over(mpos):
                back_button.draw(display, (255, 255, 255, 100))
            else:
                back_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'pause'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res_button.is_over(mpos):
                        gamestate = 'resolution'
                    if sound_button.is_over(mpos):
                        gamestate = 'sound'
                    if back_button.is_over(mpos):
                        gamestate = 'pause'

                surf = pygame.transform.scale(display, screen.get_size())
                screen.blit(surf, (0, 0))
                pygame.display.update()

        if gamestate == 'resolution':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title_2, (display.get_width() // 2 - title_2.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if res1_button.is_over(mpos):
                res1_button.draw(display, (255, 255, 255, 100))
            else:
                res1_button.draw(display, (50, 50, 50, 0))
            if res2_button.is_over(mpos):
                res2_button.draw(display, (255, 255, 255, 100))
            else:
                res2_button.draw(display, (50, 50, 50, 0))
            if res3_button.is_over(mpos):
                res3_button.draw(display, (255, 255, 255, 100))
            else:
                res3_button.draw(display, (50, 50, 50, 0))
            if res4_button.is_over(mpos):
                res4_button.draw(display, (255, 255, 255, 100))
            else:
                res4_button.draw(display, (50, 50, 50, 0))
            if back_button_2.is_over(mpos):
                back_button_2.draw(display, (255, 255, 255, 100))
            else:
                back_button_2.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res1_button.is_over(mpos):
                        pygame.display.set_mode((600, 400), pygame.RESIZABLE)
                    if res2_button.is_over(mpos):
                        pygame.display.set_mode((900, 600), pygame.RESIZABLE)
                    if res3_button.is_over(mpos):
                        pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
                    if res4_button.is_over(mpos):
                        pygame.display.set_mode((1500, 1000), pygame.RESIZABLE)
                    if back_button.is_over(mpos):
                        gamestate = 'settings'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()

        if gamestate == 'sound':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title_3, (display.get_width() // 2 - title_3.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if sfx_button.is_over(mpos):
                sfx_button.draw(display, (255, 255, 255, 100))
            else:
                sfx_button.draw(display, (50, 50, 50, 0))
            if music_button.is_over(mpos):
                music_button.draw(display, (255, 255, 255, 100))
            else:
                music_button.draw(display, (50, 50, 50, 0))
            if speech_button.is_over(mpos):
                speech_button.draw(display, (255, 255, 255, 100))
            else:
                speech_button.draw(display, (50, 50, 50, 0))
            if back_button_3.is_over(mpos):
                back_button_3.draw(display, (255, 255, 255, 100))
            else:
                back_button_3.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'settings'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sfx_button.is_over(mpos):
                        if sfx_button.text == 'SFX: On':
                            sfx_button.text = 'SFX: Off'
                        else:
                            sfx_button.text = 'SFX: On'
                    if music_button.is_over(mpos):
                        if music_button.text == 'Music: On':
                            music_button.text = 'Music: Off'
                            pygame.mixer.music.set_volume(0)
                        else:
                            music_button.text = 'Music: On'
                            pygame.mixer.music.set_volume(.3)
                    if speech_button.is_over(mpos):
                        if speech_button.text == 'Speech: On':
                            speech_button.text = 'Speech: Off'
                        else:
                            speech_button.text = 'Speech: On'
                    if back_button_3.is_over(mpos):
                        gamestate = 'settings'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()


def minigame1(selected_char):
    run = True

    continue_button = engine.Button(display.get_width() // 2 - 110 // 2, 100, 110, 35, sfont, white, 'Continue')
    settings_button = engine.Button(display.get_width() // 2 - 110 // 2, 160, 110, 35, sfont, white, 'Settings')
    main_menu_button = engine.Button(display.get_width() // 2 - 150 // 2, 220, 150, 35, sfont, white, 'Main Menu')
    title = font.render('Settings', True, (255, 255, 255))
    res_button = engine.Button(display.get_width() // 2 - 140 // 2, 100, 140, 25, sfont, white, 'Resolution')
    sound_button = engine.Button(display.get_width() // 2 - 80 // 2, 160, 80, 25, sfont, white, 'Sound')
    back_button = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    title_2 = font.render('Resolution', True, (255, 255, 255))
    res1_button = engine.Button(display.get_width() // 2 - 120 // 2, 100, 120, 25, sfont, white, '600, 400')
    res2_button = engine.Button(display.get_width() // 2 - 120 // 2, 130, 120, 25, sfont, white, '900, 600')
    res3_button = engine.Button(display.get_width() // 2 - 125 // 2, 160, 125, 25, sfont, white, '1200, 800')
    res4_button = engine.Button(display.get_width() // 2 - 130 // 2, 190, 130, 25, sfont, white, '1500, 1000')
    back_button_2 = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    title_3 = font.render('Sound', True, (255, 255, 255))
    back_button_3 = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    sfx_button = engine.Button(display.get_width() // 2 - 100 // 2, 100, 100, 25, sfont, white, 'SFX: On')
    music_button = engine.Button(display.get_width() // 2 - 130 // 2, 140, 130, 25, sfont, white, 'Music: On')
    speech_button = engine.Button(display.get_width() // 2 - 130 // 2, 180, 145, 25, sfont, white, 'Speech: On')
    start_button = engine.Button(display.get_width() // 2 - 100 // 2, 270, 100, 25, sfont, (0, 0, 0), 'Start')
    lobby_button = engine.Button(display.get_width() // 2 - 150 // 2, 870, 150, 25, sfont, (0, 0, 0),
                                 'Back to city')

    moving_right = False
    moving_left = False

    player_momentum = 0
    air_timer = 0

    global last_time
    spawn_time = 200

    chairs = []
    tables = []
    couches = []

    picked_up_furniture = []

    amount_of_furniture = 0
    furniture_limit = False
    furniture_deposit = False

    score = 0
    countdown = 0
    tutorial = True
    game_over = False

    global previous_rect, start_time

    counter = 0

    game_map = engine.load_map("maps/lobby_map")

    flip = False
    player_action = 0
    player_frame = 0

    if selected_char == 'man':
        player_action = 'idle_man'
        player = engine.Entity(100, 289, 20, 53, 0, 'player')
        player_rect = player.rect()
    if selected_char == 'woman':
        player_action = 'idle_woman'
        player = engine.Entity(100, 294, 20, 48, 0, 'player')
        player_rect = player.rect()

    gamestate = 'game'

    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.load("sounds/minigame_music.mp3")
    pygame.mixer.music.play(-1)
    run_sound = pygame.mixer.Sound('sounds/walking sound.mp3')
    run_sound.set_volume(.5)
    run_sound_timer = 0

    while run:
        if gamestate == 'game':

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            display.fill((0, 0, 0))
            display.blit(minigame_1_bg, (0, 0))

            timer.tick(120)

            if tutorial:
                pygame.draw.rect(display, (170, 170, 170), pygame.Rect(100, 100, 400, 200))
                text = sfont.render('Rules', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 100))
                text = vsfont.render('Use arrow keys to move', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 130))
                text = vsfont.render('Catch the furniture and drop it off to earn points', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 160))
                text = vsfont.render('Max furniture you can carry at a time: 5', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 190))
                text = vsfont.render('You have 1 minute. Good luck!', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 220))
                if start_button.is_over(mpos):
                    start_button.draw(display, (0, 0, 0, 100))
                else:
                    start_button.draw(display, (50, 50, 50, 0))
            if not tutorial:
                if counter != 60:
                    countdown += 1
                    time_text = sfont.render('Time: ' + str(60 - counter), True, (255, 255, 255))
                    display.blit(time_text, (500, 10))
                    if countdown % 120 == 0 and countdown != 0:
                        counter += 1
                if counter == 60:
                    game_over = True
                score_text = sfont.render('Score: ' + str(score), True, (255, 255, 255))
                display.blit(score_text, (10, 10))
            if game_over:
                pygame.draw.rect(display, (170, 170, 170), pygame.Rect(100, 100, 400, 200))
                text = sfont.render('Time is up!', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 120))
                text = sfont.render('Score: ' + str(score), True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 180))
                lobby_button.y = 270
                if lobby_button.is_over(mpos):
                    lobby_button.draw(display, (0, 0, 0, 100))
                else:
                    lobby_button.draw(display, (50, 50, 50, 0))

            if not tutorial and not game_over:
                if moving_right:
                    player_rect.x += 1
                    flip = False
                if moving_left:
                    player_rect.x -= 1
                    flip = True
                if run_sound_timer > 0:
                    run_sound_timer -= 1
                if moving_left or moving_right:
                    if run_sound_timer == 0:
                        run_sound_timer = 30
                        run_sound.play()
                if not moving_left and not moving_right:
                    run_sound.stop()

            if not tutorial and not game_over:
                spawn_time += 1
                if spawn_time == 320:
                    type_of_furniture = random.randint(1, 3)
                    if type_of_furniture == 1:
                        chairs.append(pygame.Rect(random.randint(110, 550), 0, 50, 50))
                        spawn_time = 0
                    if type_of_furniture == 2:
                        tables.append(pygame.Rect(random.randint(100, 550), 0, 100, 50))
                        spawn_time = 0
                    if type_of_furniture == 3:
                        couches.append(pygame.Rect(random.randint(100, 550), 0, 120, 50))
                        spawn_time = 0

            if not game_over:
                for chair in chairs:
                    chair.y += 1
                    display.blit(chair_img, (chair.x, chair.y))
                    if chair.y >= 400:
                        chairs.remove(chair)
                    if (chair.colliderect(player_rect) and not furniture_limit) or (chair.colliderect(
                            previous_rect) and not furniture_limit):
                        collide_sound = pygame.mixer.Sound('sounds/stacking_sound.mp3')
                        collide_sound.play()
                        amount_of_furniture += 1
                        if amount_of_furniture == 1:
                            picked_up_furniture.append(['chair', 1])
                            chairs.remove(chair)
                        if amount_of_furniture == 2:
                            picked_up_furniture.append(['chair', 2])
                            chairs.remove(chair)
                        if amount_of_furniture == 3:
                            picked_up_furniture.append(['chair', 3])
                            chairs.remove(chair)
                        if amount_of_furniture == 4:
                            picked_up_furniture.append(['chair', 4])
                            chairs.remove(chair)
                        if amount_of_furniture == 5:
                            picked_up_furniture.append(['chair', 5])
                            chairs.remove(chair)
                            furniture_limit = True
                for table in tables:
                    table.y += 1
                    display.blit(table_img, (table.x, table.y))
                    if table.y >= 400:
                        tables.remove(table)
                    if (table.colliderect(player_rect) and not furniture_limit) or (table.colliderect(
                            previous_rect) and not furniture_limit):
                        amount_of_furniture += 1
                        collide_sound = pygame.mixer.Sound('sounds/stacking_sound.mp3')
                        collide_sound.play()
                        if amount_of_furniture == 1:
                            picked_up_furniture.append(['table', 1])
                            tables.remove(table)
                        if amount_of_furniture == 2:
                            picked_up_furniture.append(['table', 2])
                            tables.remove(table)
                        if amount_of_furniture == 3:
                            picked_up_furniture.append(['table', 3])
                            tables.remove(table)
                        if amount_of_furniture == 4:
                            picked_up_furniture.append(['table', 4])
                            tables.remove(table)
                        if amount_of_furniture == 5:
                            picked_up_furniture.append(['table', 5])
                            tables.remove(table)
                            furniture_limit = True
                for couch in couches:
                    couch.y += 1
                    display.blit(couch_img, (couch.x, couch.y))
                    if couch.y >= 400:
                        couches.remove(couch)
                    if (couch.colliderect(player_rect) and not furniture_limit) or (couch.colliderect(
                            previous_rect) and not furniture_limit):
                        amount_of_furniture += 1
                        collide_sound = pygame.mixer.Sound('sounds/stacking_sound.mp3')
                        collide_sound.play()
                        if amount_of_furniture == 1:
                            picked_up_furniture.append(['couch', 1])
                            couches.remove(couch)
                        if amount_of_furniture == 2:
                            picked_up_furniture.append(['couch', 2])
                            couches.remove(couch)
                        if amount_of_furniture == 3:
                            picked_up_furniture.append(['couch', 3])
                            couches.remove(couch)
                        if amount_of_furniture == 4:
                            picked_up_furniture.append(['couch', 4])
                            couches.remove(couch)
                        if amount_of_furniture == 5:
                            picked_up_furniture.append(['couch', 5])
                            couches.remove(couch)
                            furniture_limit = True

                for furniture in picked_up_furniture:
                    if furniture[0] == 'chair':
                        if furniture[1] == 1 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 20, 235, 50, 50)
                            display.blit(chair_img, (player_rect.x - 20, 235))
                        if furniture[1] == 2 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 20, 185, 50, 50)
                            display.blit(chair_img, (player_rect.x - 20, 185))
                        if furniture[1] == 3 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 20, 135, 50, 50)
                            display.blit(chair_img, (player_rect.x - 20, 135))
                        if furniture[1] == 4 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 20, 85, 50, 50)
                            display.blit(chair_img, (player_rect.x - 20, 85))
                        if furniture[1] == 5 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 20, 35, 50, 50)
                            display.blit(chair_img, (player_rect.x - 20, 35))
                    if furniture[0] == 'table':
                        if furniture[1] == 1 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 35, 235, 80, 50)
                            display.blit(table_img, (player_rect.x - 35, 235))
                        if furniture[1] == 2 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 35, 185, 80, 50)
                            display.blit(table_img, (player_rect.x - 35, 185))
                        if furniture[1] == 3 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 35, 135, 80, 50)
                            display.blit(table_img, (player_rect.x - 35, 135))
                        if furniture[1] == 4 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 35, 85, 80, 50)
                            display.blit(table_img, (player_rect.x - 35, 85))
                        if furniture[1] == 5 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 35, 35, 80, 50)
                            display.blit(table_img, (player_rect.x - 35, 35))
                    if furniture[0] == 'couch':
                        if furniture[1] == 1 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 50, 235, 120, 50)
                            display.blit(couch_img, (player_rect.x - 50, 235))
                        if furniture[1] == 2 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 50, 185, 120, 50)
                            display.blit(couch_img, (player_rect.x - 50, 185))
                        if furniture[1] == 3 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 50, 135, 120, 50)
                            display.blit(couch_img, (player_rect.x - 50, 135))
                        if furniture[1] == 4 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 50, 85, 120, 50)
                            display.blit(couch_img, (player_rect.x - 50, 85))
                        if furniture[1] == 5 and not furniture_deposit:
                            previous_rect = pygame.Rect(player_rect.x - 50, 35, 120, 50)
                            display.blit(couch_img, (player_rect.x - 50, 35))

            if not tutorial and not game_over:
                if player_rect.x <= 60:
                    furniture_deposit = True
                    furniture_limit = False
                    score += amount_of_furniture
                    amount_of_furniture = 0
                    for furniture in picked_up_furniture:
                        picked_up_furniture.remove(furniture)
                if player_rect.x >= 60:
                    furniture_deposit = False

            if not tutorial and not game_over:
                if selected_char == 'man':
                    if moving_right:
                        player_action, player_frame = change_action(player_action, player_frame, 'run_man')
                    if moving_left:
                        player_action, player_frame = change_action(player_action, player_frame, 'run_man')
                    if not moving_left and not moving_right:
                        player_action, player_frame = change_action(player_action, player_frame, 'idle_man')
                if selected_char == 'woman':
                    if moving_right:
                        player_action, player_frame = change_action(player_action, player_frame, 'run_woman')
                    if moving_left:
                        player_action, player_frame = change_action(player_action, player_frame, 'run_woman')
                    if not moving_left and not moving_right:
                        player_action, player_frame = change_action(player_action, player_frame, 'idle_woman')

                player_frame += 1
                if player_frame >= len(animation_database[player_action]):
                    player_frame = 0
                player_img_id = animation_database[player_action][player_frame]
                player_img = animation_frames[player_img_id]
                display.blit(pygame.transform.flip(player_img, flip, False), (player_rect.x, player_rect.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_over(mpos):
                        tutorial = False
                    if lobby_button.is_over(mpos):
                        lobby(selected_char, 1, score)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'pause'
                    if event.key == pygame.K_RIGHT:
                        moving_right = True
                    if event.key == pygame.K_LEFT:
                        moving_left = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        moving_right = False
                    if event.key == pygame.K_LEFT:
                        moving_left = False

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()

        if gamestate == 'pause':
            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))
            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if continue_button.is_over(mpos):
                continue_button.draw(display, (255, 255, 255, 100))
            else:
                continue_button.draw(display, (50, 50, 50, 0))
            if settings_button.is_over(mpos):
                settings_button.draw(display, (255, 255, 255, 100))
            else:
                settings_button.draw(display, (50, 50, 50, 0))
            if main_menu_button.is_over(mpos):
                main_menu_button.draw(display, (255, 255, 255, 100))
            else:
                main_menu_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    gamestate = 'game'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_button.is_over(mpos):
                        main_menu()
                    if continue_button.is_over(mpos):
                        gamestate = 'game'
                    if settings_button.is_over(mpos):
                        gamestate = 'settings'
            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()  # update display

        if gamestate == 'settings':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title, (display.get_width() // 2 - title.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if res_button.is_over(mpos):
                res_button.draw(display, (255, 255, 255, 100))
            else:
                res_button.draw(display, (50, 50, 50, 0))
            if sound_button.is_over(mpos):
                sound_button.draw(display, (255, 255, 255, 100))
            else:
                sound_button.draw(display, (50, 50, 50, 0))
            if back_button.is_over(mpos):
                back_button.draw(display, (255, 255, 255, 100))
            else:
                back_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'pause'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res_button.is_over(mpos):
                        gamestate = 'resolution'
                    if sound_button.is_over(mpos):
                        gamestate = 'sound'
                    if back_button.is_over(mpos):
                        gamestate = 'pause'

                surf = pygame.transform.scale(display, screen.get_size())
                screen.blit(surf, (0, 0))
                pygame.display.update()

        if gamestate == 'resolution':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title_2, (display.get_width() // 2 - title_2.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if res1_button.is_over(mpos):
                res1_button.draw(display, (255, 255, 255, 100))
            else:
                res1_button.draw(display, (50, 50, 50, 0))
            if res2_button.is_over(mpos):
                res2_button.draw(display, (255, 255, 255, 100))
            else:
                res2_button.draw(display, (50, 50, 50, 0))
            if res3_button.is_over(mpos):
                res3_button.draw(display, (255, 255, 255, 100))
            else:
                res3_button.draw(display, (50, 50, 50, 0))
            if res4_button.is_over(mpos):
                res4_button.draw(display, (255, 255, 255, 100))
            else:
                res4_button.draw(display, (50, 50, 50, 0))
            if back_button_2.is_over(mpos):
                back_button_2.draw(display, (255, 255, 255, 100))
            else:
                back_button_2.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res1_button.is_over(mpos):
                        pygame.display.set_mode((600, 400), pygame.RESIZABLE)
                    if res2_button.is_over(mpos):
                        pygame.display.set_mode((900, 600), pygame.RESIZABLE)
                    if res3_button.is_over(mpos):
                        pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
                    if res4_button.is_over(mpos):
                        pygame.display.set_mode((1500, 1000), pygame.RESIZABLE)
                    if back_button.is_over(mpos):
                        gamestate = 'settings'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()

        if gamestate == 'sound':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title_3, (display.get_width() // 2 - title_3.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if sfx_button.is_over(mpos):
                sfx_button.draw(display, (255, 255, 255, 100))
            else:
                sfx_button.draw(display, (50, 50, 50, 0))
            if music_button.is_over(mpos):
                music_button.draw(display, (255, 255, 255, 100))
            else:
                music_button.draw(display, (50, 50, 50, 0))
            if speech_button.is_over(mpos):
                speech_button.draw(display, (255, 255, 255, 100))
            else:
                speech_button.draw(display, (50, 50, 50, 0))
            if back_button_3.is_over(mpos):
                back_button_3.draw(display, (255, 255, 255, 100))
            else:
                back_button_3.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'settings'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sfx_button.is_over(mpos):
                        if sfx_button.text == 'SFX: On':
                            sfx_button.text = 'SFX: Off'
                        else:
                            sfx_button.text = 'SFX: On'
                    if music_button.is_over(mpos):
                        if music_button.text == 'Music: On':
                            music_button.text = 'Music: Off'
                            pygame.mixer.music.set_volume(0)
                        else:
                            music_button.text = 'Music: On'
                            pygame.mixer.music.set_volume(.2)
                    if speech_button.is_over(mpos):
                        if speech_button.text == 'Speech: On':
                            speech_button.text = 'Speech: Off'
                        else:
                            speech_button.text = 'Speech: On'
                    if back_button_3.is_over(mpos):
                        gamestate = 'settings'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()


def minigame2(selected_char, points):
    run = True

    continue_button = engine.Button(display.get_width() // 2 - 110 // 2, 100, 110, 35, sfont, white, 'Continue')
    settings_button = engine.Button(display.get_width() // 2 - 110 // 2, 160, 110, 35, sfont, white, 'Settings')
    main_menu_button = engine.Button(display.get_width() // 2 - 150 // 2, 220, 150, 35, sfont, white, 'Main Menu')
    title = font.render('Settings', True, (255, 255, 255))
    res_button = engine.Button(display.get_width() // 2 - 140 // 2, 100, 140, 25, sfont, white, 'Resolution')
    sound_button = engine.Button(display.get_width() // 2 - 80 // 2, 160, 80, 25, sfont, white, 'Sound')
    back_button = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    title_2 = font.render('Resolution', True, (255, 255, 255))
    res1_button = engine.Button(display.get_width() // 2 - 120 // 2, 100, 120, 25, sfont, white, '600, 400')
    res2_button = engine.Button(display.get_width() // 2 - 120 // 2, 130, 120, 25, sfont, white, '900, 600')
    res3_button = engine.Button(display.get_width() // 2 - 125 // 2, 160, 125, 25, sfont, white, '1200, 800')
    res4_button = engine.Button(display.get_width() // 2 - 130 // 2, 190, 130, 25, sfont, white, '1500, 1000')
    back_button_2 = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    title_3 = font.render('Sound', True, (255, 255, 255))
    back_button_3 = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    sfx_button = engine.Button(display.get_width() // 2 - 100 // 2, 100, 100, 25, sfont, white, 'SFX: On')
    music_button = engine.Button(display.get_width() // 2 - 130 // 2, 140, 130, 25, sfont, white, 'Music: On')
    speech_button = engine.Button(display.get_width() // 2 - 130 // 2, 180, 145, 25, sfont, white, 'Speech: On')
    start_button = engine.Button(display.get_width() // 2 - 100 // 2, 270, 100, 25, sfont, (0, 0, 0), 'Start')
    lobby_button = engine.Button(display.get_width() // 2 - 150 // 2, 870, 150, 25, sfont, (0, 0, 0),
                                 'Back to city')

    moving_right = False
    moving_left = False
    moving_up = False
    moving_down = False

    global last_time

    customers = []
    no_customers = True
    received_furniture = False
    held_furniture = 0

    picked_up_furniture = []

    amount_of_furniture = 0

    money = 0
    countdown = 0
    tutorial = True
    game_over = False

    global previous_rect, start_time

    counter = 0
    num = 0

    game_map = engine.load_map("maps/lobby_map")

    flip = False
    player_action = 0
    player_frame = 0

    if selected_char == 'man':
        player_action = 'idle_man'
        player = engine.Entity(250, 150, 20, 53, 0, 'player')
        player_rect = player.rect()
    if selected_char == 'woman':
        player_action = 'idle_woman'
        player = engine.Entity(250, 150, 20, 48, 0, 'player')
        player_rect = player.rect()

    gamestate = 'game'

    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.load("sounds/minigame_music.mp3")
    pygame.mixer.music.play(-1)
    run_sound = pygame.mixer.Sound('sounds/walking sound.mp3')
    run_sound.set_volume(.5)
    run_sound_timer = 0

    while run:
        if gamestate == 'game':

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            display.fill((0, 0, 0))
            display.blit(minigame_2_bg, (0, 0))

            timer.tick(60)

            if tutorial:
                pygame.draw.rect(display, (170, 170, 170), pygame.Rect(100, 100, 400, 200))
                text = sfont.render('Rules', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 100))
                text = vsfont.render('Use arrow keys to move', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 130))
                text = vsfont.render('Look out for what the customer wants', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 160))
                text = vsfont.render('Collect the furniture and sell it to the customer', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 190))
                text = vsfont.render('You have 1 minute. Good luck!', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 220))
                if start_button.is_over(mpos):
                    start_button.draw(display, (0, 0, 0, 100))
                else:
                    start_button.draw(display, (50, 50, 50, 0))
            if not tutorial:
                if counter != 60:
                    countdown += 1
                    time_text = sfont.render('Time: ' + str(60 - counter), True, (255, 255, 255))
                    display.blit(time_text, (500, 10))
                    if countdown % 60 == 0 and countdown != 0:
                        counter += 1
                if counter == 60:
                    game_over = True
                score_text = sfont.render('Money: $' + str(money), True, (255, 255, 255))
                display.blit(score_text, (10, 10))
                if held_furniture == 1:
                    furniture_text = sfont.render('Inventory: Chair', True, (255, 255, 255))
                    display.blit(furniture_text, (300 - furniture_text.get_width() // 2, 350))
                if held_furniture == 2:
                    furniture_text = sfont.render('Inventory: Table', True, (255, 255, 255))
                    display.blit(furniture_text, (300 - furniture_text.get_width() // 2, 350))
                if held_furniture == 3:
                    furniture_text = sfont.render('Inventory: Couch', True, (255, 255, 255))
                    display.blit(furniture_text, (300 - furniture_text.get_width() // 2, 350))
            if game_over:
                pygame.draw.rect(display, (170, 170, 170), pygame.Rect(100, 100, 400, 200))
                text = sfont.render('Time is up!', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 100))
                text = sfont.render('Money: $' + str(money), True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 150))
                lobby_button.y = 270
                if lobby_button.is_over(mpos):
                    lobby_button.draw(display, (0, 0, 0, 100))
                else:
                    lobby_button.draw(display, (50, 50, 50, 0))

            if not tutorial and not game_over:
                if moving_right:
                    player_rect.x += 2
                    flip = False
                if moving_left:
                    player_rect.x -= 2
                    flip = True
                if moving_up:
                    player_rect.y -= 2
                if moving_down:
                    player_rect.y += 2
                if run_sound_timer > 0:
                    run_sound_timer -= 1
                if moving_right or moving_left or moving_up or moving_down:
                    if run_sound_timer == 0:
                        run_sound_timer = 15
                        run_sound.play()
                if not moving_left and not moving_right and not moving_down and not moving_up:
                    run_sound.stop()

            couch_rect = pygame.Rect(30, 280, 160, 90)
            shape_surf = pygame.Surface(couch_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0, 0, 0, 0), shape_surf.get_rect())
            display.blit(shape_surf, (30, 280, 160, 90))

            chair_rect = pygame.Rect(465, 285, 80, 80)
            shape_surf = pygame.Surface(chair_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0, 0, 0, 0), shape_surf.get_rect())
            display.blit(shape_surf, (465, 285, 80, 80))

            table_rect = pygame.Rect(230, 280, 150, 80)
            shape_surf = pygame.Surface(table_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0, 0, 0, 0), shape_surf.get_rect())
            display.blit(shape_surf, (230, 280, 150, 80))

            if not tutorial and not game_over and no_customers:
                customers.append([pygame.Rect(280, 80, 50, 50), random.randint(1, 3)])
                received_furniture = False
                no_customers = False

            if not game_over:
                for customer in customers:
                    shape_surf = pygame.Surface(customer[0].size, pygame.SRCALPHA)
                    pygame.draw.rect(shape_surf, (0, 0, 0, 0), shape_surf.get_rect())
                    display.blit(shape_surf, (30, 280, 160, 90))

                    display.blit(customer_img, (280, 80))
                    display.blit(speech_box_img, (310, 80))
                    if customer[1] == 1:
                        text = vsfont.render('chair', True, (0, 0, 0))
                        display.blit(text, (314, 85))
                    if customer[1] == 2:
                        text = vsfont.render('table', True, (0, 0, 0))
                        display.blit(text, (314, 85))
                    if customer[1] == 3:
                        text = vsfont.render('couch', True, (0, 0, 0))
                        display.blit(text, (314, 85))
                    if customer[0].colliderect(player_rect) and customer[1] == held_furniture:
                        received_furniture = True
                    if received_furniture:
                        money += 80
                        customers.remove(customer)
                        held_furniture = 0
                        received_furniture = False
                        no_customers = True

            if couch_rect.colliderect(player_rect):
                held_furniture = 3
            if table_rect.colliderect(player_rect):
                held_furniture = 2
            if chair_rect.colliderect(player_rect):
                held_furniture = 1

            if not tutorial and not game_over:
                if selected_char == 'man':
                    if moving_right or moving_up or moving_down:
                        player_action, player_frame = change_action(player_action, player_frame, 'run_man')
                    if moving_left:
                        player_action, player_frame = change_action(player_action, player_frame, 'run_man')
                    if not moving_left and not moving_right and not moving_up and not moving_down:
                        player_action, player_frame = change_action(player_action, player_frame, 'idle_man')
                if selected_char == 'woman':
                    if moving_right:
                        player_action, player_frame = change_action(player_action, player_frame, 'run_woman')
                    if moving_left:
                        player_action, player_frame = change_action(player_action, player_frame, 'run_woman')
                    if not moving_left and not moving_right:
                        player_action, player_frame = change_action(player_action, player_frame, 'idle_woman')

                player_frame += 1
                if player_frame >= len(animation_database[player_action]):
                    player_frame = 0
                player_img_id = animation_database[player_action][player_frame]
                player_img = animation_frames[player_img_id]
                display.blit(pygame.transform.flip(player_img, flip, False), (player_rect.x, player_rect.y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_over(mpos):
                        tutorial = False
                    if lobby_button.is_over(mpos):
                        lobby(selected_char, 2, money + points)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'pause'
                    if event.key == pygame.K_RIGHT:
                        moving_right = True
                    if event.key == pygame.K_LEFT:
                        moving_left = True
                    if event.key == pygame.K_UP:
                        moving_up = True
                    if event.key == pygame.K_DOWN:
                        moving_down = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        moving_right = False
                    if event.key == pygame.K_LEFT:
                        moving_left = False
                    if event.key == pygame.K_UP:
                        moving_up = False
                    if event.key == pygame.K_DOWN:
                        moving_down = False

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()

        if gamestate == 'pause':
            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))
            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if continue_button.is_over(mpos):
                continue_button.draw(display, (255, 255, 255, 100))
            else:
                continue_button.draw(display, (50, 50, 50, 0))
            if settings_button.is_over(mpos):
                settings_button.draw(display, (255, 255, 255, 100))
            else:
                settings_button.draw(display, (50, 50, 50, 0))
            if main_menu_button.is_over(mpos):
                main_menu_button.draw(display, (255, 255, 255, 100))
            else:
                main_menu_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    gamestate = 'game'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_button.is_over(mpos):
                        main_menu()
                    if continue_button.is_over(mpos):
                        gamestate = 'game'
                    if settings_button.is_over(mpos):
                        gamestate = 'settings'
            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()  # update display

        if gamestate == 'settings':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title, (display.get_width() // 2 - title.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if res_button.is_over(mpos):
                res_button.draw(display, (255, 255, 255, 100))
            else:
                res_button.draw(display, (50, 50, 50, 0))
            if sound_button.is_over(mpos):
                sound_button.draw(display, (255, 255, 255, 100))
            else:
                sound_button.draw(display, (50, 50, 50, 0))
            if back_button.is_over(mpos):
                back_button.draw(display, (255, 255, 255, 100))
            else:
                back_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'pause'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res_button.is_over(mpos):
                        gamestate = 'resolution'
                    if sound_button.is_over(mpos):
                        gamestate = 'sound'
                    if back_button.is_over(mpos):
                        gamestate = 'pause'

                surf = pygame.transform.scale(display, screen.get_size())
                screen.blit(surf, (0, 0))
                pygame.display.update()

        if gamestate == 'resolution':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title_2, (display.get_width() // 2 - title_2.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if res1_button.is_over(mpos):
                res1_button.draw(display, (255, 255, 255, 100))
            else:
                res1_button.draw(display, (50, 50, 50, 0))
            if res2_button.is_over(mpos):
                res2_button.draw(display, (255, 255, 255, 100))
            else:
                res2_button.draw(display, (50, 50, 50, 0))
            if res3_button.is_over(mpos):
                res3_button.draw(display, (255, 255, 255, 100))
            else:
                res3_button.draw(display, (50, 50, 50, 0))
            if res4_button.is_over(mpos):
                res4_button.draw(display, (255, 255, 255, 100))
            else:
                res4_button.draw(display, (50, 50, 50, 0))
            if back_button_2.is_over(mpos):
                back_button_2.draw(display, (255, 255, 255, 100))
            else:
                back_button_2.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res1_button.is_over(mpos):
                        pygame.display.set_mode((600, 400), pygame.RESIZABLE)
                    if res2_button.is_over(mpos):
                        pygame.display.set_mode((900, 600), pygame.RESIZABLE)
                    if res3_button.is_over(mpos):
                        pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
                    if res4_button.is_over(mpos):
                        pygame.display.set_mode((1500, 1000), pygame.RESIZABLE)
                    if back_button.is_over(mpos):
                        gamestate = 'settings'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()

        if gamestate == 'sound':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title_3, (display.get_width() // 2 - title_3.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if sfx_button.is_over(mpos):
                sfx_button.draw(display, (255, 255, 255, 100))
            else:
                sfx_button.draw(display, (50, 50, 50, 0))
            if music_button.is_over(mpos):
                music_button.draw(display, (255, 255, 255, 100))
            else:
                music_button.draw(display, (50, 50, 50, 0))
            if speech_button.is_over(mpos):
                speech_button.draw(display, (255, 255, 255, 100))
            else:
                speech_button.draw(display, (50, 50, 50, 0))
            if back_button_3.is_over(mpos):
                back_button_3.draw(display, (255, 255, 255, 100))
            else:
                back_button_3.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'settings'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sfx_button.is_over(mpos):
                        if sfx_button.text == 'SFX: On':
                            sfx_button.text = 'SFX: Off'
                        else:
                            sfx_button.text = 'SFX: On'
                    if music_button.is_over(mpos):
                        if music_button.text == 'Music: On':
                            music_button.text = 'Music: Off'
                            pygame.mixer.music.set_volume(0)
                        else:
                            music_button.text = 'Music: On'
                            pygame.mixer.music.set_volume(.2)
                    if speech_button.is_over(mpos):
                        if speech_button.text == 'Speech: On':
                            speech_button.text = 'Speech: Off'
                        else:
                            speech_button.text = 'Speech: On'
                    if back_button_3.is_over(mpos):
                        gamestate = 'settings'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()


def minigame3(selected_char, points):
    run = True

    continue_button = engine.Button(display.get_width() // 2 - 110 // 2, 100, 110, 35, sfont, white, 'Continue')
    settings_button = engine.Button(display.get_width() // 2 - 110 // 2, 160, 110, 35, sfont, white, 'Settings')
    main_menu_button = engine.Button(display.get_width() // 2 - 150 // 2, 220, 150, 35, sfont, white, 'Main Menu')
    title = font.render('Settings', True, (255, 255, 255))
    res_button = engine.Button(display.get_width() // 2 - 140 // 2, 100, 140, 25, sfont, white, 'Resolution')
    sound_button = engine.Button(display.get_width() // 2 - 80 // 2, 160, 80, 25, sfont, white, 'Sound')
    back_button = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    title_2 = font.render('Resolution', True, (255, 255, 255))
    res1_button = engine.Button(display.get_width() // 2 - 120 // 2, 100, 120, 25, sfont, white, '600, 400')
    res2_button = engine.Button(display.get_width() // 2 - 120 // 2, 130, 120, 25, sfont, white, '900, 600')
    res3_button = engine.Button(display.get_width() // 2 - 125 // 2, 160, 125, 25, sfont, white, '1200, 800')
    res4_button = engine.Button(display.get_width() // 2 - 130 // 2, 190, 130, 25, sfont, white, '1500, 1000')
    back_button_2 = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    title_3 = font.render('Sound', True, (255, 255, 255))
    back_button_3 = engine.Button(display.get_width() // 2 - 90 // 2, 220, 90, 25, sfont, white, '< Back')
    sfx_button = engine.Button(display.get_width() // 2 - 100 // 2, 100, 100, 25, sfont, white, 'SFX: On')
    music_button = engine.Button(display.get_width() // 2 - 130 // 2, 140, 130, 25, sfont, white, 'Music: On')
    speech_button = engine.Button(display.get_width() // 2 - 130 // 2, 180, 145, 25, sfont, white, 'Speech: On')
    start_button = engine.Button(display.get_width() // 2 - 100 // 2, 270, 100, 25, sfont, (0, 0, 0), 'Start')
    lobby_button = engine.Button(display.get_width() // 2 - 150 // 2, 870, 150, 25, sfont, (0, 0, 0),
                                 'Back to city')
    chair_plus_button = engine.Button(190, 201, 27, 27, sfont, (0, 0, 0), '')
    table_plus_button = engine.Button(352, 201, 27, 27, sfont, (0, 0, 0), '')
    couch_plus_button = engine.Button(516, 200, 27, 27, sfont, (0, 0, 0), '')

    global last_time

    money = points - 600
    if money < 100:
        money = 100

    score = 0

    random_stock = random.randint(8, 15)
    random_stock2 = random.randint(8, 15)
    random_stock3 = random.randint(8, 15)

    tutorial = True
    game_over = False

    global start_time

    counter = 0

    gamestate = 'game'

    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.load("sounds/minigame_music.mp3")
    pygame.mixer.music.play(-1)

    while run:
        if gamestate == 'game':

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            dt = time.time() - last_time
            dt *= 60
            last_time = time.time()

            display.fill((0, 0, 0))
            display.blit(minigame_3_bg, (0, 0))

            timer.tick(60)

            if tutorial:
                pygame.draw.rect(display, (170, 170, 170),
                                 pygame.Rect(display.get_width() // 2 - 450 // 2, 100, 450, 200))
                text = sfont.render('Rules', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 100))
                text = vsfont.render('Time to order and restock!', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 130))
                text = vsfont.render('Click the plus button to buy and restock', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 160))
                text = vsfont.render('The more necessary the purchase, the more points you get', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 190))
                text = vsfont.render('Use all of your furniture allowance. Good Luck!', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 220))
                if start_button.is_over(mpos):
                    start_button.draw(display, (0, 0, 0, 100))
                else:
                    start_button.draw(display, (50, 50, 50, 0))
            if not tutorial:
                money_text = sfont.render('Money to spend: $' + str(money), True, (255, 255, 255))
                display.blit(money_text, (50, 30))
                score_text = sfont.render('Score: ' + str(score), True, (255, 255, 255))
                display.blit(score_text, (450, 30))
                if money < 50:
                    game_over = True

            if game_over:
                pygame.draw.rect(display, (170, 170, 170), pygame.Rect(100, 100, 400, 200))
                text = sfont.render('No more money to spend!', True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 100))
                text = sfont.render('Score: ' + str(score), True, (0, 0, 0))
                display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 150))
                lobby_button.y = 270
                if lobby_button.is_over(mpos):
                    lobby_button.draw(display, (0, 0, 0, 100))
                else:
                    lobby_button.draw(display, (50, 50, 50, 0))

            if not tutorial and not game_over:
                text = stock_font.render('Stock: ' + str(random_stock) + '/20', True, (0, 0, 0))
                display.blit(text, (85, 210))

                text = stock_font.render('Stock: ' + str(random_stock2) + '/20', True, (0, 0, 0))
                display.blit(text, (250, 210))

                text = stock_font.render('Stock: ' + str(random_stock3) + '/20', True, (0, 0, 0))
                display.blit(text, (415, 210))

                if chair_plus_button.is_over(mpos):
                    chair_plus_button.draw(display, (255, 255, 255, 100))
                else:
                    chair_plus_button.draw(display, (50, 50, 50, 0))
                if table_plus_button.is_over(mpos):
                    table_plus_button.draw(display, (255, 255, 255, 100))
                else:
                    table_plus_button.draw(display, (50, 50, 50, 0))
                if couch_plus_button.is_over(mpos):
                    couch_plus_button.draw(display, (255, 255, 255, 100))
                else:
                    couch_plus_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_over(mpos):
                        tutorial = False
                    if lobby_button.is_over(mpos):
                        lobby(selected_char, 3, points + score)
                    if chair_plus_button.is_over(mpos):
                        if random_stock < 20:
                            if money >= 50:
                                money -= 50
                            a = 20 - random_stock
                            a = a * 2
                            score += a
                            random_stock += 1
                    if table_plus_button.is_over(mpos):
                        if random_stock2 < 20:
                            if money >= 50:
                                money -= 50
                            a = 20 - random_stock2
                            a = a * 2
                            score += a
                            random_stock2 += 1
                    if couch_plus_button.is_over(mpos):
                        if random_stock3 < 20:
                            if money >= 50:
                                money -= 50
                            a = 20 - random_stock3
                            a = a * 2
                            score += a
                            random_stock3 += 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'pause'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()

        if gamestate == 'pause':
            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))
            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if continue_button.is_over(mpos):
                continue_button.draw(display, (255, 255, 255, 100))
            else:
                continue_button.draw(display, (50, 50, 50, 0))
            if settings_button.is_over(mpos):
                settings_button.draw(display, (255, 255, 255, 100))
            else:
                settings_button.draw(display, (50, 50, 50, 0))
            if main_menu_button.is_over(mpos):
                main_menu_button.draw(display, (255, 255, 255, 100))
            else:
                main_menu_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    gamestate = 'game'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if main_menu_button.is_over(mpos):
                        main_menu()
                    if continue_button.is_over(mpos):
                        gamestate = 'game'
                    if settings_button.is_over(mpos):
                        gamestate = 'settings'
            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()  # update display

        if gamestate == 'settings':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title, (display.get_width() // 2 - title.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if res_button.is_over(mpos):
                res_button.draw(display, (255, 255, 255, 100))
            else:
                res_button.draw(display, (50, 50, 50, 0))
            if sound_button.is_over(mpos):
                sound_button.draw(display, (255, 255, 255, 100))
            else:
                sound_button.draw(display, (50, 50, 50, 0))
            if back_button.is_over(mpos):
                back_button.draw(display, (255, 255, 255, 100))
            else:
                back_button.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'pause'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res_button.is_over(mpos):
                        gamestate = 'resolution'
                    if sound_button.is_over(mpos):
                        gamestate = 'sound'
                    if back_button.is_over(mpos):
                        gamestate = 'pause'

                surf = pygame.transform.scale(display, screen.get_size())
                screen.blit(surf, (0, 0))
                pygame.display.update()

        if gamestate == 'resolution':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title_2, (display.get_width() // 2 - title_2.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if res1_button.is_over(mpos):
                res1_button.draw(display, (255, 255, 255, 100))
            else:
                res1_button.draw(display, (50, 50, 50, 0))
            if res2_button.is_over(mpos):
                res2_button.draw(display, (255, 255, 255, 100))
            else:
                res2_button.draw(display, (50, 50, 50, 0))
            if res3_button.is_over(mpos):
                res3_button.draw(display, (255, 255, 255, 100))
            else:
                res3_button.draw(display, (50, 50, 50, 0))
            if res4_button.is_over(mpos):
                res4_button.draw(display, (255, 255, 255, 100))
            else:
                res4_button.draw(display, (50, 50, 50, 0))
            if back_button_2.is_over(mpos):
                back_button_2.draw(display, (255, 255, 255, 100))
            else:
                back_button_2.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if res1_button.is_over(mpos):
                        pygame.display.set_mode((600, 400), pygame.RESIZABLE)
                    if res2_button.is_over(mpos):
                        pygame.display.set_mode((900, 600), pygame.RESIZABLE)
                    if res3_button.is_over(mpos):
                        pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
                    if res4_button.is_over(mpos):
                        pygame.display.set_mode((1500, 1000), pygame.RESIZABLE)
                    if back_button.is_over(mpos):
                        gamestate = 'settings'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()

        if gamestate == 'sound':

            display.fill((0, 0, 0))
            display.blit(pause_menu_bg, (0, 0))

            display.blit(title_3, (display.get_width() // 2 - title_3.get_width() // 2, 30))

            w = screen.get_size()[0] / 600
            h = screen.get_size()[1] / 400

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] / w
            mpos[1] = mpos[1] / h

            if sfx_button.is_over(mpos):
                sfx_button.draw(display, (255, 255, 255, 100))
            else:
                sfx_button.draw(display, (50, 50, 50, 0))
            if music_button.is_over(mpos):
                music_button.draw(display, (255, 255, 255, 100))
            else:
                music_button.draw(display, (50, 50, 50, 0))
            if speech_button.is_over(mpos):
                speech_button.draw(display, (255, 255, 255, 100))
            else:
                speech_button.draw(display, (50, 50, 50, 0))
            if back_button_3.is_over(mpos):
                back_button_3.draw(display, (255, 255, 255, 100))
            else:
                back_button_3.draw(display, (50, 50, 50, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gamestate = 'settings'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sfx_button.is_over(mpos):
                        if sfx_button.text == 'SFX: On':
                            sfx_button.text = 'SFX: Off'
                        else:
                            sfx_button.text = 'SFX: On'
                    if music_button.is_over(mpos):
                        if music_button.text == 'Music: On':
                            music_button.text = 'Music: Off'
                            pygame.mixer.music.set_volume(0)
                        else:
                            music_button.text = 'Music: On'
                            pygame.mixer.music.set_volume(.2)
                    if speech_button.is_over(mpos):
                        if speech_button.text == 'Speech: On':
                            speech_button.text = 'Speech: Off'
                        else:
                            speech_button.text = 'Speech: On'
                    if back_button_3.is_over(mpos):
                        gamestate = 'settings'

            surf = pygame.transform.scale(display, screen.get_size())
            screen.blit(surf, (0, 0))
            pygame.display.update()


def game_over_win(score, enemy_score):
    run = True

    main_menu_button = engine.Button(display.get_width() // 2 - 130 // 2, 220, 130, 35, sfont, (0, 0, 0), 'Main Menu')

    while run:
        display.fill((0, 0, 0))
        display.blit(win_screen_bg, (0, 0))

        w = screen.get_size()[0] / 600
        h = screen.get_size()[1] / 400

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0] / w
        mpos[1] = mpos[1] / h

        text = font.render('Congratulations! You Have Won!', True, (0, 0, 0))
        display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 60))
        points_text = sfont.render('Your Score: ' + str(score), True, (0, 240, 0))
        display.blit(points_text, (50, 180))
        enemy_points_text = sfont.render('Enemy Score: ' + str(enemy_score), True, (255, 0, 0))
        display.blit(enemy_points_text, (350, 180))

        if main_menu_button.is_over(mpos):
            main_menu_button.draw(display, (255, 255, 255, 100))
        else:
            main_menu_button.draw(display, (50, 50, 50, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.is_over(mpos):
                    main_menu(True)

        surf = pygame.transform.scale(display, screen.get_size())
        screen.blit(surf, (0, 0))
        pygame.display.update()


def game_over_lose(score, enemy_score):
    run = True

    main_menu_button = engine.Button(display.get_width() // 2 - 130 // 2, 260, 130, 35, sfont, (0, 0, 0), 'Main Menu')

    while run:
        display.fill((0, 0, 0))
        display.blit(lose_screen_bg, (0, 0))

        w = screen.get_size()[0] / 600
        h = screen.get_size()[1] / 400

        mpos = list(pygame.mouse.get_pos())
        mpos[0] = mpos[0] / w
        mpos[1] = mpos[1] / h

        text = font.render('Game Over! You Have Lost!', True, (0, 0, 0))
        display.blit(text, (display.get_width() // 2 - text.get_width() // 2, 60))
        points_text = sfont.render('Your Score: ' + str(score), True, (0, 240, 0))
        display.blit(points_text, (50, 180))
        enemy_points_text = sfont.render('Enemy Score: ' + str(enemy_score), True, (255, 0, 0))
        display.blit(enemy_points_text, (350, 180))

        if main_menu_button.is_over(mpos):
            main_menu_button.draw(display, (255, 255, 255, 100))
        else:
            main_menu_button.draw(display, (50, 50, 50, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.is_over(mpos):
                    main_menu(True)

        surf = pygame.transform.scale(display, screen.get_size())
        screen.blit(surf, (0, 0))
        pygame.display.update()


# the thing that will run the whole game
main_menu()
