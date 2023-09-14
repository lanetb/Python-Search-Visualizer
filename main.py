import pygame, sys, random, math #pygame and module systems
from collections import deque
from tkinter import messagebox, Tk #allows for small dialog boxes to be created
from algos import dijk

# Initialize pygame
size = (width, height) = (850, 480) #width and height of the screen
pygame.init() #initializes pygame

# Create screen
win = pygame.display.set_mode(size)
pygame.display.set_caption("Pathfinding")
clock = pygame.time.Clock()

cols, rows = 85, 48

w = width // cols
h = height // rows

grid = []
queue = deque()
path = []

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

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * w, self.y * h, w-2, h-2))

    def set_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

#creates the grid
for col in range(cols):
    arr=[]
    for row in range(rows):
        arr.append(Box(col, row))
    grid.append(arr)

#Sets the neighbors for each box
for col in range(cols):
    for row in range(rows):
        grid[col][row].set_neighbors()

#creates the start box
start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
     #main method houses the main loop
    while True:
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse interaction
            elif event.type == pygame.MOUSEMOTION: #checks for the event type of motion
                x, y = pygame.mouse.get_pos()
                print(x) #records the position of the mouse
                #drawing the wall
                if event.buttons[0] and x < width and x > 0 and y < height and y > 0: #checks if the left mouse button is pressed
                    i = x // w #records the x position of the mouse
                    j = y // h #records the y position of the mouse
                    grid[i][j].wall = True #sets the wall to true

                if event.buttons[2] and not target_box_set and x < width and x > 0 and y < height and y > 0: #checks if the right mouse button is pressed and the target box is not set
                    i = x // w #records the x position of the mouse
                    j = y // h #records the y position of the mouse
                    target_box = grid[i][j] #sets the target box to the current box
                    target_box.target = True #sets the target box to true
                    target_box_set = True #sets the target box flag to true

            #keyboard interaction
            if event.type == pygame.KEYDOWN and target_box_set:
                if event.key == pygame.K_SPACE:
                    begin_search = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.popleft()
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    dijk(grid, current_box, queue)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("Path Not Found", "There was no path to the target box")
                    searching = False

        win.fill((0, 0, 0)) #window fills color black

        for col in range(cols):
            for row in range(rows):
                box = grid[col][row]
                box.draw(win, (55, 55, 55))
                if box.queued:
                    box.draw(win, (200, 0, 0))
                if box.visited:
                    box.draw(win, (0, 200, 0))
                if box in path:
                    box.draw(win, (0, 0, 200))
                if box.start:
                    box.draw(win, (0, 200, 200))
                if box.target:
                    box.draw(win, (200, 200, 0))
                if box.wall:
                    box.draw(win, (190, 190, 190))


        pygame.display.flip() #updates the screen can also use pygame.display.update()

main()
