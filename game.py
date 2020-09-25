import pygame as pg
import numpy as np

# make constants
# size of each square in pixels
box_size = 20
# dimensions in boxes
width, height = 50, 40
screen_dimensions = (width*box_size, height*box_size)
screen = pg.display.set_mode(screen_dimensions)
line_color = (100, 100, 100)
# in milliseconds
tick_time = 500

# create the box array. each element will be a true or false, depending on if it has a square
boxes = np.zeros(shape=(width, height)).astype(np.bool)

# returns a grid surface, with the squares colored in appropriately
def create_grid():
    grid = pg.Surface(screen_dimensions)
    print(boxes)
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


# set up PyGame
pg.init()

# game loop
needs_to_update = True
while True:
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
        # check if user clicked in box
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            x_coord = int(x / box_size)
            y_coord = int(y / box_size)
            needs_to_update = True
            boxes[x_coord, y_coord] = not boxes[x_coord, y_coord]
