#!/usr/bin/python3

import pygame
import sys
import os
import random
import time

from pygame.locals import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS # PyInstaller creates a temp folder and stores path in _MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

bricks_x = 10 # numbered 0-(N-1), with zero on left
bricks_y = 20 # two extra invisible rows, so numbered 0-(N+1), with 0,1 being invisible rows on top
brick_pixels_x = 40
brick_pixels_y = 30
banner_height = 34
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load(resource_path("tetris.mp3"))
pygame.key.set_repeat(300, 50)

font = pygame.font.Font(resource_path("modern-tetris.ttf"), 48)
pygame.display.set_icon(pygame.image.load(resource_path("tetris_icon.png")))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((bricks_x * brick_pixels_x,
                                  bricks_y * brick_pixels_y + banner_height))

bg = pygame.transform.scale(pygame.image.load(resource_path("tetris.png")),
                            (bricks_x * brick_pixels_x,
                             bricks_y * brick_pixels_y + banner_height)).convert()

brick_images = list()
for i in range(1,8):
    bi = pygame.transform.scale(pygame.image.load(resource_path("brick_%d.png" % i)),
                                (brick_pixels_x,
                                 brick_pixels_y)).convert()
    brick_images.append(bi)

pygame.mouse.set_visible(0)
pygame.display.set_caption('Simon\'s Tetris')
pygame.event.set_allowed([QUIT, KEYDOWN])

# setup the types of brick, from https://tetris.fandom.com/wiki/SRS
brick_types = [
    { "maps" : [ [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
                 [[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]],
                 [[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]],
                 [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]] ],
    },
    { "maps" : [ [[2,0,0],[2,2,2],[0,0,0]],
                 [[0,2,2],[0,2,0],[0,2,0]],
                 [[0,0,0],[2,2,2],[0,0,2]],
                 [[0,2,0],[0,2,0],[2,2,0]] ],
    },
    { "maps" : [ [[0,0,3],[3,3,3],[0,0,0]],
                 [[0,3,0],[0,3,0],[0,3,3]],
                 [[0,0,0],[3,3,3],[3,0,0]],
                 [[3,3,0],[0,3,0],[0,3,0]] ],
    },
    { "maps" : [ [[0,4,4,0],[0,4,4,0],[0,0,0,0]],
                 [[0,4,4,0],[0,4,4,0],[0,0,0,0]],
                 [[0,4,4,0],[0,4,4,0],[0,0,0,0]],
                 [[0,4,4,0],[0,4,4,0],[0,0,0,0]] ],
    },
    { "maps" : [ [[0,5,5],[5,5,0],[0,0,0]],
                 [[0,5,0],[0,5,5],[0,0,5]],
                 [[0,0,0],[0,5,5],[5,5,0]],
                 [[5,0,0],[5,5,0],[0,5,0]] ],
    },
    { "maps" : [ [[0,6,0],[6,6,6],[0,0,0]],
                 [[0,6,0],[0,6,6],[0,6,0]],
                 [[0,0,0],[6,6,6],[0,6,0]],
                 [[0,6,0],[6,6,0],[0,6,0]] ],
    },
    { "maps" : [ [[7,7,0],[0,7,7],[0,0,0]],
                 [[0,0,7],[0,7,7],[0,7,0]],
                 [[0,0,0],[7,7,0],[0,7,7]],
                 [[0,7,0],[7,7,0],[7,0,0]] ],
    },
]

# https://tetris.fandom.com/wiki/SRS
wall_kick_types = [ 1, 0, 0, 2, 0, 0, 0 ] # I=1, O=2, others=0

