import pygame
from time import sleep
import numpy as np
import matplotlib.pyplot as plt


def write(text, size, x, y, color):
    font = pygame.font.SysFont("comicsansms", size)
    label = font.render(text, 1, pygame.Color(color))
    screen.blit(label, (x,y))

pygame.init()

width, height, menuH = 550, 550, 150
size = width, height + menuH
bg = 25, 25, 25

screen = pygame.display.set_mode(size)
screen.fill(bg)

n_cx = 30
n_cy = 30

dimW_cell = (width - 1)  / n_cx
dimH_cell = (height - 1) / n_cy

game_state = np.zeros((n_cx, n_cy))
pause = True
while True:

    screen.fill(bg)
    
    write("Welcome to Conway's Game of Life", 25, 10, 10, "White")
    write("Rules: ", 15, 10, 45, "White")
    rule1 = "Any dead cell with three live neighbors becomes a live cell"
    rule2 = "Any live cell with two or three live neighbors survives, otherwise, die."
    write(rule1, 12, 30, 65, "White")
    write(rule2, 12, 30, 80, "White")
    write("Instructions:", 15, 10, 102, "White")
    instructions = "Left click creates a cell, right click kills a cell, middle click kills all cells"
    write(instructions, 12, 30, 118, "White")

    game_state_copy = np.copy(game_state)

    for y in range(0, n_cy ):
        for x in range(0, n_cx):
            
            if not pause:
                neighbors = np.sum([game_state[(x-1) % n_cx, (y - 1) % n_cy],
                game_state[(x) % n_cx, (y - 1) % n_cy],
                game_state[(x+1) % n_cx, (y - 1) % n_cy],
                game_state[(x-1) % n_cx, (y) % n_cy],
                game_state[(x+1) % n_cx, (y) % n_cy],
                game_state[(x-1) % n_cx, (y +1) % n_cy],
                game_state[(x) % n_cx, (y + 1) % n_cy],
                game_state[(x+1) % n_cx, (y + 1) % n_cy]])
                
                #Any dead cell with three live neighbors becomes a live cell.
                if game_state[x, y] == 0 and neighbors == 3:
                    game_state_copy[x,y] = 1

                #Any live cell with two or three live neighbors survives, otherwise, die.
                elif game_state[x, y] == 1 and                          (neighbors < 2 or neighbors >3):
                    game_state_copy[x,y] = 0

            polygon = [
                ((x)*dimW_cell, (y)*dimH_cell + menuH),
                ((x +1) * dimW_cell, (y)*dimH_cell + menuH),
                ((x +1) * dimW_cell, (y +1)*dimH_cell + menuH),
                ((x )*dimW_cell, (y +1)*dimH_cell + menuH)
            ]
            border = int(abs(1-game_state_copy[x,y]))
            pygame.draw.polygon(screen, (255, 255, 255), polygon, border)
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            pause = not pause
        
        click = pygame.mouse.get_pressed()

        if sum(click) > 0:
            pos_x, pos_y = pygame.mouse.get_pos()
            cell_x = int( np.floor(pos_x / dimW_cell)) 
            cell_y = int( np.floor((pos_y - menuH)/ dimH_cell)) 
            if click[0]:
                game_state_copy[cell_x, cell_y] = 1
            elif click[2]:
                game_state_copy[cell_x, cell_y] = 0
            else:
                game_state_copy = np.zeros((n_cx, n_cy))
    game_state = game_state_copy

    pygame.display.update()
    sleep(0.05)


    
        
