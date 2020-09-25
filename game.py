import pygame as pg
import numpy as np
from enum import Enum
import itertools
import time

# make constants
# size of each square in pixels
box_size = 20
# dimensions in boxes
width, height = 50, 40
screen_dimensions = (width*box_size, height*box_size)
screen = pg.display.set_mode(screen_dimensions)
line_color = (100, 100, 100)
# in milliseconds
tick_time = 250

# the mode we're currently in, whether we're placing or watching it go
Mode = Enum('Mode', 'place simulate')
curr_mode = Mode.place

# create the box array. each element will be a true or false, depending on if it has a square
boxes = np.zeros(shape=(width, height)).astype(np.bool)
boxes_orig = boxes.copy()

# returns a grid surface, with the squares colored in appropriately
def create_grid():
    grid = pg.Surface(screen_dimensions)
    for index, box in np.ndenumerate(boxes):
        if box:
            box_rect = pg.Rect((index[0] * box_size, index[1] * box_size), (box_size,)*2)
            pg.draw.rect(grid, (255, 255, 255), box_rect)
    for x in range(0, width):
        pg.draw.line(grid, line_color, start_pos=(x*box_size, 0), end_pos=(x*box_size, screen_dimensions[1]-1))
        pg.draw.line(grid, line_color, ((x+1)*box_size-1, 0), ((x+1)*box_size-1, screen_dimensions[1]-1))
    for y in range(0, height):
        pg.draw.line(grid, line_color, start_pos=(0, y*box_size), end_pos=(screen_dimensions[0]-1, y*box_size))
        pg.draw.line(grid, line_color, (0, (y+1)*box_size-1), (screen_dimensions[0]-1, (y+1)*box_size-1))
    return grid


# returns the amount of neighbors for a given grid
def get_neighbors(x, y):
    neighbor_sum = 0
    offset_list = {-1, 0, 1}
    for (x_offset, y_offset) in itertools.product(offset_list, offset_list):
        new_x = x + x_offset
        new_y = y + y_offset
        if not (x_offset == 0 and y_offset == 0) and new_x < width and new_y < height and boxes[new_x, new_y]:
            neighbor_sum += 1
    return neighbor_sum


# what to do every tick logic-wise, and returns the new boxes array
def logic_tick():
    neighbors = np.zeros((width, height))
    for index, box in np.ndenumerate(boxes):
        neighbor_count = get_neighbors(*index)
        neighbors[index] = neighbor_count == 3 or (neighbor_count == 2 and boxes[index])
    return neighbors.copy()


# set up PyGame
pg.init()

# game loop
needs_to_update = True
timer_start = time.time()
while True:
    # tick
    if curr_mode == Mode.simulate:
        time_surpassed = (time.time() - timer_start) * 1000
        if time_surpassed >= tick_time:
            boxes = logic_tick()
            needs_to_update = True
            timer_start = time.time()

    if needs_to_update:
        screen.fill(0)
        grid = create_grid()
        screen.blit(grid, (0, 0))
        needs_to_update = False

    # update screen
    pg.display.flip()

    # inputs
    for event in pg.event.get():
        # check if user wants to exit
        if event.type == pg.QUIT:
            pg.quit()
            exit(0)
        # check if the user is changing modes or quitting
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                pg.quit()
                exit(0)
            if event.key == pg.K_p:
                curr_mode = Mode.place
                boxes = boxes_orig.copy()
                needs_to_update = True
            elif event.key == pg.K_s:
                curr_mode = Mode.simulate
                boxes = boxes_orig.copy()
                timer_start = time.time()
                needs_to_update = True
        # check if user clicked in box
        if curr_mode == Mode.place and event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            x_coord = int(x / box_size)
            y_coord = int(y / box_size)
            boxes[x_coord, y_coord] = not boxes[x_coord, y_coord]
            boxes_orig[x_coord, y_coord] = not boxes_orig[x_coord, y_coord]
            needs_to_update = True