wall_kicks_by_type = [
    # type 0
    [
        [ [ 0, 0], [-1, 0], [-1, 1], [ 0,-2], [-1,-2] ], # 0 +1
        [ [ 0, 0], [ 1, 0], [ 1, 1], [ 0,-2], [ 1,-2] ], # 0 -1
        [ [ 0, 0], [ 1, 0], [ 1,-1], [ 0, 2], [ 1, 2] ], # 1 +1
        [ [ 0, 0], [ 1, 0], [ 1,-1], [ 0, 2], [ 1, 2] ], # 1 -1
        [ [ 0, 0], [ 1, 0], [ 1, 1], [ 0,-2], [ 1,-2] ], # 2 +1
        [ [ 0, 0], [-1, 0], [-1, 1], [ 0,-2], [-1,-2] ], # 2 -1
        [ [ 0, 0], [-1, 0], [-1,-1], [ 0, 2], [-1, 2] ], # 3 +1
        [ [ 0, 0], [-1, 0], [-1,-1], [ 0, 2], [-1, 2] ], # 3 -1
    ],
    # type 1
    [
        [ [ 0, 0], [-2, 0], [ 1, 0], [-2,-1], [ 1, 2] ], # 0 +1
        [ [ 0, 0], [-1, 0], [ 2, 0], [-1, 2], [ 2,-1] ], # 0 -1
        [ [ 0, 0], [-1, 0], [ 2, 0], [-1, 2], [ 2,-1] ], # 1 +1
        [ [ 0, 0], [ 2, 0], [-1, 0], [ 2, 1], [-1,-2] ], # 1 -1
        [ [ 0, 0], [ 2, 0], [-1, 0], [ 2, 1], [-1,-2] ], # 2 +1
        [ [ 0, 0], [ 1, 0], [-2, 0], [ 1,-2], [-2, 1] ], # 2 -1
        [ [ 0, 0], [ 1, 0], [-2, 0], [ 1,-1], [-2, 1] ], # 3 +1
        [ [ 0, 0], [-2, 0], [ 1, 0], [-2,-1], [ 1, 2] ], # 3 -1
    ],
    # type 2
    [
        [ [ 0, 0] ], # 0 +1
        [ [ 0, 0] ], # 0 -1
        [ [ 0, 0] ], # 1 +1
        [ [ 0, 0] ], # 1 -1
        [ [ 0, 0] ], # 2 +1
        [ [ 0, 0] ], # 2 -1
        [ [ 0, 0] ], # 3 +1
        [ [ 0, 0] ], # 3 -1
    ]
]

colors = [
    [  0,  0,  0,  0], # 0: no color
    [  0,255,255,255], # 1: cyan
    [  0,  0,255,255], # 2: blue
    [255,127,  0,255], # 3: orange
    [255,255,  0,255], # 4: yellow
    [  0,255,  0,255], # 5: green
    [127,  0,127,255], # 6: purple
    [255,  0,  0,255], # 7: red
    [255,255,255,255], # 8: white
    [  0,  0,  0,255], # 9: black
]

# from https://tetris.fandom.com/wiki/Tetris_(NES,_Nintendo)
level_shift_time = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5,
                    4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]

def main():
    global running
    global show_help
    show_help = True
    while True:
        # show help screen
        running = True
        while (show_help and running):
            clock.tick(10)
            iter_help()
        # run game
        init_game()
        pygame.mixer.music.play()
        running = True
        while (running):
            clock.tick(50)
            iter_game()
            pygame.display.update()
            if (pygame.mixer.music.get_pos() >= 38100):
                pygame.mixer.music.play()
                
        # show game over screen
        pygame.mixer.music.fadeout(3)
        running = True
        while (running):
            clock.tick(10)
            iter_done()


def init_game():
    global static_map
    global active_brick
    global brick_bag
    global shift_time
    global shift_count
    global shift_fast
    global close_counts
    global last_was_tetris
    global score
    global level
    global lines
    global paused
    static_map = [[0 for x in range(bricks_x)] for y in range(bricks_y+2)]
    brick_bag = list()
    active_brick = { "type" : -1, "orientation" : 0, "pos_x" : 0, "pos_y" : 0 }
    shift_time = level_shift_time[0]
    shift_count = 0
    shift_fast = 0
    close_counts = [0 for x in range(bricks_y+2)]
    last_was_tetris = False
    score = 0
    level = 0
    lines = 0
    paused = 0
        
