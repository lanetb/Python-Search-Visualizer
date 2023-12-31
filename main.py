import pygame, pygame_widgets, sys, queue
from collections import deque
from tkinter import messagebox, Tk
from algos import dijk, a_star, manhatten_heuristic, euclidean_heuristic
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button
from itertools import count
from maze import create_maze
import sys

sys.setrecursionlimit(5000)

# Initialize pygame
size = (width, height) = (860, (480+25))
pygame.init()

# Create screen
win = pygame.display.set_mode(size)
pygame.display.set_caption("Pathfinding")
clock = pygame.time.Clock()

cols, rows = 86*2, 48*2
w = width // cols
h = (height - 25) // rows  # Subtract 50 for the GUI bar

grid = []
que = deque()
p_que = queue.PriorityQueue()
path = []

# Define GUI variables
gui_height = 25
gui_color = (200, 200, 200)

dropdown = Dropdown(
    win, 5, 2.5, 150, 15, name='Select Algorithm \/',
    choices=[
        'Dijkstra',
        'A*',
    ],
    borderRadius=0, borderThickness = 10, borderColour = pygame.Color("Black"), 
    inactiveColour=pygame.Color('white'), values=["Dijkstra", "A*"], direction='down', 
    textHAlign='left',
)

dropdown2 = Dropdown(
    win, 160, 2.5, 150, 15, name='Select Heristic \/',
    choices=[
        'Manhatten',
        'Euclidean',
    ],
    borderRadius=0, borderThickness = 10, borderColour = pygame.Color("Black"), 
    inactiveColour=pygame.Color('white'), values=["manhatten", "euclidean"], direction='down', 
    textHAlign='left',
)