def iter_help():
    global running
    global show_help

    # check for user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_s):
                running = False
                show_help = False
            if (event.key == pygame.K_q):
                sys.exit(0)
    # draw screen background
    screen.blit(bg, (0, 0))

    # draw help screen
    draw_text("Simon's Tetris",
              (brick_pixels_x * 0.2), (brick_pixels_y * 3),
              (brick_pixels_x * 9.8), (brick_pixels_y * 2))
    line_pointer = (brick_pixels_y * 8)
    line_size = brick_pixels_y
    key_pos = (brick_pixels_x * 0.8)
    txt_pos = (brick_pixels_x * 5)
    draw_text("Left", key_pos, line_pointer)
    draw_text("Move Left", txt_pos, line_pointer)
    line_pointer += line_size
    draw_text("Right", key_pos, line_pointer)
    draw_text("Move Right", txt_pos, line_pointer)
    line_pointer += line_size
    draw_text("Z", key_pos, line_pointer)
    draw_text("Rotate CCW", txt_pos, line_pointer)
    line_pointer += line_size
    draw_text("X, Up", key_pos, line_pointer)
    draw_text("Rotate CW", txt_pos, line_pointer)
    line_pointer += line_size
    draw_text("Space, Down", key_pos, line_pointer)
    draw_text("Fast Drop", txt_pos, line_pointer)
    line_pointer += line_size
    line_pointer += line_size
    draw_text("S", key_pos, line_pointer)
    draw_text("Start", txt_pos, line_pointer)
    line_pointer += line_size
    draw_text("P", key_pos, line_pointer)
    draw_text("Pause", txt_pos, line_pointer)
    line_pointer += line_size
    draw_text("Q", key_pos, line_pointer)
    draw_text("Quit", txt_pos, line_pointer)

    pygame.display.update()
        
def iter_done():
    global running
    global show_help
    # check for user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_h):
                running = False
                show_help = True
            if (event.key == pygame.K_s):
                running = False
                show_help = False
            if (event.key == pygame.K_q):
                sys.exit(0)
    # show game over

    draw_text("Game Over,",
              (brick_pixels_x*(bricks_x-8)/2), (brick_pixels_y * 5),
              (brick_pixels_x * 8), (brick_pixels_y * 3))

    draw_text("Comrade!",
              (brick_pixels_x*(bricks_x-8)/2), (brick_pixels_y * 9),
              (brick_pixels_x * 8), (brick_pixels_y * 3),
              (255,0,0))
    
    line_pointer = (brick_pixels_y * 13)
    line_size = brick_pixels_y
    key_pos = (brick_pixels_x * 0.8)
    txt_pos = (brick_pixels_x * 5)
    draw_text("H", key_pos, line_pointer)
    draw_text("Help Menu", txt_pos, line_pointer)
    line_pointer += line_size
    draw_text("S", key_pos, line_pointer)
    draw_text("Start", txt_pos, line_pointer)
    line_pointer += line_size
    draw_text("Q", key_pos, line_pointer)
    draw_text("Quit", txt_pos, line_pointer)

    pygame.display.update()


def iter_game():
    global running
    global paused
    global brick_bag
    global active_brick
    global shift_count
    global shift_fast
    global shift_time
    global close_counts
    global last_was_tetris
    global score
    global level
    global lines

    # check if we are starting a new brick
    if (active_brick["type"] == -1):
        # we need to choose a brick
        if (len(brick_bag)==0):
            # we need to populate the brick bag
            brick_bag = [ 0, 1, 2, 3, 4, 5, 6 ]
            random.shuffle(brick_bag)
        # pick next brick from bag
        active_brick["type"] = brick_bag.pop(0)
        active_brick["orientation"] = 0
        active_brick["pos_x"] = int((bricks_x / 2)-1)
        active_brick["pos_y"] = 1
        collision = 1
        while (collision and active_brick["pos_y"] >= 0):
            # check to see if it can be spawned here
            collision = 0
            temp_map = brick_types[active_brick["type"]]["maps"][active_brick["pos_y"]]
            for col in range(len(temp_map)):
                for row in range(len(temp_map)):
                    if ((collision==0) and (temp_map[row][col]>0)):
                        if (static_map [row+active_brick["pos_y"]] [col+active_brick["pos_x"]]):
                            collision = 1
            if (collision):
                active_brick["pos_y"] -= 1
        if (active_brick["pos_y"] < 0):
            # cannot spawn, game over
            running = False
        
    # check for user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            check_shift = 0
            check_rotate = 0
            if (event.key == pygame.K_q):
                sys.exit(0)
            elif (event.key == pygame.K_p):
                paused = (paused ^ 1)
            elif (event.key == pygame.K_LEFT):
                do_shift = -1 
                check_shift = 1
            elif (event.key == pygame.K_RIGHT):
                do_shift = 1 
                check_shift = 1
            elif ((event.key == pygame.K_x) or
                  (event.key == pygame.K_UP)):
                do_rotate = 0 # clockwise
                check_rotate = 1
            elif (event.key == pygame.K_z):
                do_rotate = 1 # counter-clockwise
                check_rotate = 1
            elif ((event.key == pygame.K_SPACE) or
                  (event.key == pygame.K_DOWN)):
                if (shift_fast == 0):
                    shift_fast = 1
                    score += (bricks_y + 2 - active_brick["pos_y"])
            if (check_shift):
                new_x = active_brick["pos_x"] + do_shift
                collision = check_collision(active_brick["orientation"], new_x, active_brick["pos_y"])
                if (collision == 0):
                    active_brick["pos_x"] = new_x
            elif (check_rotate):
                if (do_rotate): # counter-clockwise
                    new_o = active_brick["orientation"] - 1
                    if (new_o == -1):
                        new_o = 3
                else: # clockwise
                    new_o = active_brick["orientation"] + 1
                    if (new_o == 4):
                        new_o = 0
                wall_kick_type = wall_kick_types[active_brick["type"]]
                wall_kick_index = (active_brick["orientation"]<<1)+do_rotate
                wall_kicks = wall_kicks_by_type[wall_kick_type][wall_kick_index]
                for kick in wall_kicks:
                    try_x = active_brick["pos_x"] + kick[0]
                    try_y = active_brick["pos_y"] - kick[1]
                    collision = check_collision(new_o, try_x, try_y)
                    if (collision==0):
                        active_brick["pos_x"] = try_x
                        active_brick["pos_y"] = try_y
                        active_brick["orientation"] = new_o
                        break
                
    if paused:
        return

    # check if we are moving active brick down
    shift_count += 1
    if (shift_fast or (shift_count >= shift_time)):
        active_brick["pos_y"] += 1
        shift_count = 0

    # draw screen background
    screen.blit(bg, (0, 0))

    # draw score
    draw_text("Level:",           (brick_pixels_x*0.2), (brick_pixels_y*0.2))
    draw_text("%d" % (level),     (brick_pixels_x*2.5), (brick_pixels_y*0.2))
    draw_text("Score:",           (brick_pixels_x*3.8), (brick_pixels_y*0.2))
    draw_text("%d" % (score),     (brick_pixels_x*6.1), (brick_pixels_y*0.2))

    # grab a map of the current brick and orientation, we will use this a lot
    temp_map = brick_types[active_brick["type"]]["maps"][active_brick["orientation"]]

    # check to see if brick has hit something
    hit = 0
    for col in range(len(temp_map)):
        for row in range(len(temp_map)):
            if (temp_map[row][col]):
                # check to see if we've hit the bottom of the screen
                if ((row + active_brick["pos_y"]) > (bricks_y+1)):
                    hit = 1
                # check to see if we've hit something in the map
                elif (static_map [row + active_brick["pos_y"]] [col + active_brick["pos_x"]] ):
                    hit = 1

    if (hit): 
        active_brick["pos_y"] -= 1 # we've gone too far down, so we back up a row before locking
        for col in range(len(temp_map)):
            for row in range(len(temp_map)):
                if (temp_map[row][col]):
                    static_map [row+active_brick["pos_y"]] [col + active_brick["pos_x"]] = temp_map[row][col]
        active_brick["type"] = -1 # this indicates that there is no longer an active brick
        shift_fast = 0
    else:
        for col in range(len(temp_map)):
            for row in range(len(temp_map)):
                if (temp_map[row][col]):
                    draw_box(col + active_brick["pos_x"],
                             row + active_brick["pos_y"],
                             temp_map[row][col])
        
    # check for closing row
    closed = 0
    for row in range(bricks_y+1,1,-1):
        if (close_counts[row]==0):
            needs_closing = 1
            for col in range(bricks_x):
                if (static_map[row][col] == 0):
                    needs_closing = 0
            if (needs_closing):
                close_counts[row] = shift_time
                closed += 1
    if (closed):
        lines += closed
        if (closed==1):
            base_score = 100
            last_was_tetris = False
        elif (closed==2):
            base_score = 300
            last_was_tetris = False
        elif (closed==3):
            base_score = 500
            last_was_tetris = False
        else: # tetris
            base_score = 1200 if last_was_tetris else 800
            last_was_tetris = True
        score += (base_score * (level+1))
        if (lines >= ((level+1)*10)):
            if (level < 29):
                level += 1
                shift_time = level_shift_time[level]

    # flash closing row
    for close_row in range(bricks_y+1,1,-1):
        if (close_counts[close_row]):
            color = 8 + ((close_counts[close_row]>>2) & 1)
            for col in range(bricks_x):
                static_map[close_row][col] = color
            close_counts[close_row] -= 1
            if (close_counts[close_row] == 0):
                # done flashing the row, shift them down
                for row in range(close_row,1,-1):
                    for col in range(bricks_x):
                        static_map[row][col] = static_map[row-1][col]
                    close_counts[row] = close_counts[row-1]

    # draw static map
    for col in range(bricks_x):
        for row in range(2,bricks_y+2):
            if (static_map[row][col]):
                draw_box(col,row,static_map[row][col])