# Creates the grid
class Box:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.neighbors = []
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbors = []
        self.prior = None
        self.f_cost, self.g_cost, self.h_cost = 0, 0, 0

    def draw(self, win, color, shape=True):
        if shape:
            pygame.draw.rect(win, color, (self.x * w, self.y * h + gui_height, w-2, h-2))
        else:
            pygame.draw.circle(win, color, (self.x * w + w // 2.5, self.y * h + h // 2.5 + gui_height), w // 3)

    def set_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

    def get_cost(self):
        return self.cost

# ... (rest of your Box class)

for col in range(cols):
    arr = []
    for row in range(rows):
        arr.append(Box(col, row))
    grid.append(arr)

for col in range(cols):
    for row in range(rows):
        grid[col][row].set_neighbors()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
unique = count(0,-1)
que.append(start_box)
p_que.put((0, next(unique), start_box))
heristic = "manhatten"
algorithm_type = "A*"

def rest_p_que():
    while not p_que.empty():
        p_que.get()
    p_que.put((0, next(unique), start_box))

# Main loop
def main():
    begin_search = False
    target_box_set = False
    target_box = None
    searching = True
    running = True

    def reset_begin_search():
        nonlocal begin_search
        begin_search = False

    def reset_searching():
        nonlocal searching
        searching = True

    def reset_search():
        reset_searching()
        reset_begin_search()
        path.clear()
        que.clear()
        que.append(start_box)
        rest_p_que()
        for col in range(cols):
            for row in range(rows):
                if not grid[col][row].wall:
                    grid[col][row].visited = False
                    grid[col][row].queued = False
                    grid[col][row].prior = None
                    grid[col][row].f_cost = 0
                    grid[col][row].g_cost = 0
                    grid[col][row].h_cost = 0    

    def reset_full():
        reset_search()
        nonlocal target_box_set
        target_box_set = False
        nonlocal target_box
        target_box = None
        for col in range(cols):
            for row in range(rows):
                grid[col][row].wall = False
                grid[col][row].target = False
        start_box.start = True
        start_box.visited = True 
    
    def start_search():
        if target_box_set:
            nonlocal heristic
            heristic=dropdown2.getSelected()
            match heristic:
                case "manhatten":
                    start_box.cost_f, start_box.cost_h = manhatten_heuristic(start_box, target_box), manhatten_heuristic(start_box, target_box)
                case "euclidean":
                    start_box.cost_f, start_box.cost_h = euclidean_heuristic(start_box, target_box), euclidean_heuristic(start_box, target_box)
            nonlocal begin_search
            begin_search = True

    button = Button(
        win, 640, 2.5, 100, 15, text='reset search',
        inactiveColour=pygame.Color('red'), hoverColour=pygame.Color('darkred') ,pressedColour=pygame.Color('red'),
        onClick=lambda: reset_search(),
    )

    button2 = Button(
        win, 745, 2.5, 100, 15, text='reset full',
        inactiveColour=pygame.Color('red'), hoverColour=pygame.Color('darkred') ,pressedColour=pygame.Color('red'),
        onClick=lambda: reset_full(),
    )

    button3 = Button(
        win, 535, 2.5, 100, 15, text='start search',
        inactiveColour=pygame.Color('green'), hoverColour=pygame.Color('darkgreen') ,pressedColour=pygame.Color('green'),
        onClick=lambda: start_search(),
    )

    button4 = Button(
            win, 430, 2.5, 100, 15, text='create maze',
            inactiveColour=pygame.Color('blue'), hoverColour=pygame.Color('darkblue') ,pressedColour=pygame.Color('blue'),
            onClick=lambda x, y,z, a: (set_running(z), reset_full(), create_maze(x, y), set_running(a)), onClickParams=(grid, win, False, True),
    )

    def set_running(var):
        nonlocal running
        running = var
    
    while running:
        algorithm_type = dropdown.getSelected()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                if event.buttons[0] and x < width and x > 0 and y < height and y > gui_height:
                    i = x // w
                    j = (y - gui_height) // h
                    grid[i][j].wall = True
                if event.buttons[2] and not target_box_set and x < width and x > 0 and y < height and y > gui_height:
                    i = x // w
                    j = (y - gui_height) // h
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            elif event.type == pygame.KEYDOWN and target_box_set:
                heristic=dropdown2.getSelected()
                match heristic:
                    case "manhatten":
                        start_box.cost_f, start_box.cost_h = manhatten_heuristic(start_box, target_box), manhatten_heuristic(start_box, target_box)
                    case "euclidean":
                        start_box.cost_f, start_box.cost_h = euclidean_heuristic(start_box, target_box), euclidean_heuristic(start_box, target_box)
                if event.key == pygame.K_SPACE:
                    begin_search = True
        if begin_search:
            match algorithm_type:
                case "Dijkstra": 
                        if len(que) > 0 and searching:
                                searching = dijk(grid, que, target_box, path, start_box)          
                        else:
                            if searching:
                                Tk().wm_withdraw()
                                messagebox.showinfo("Path Not Found", "There was no path to the target box")
                                searching = False
                case "A*":
                        if not p_que.empty() and searching:
                                searching = a_star(grid, p_que, unique, target_box, start_box, path, heristic)         
                        else:
                            if searching:
                                Tk().wm_withdraw()
                                messagebox.showinfo("Path Not Found", "There was no path to the target box")
                                searching = False

        win.fill((0, 0, 0))

        for col in range(cols):
            for row in range(rows):
                box = grid[col][row]
                box.draw(win, (20, 20, 20))
                if box.queued:
                    box.draw(win, (200, 150, 150), False)
                if box.visited:
                    box.draw(win, (0, 255, 150))
                if box.wall:
                    box.draw(win, (75, 75, 75))
                if box in path:
                    box.draw(win, (0, 150, 250))
                if box.start:
                    box.draw(win, (0, 200, 200))
                if box.target:
                    box.draw(win, (200, 200, 0))
        # Draw GUI
        pygame.draw.rect(win, gui_color, (0, 0, width, gui_height-5))
        pygame_widgets.update(events)

        pygame.display.flip()

main()