def check_collision(o, x, y):
    temp_map = brick_types[active_brick["type"]]["maps"][o]
    collision = 0
    for col in range(len(temp_map)):
        if collision:
            break
        for row in range(len(temp_map)):
            if collision:
                break
            elif (temp_map[row][col]>0):
                if ((col + x) < 0):
                    collision = 1
                elif ((col + x) > (bricks_x-1)):
                    collision = 1
                elif ((row + y) > (bricks_y+1)):
                    collision = 1
                elif (static_map [row + y] [col + x]):
                    collision = 1
    return collision

def draw_text(txt, x, y, size_x = -1, size_y = (brick_pixels_y*0.8), color=(255,255,255)):
    if (size_x == -1): size_x = (brick_pixels_x * 0.35 * len(txt))
    screen.blit(pygame.transform.scale(font.render(txt, True, (0,0,0)),
                                       (size_x, size_y)),
                (x+(size_y*0.10), y+(size_y*0.10)))
    screen.blit(pygame.transform.scale(font.render(txt, True, color),
                                       (size_x, size_y)),
                (x, y))

def draw_box (x, y, c):
    if (y>=2): # i.e. we only know 2-21 if bricks_y==20
        if (c<8):
            screen.blit(brick_images[c-1], (x*brick_pixels_x,
                                            (y-2)*brick_pixels_y + banner_height))
        else:
            screen.fill(colors[c], [x*brick_pixels_x + 2,
                                    (y-2)*brick_pixels_y + banner_height,
                                    brick_pixels_x-2,
                                    brick_pixels_y-2])

                                

main()        
