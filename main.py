import pygame
import sys
from collections import deque
from tkinter import messagebox, Tk
from algos import dijk, a_star
import queue

# Initialize pygame
size = (width, height) = (850, (480+50))
pygame.init()

# Create screen
win = pygame.display.set_mode(size)
pygame.display.set_caption("Pathfinding")
clock = pygame.time.Clock()

cols, rows = 85, 48
w = width // cols
h = (height - 50) // rows  # Subtract 50 for the GUI bar

algorithm_type = "Dijkstra"
grid = []
match algorithm_type:
    case "Dijkstra":
        que = deque()
    case "A*":
        que = queue.PriorityQueue()
path = []

# Define GUI variables
gui_height = 50
gui_color = (255, 255, 255)
button_color = (0, 100, 200)
button_hover_color = (0, 150, 255)
button_font = pygame.font.Font(None, 36)

# Create a Button class for the GUI
class Button:
    def __init__(self, text, x, y, width, height, command):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.command = command
        self.hovered = False

    def draw(self):
        color = button_hover_color if self.hovered else button_color
        pygame.draw.rect(win, color, self.rect)
        text = button_font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        win.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.command()

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

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * w, self.y * h + gui_height, w-2, h-2))

    def set_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

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
que.append(start_box)

# Main loop
def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None

    while True:
        for event in pygame.event.get():
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
                if event.key == pygame.K_SPACE:
                    begin_search = True

        if begin_search:
            if len(que) > 0 and searching:
                current_box = que.popleft()
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    match algorithm_type:
                        case "Dijkstra": 
                            dijk(grid, current_box, que)
                        case "A*":
                            a_star(grid, current_box, que, target_box, heristic="manhatten")
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("Path Not Found", "There was no path to the target box")
                    searching = False

        win.fill((0, 0, 0))

        for col in range(cols):
            for row in range(rows):
                box = grid[col][row]
                box.draw(win, (55, 55, 55))
                if box.queued:
                    box.draw(win, (200, 0, 0))
                if box.visited:
                    box.draw(win, (0, 255, 0))
                if box in path:
                    box.draw(win, (0, 0, 200))
                if box.start:
                    box.draw(win, (0, 200, 200))
                if box.target:
                    box.draw(win, (200, 200, 0))
                if box.wall:
                    box.draw(win, (150, 150, 150))

        # Draw GUI
        pygame.draw.rect(win, gui_color, (0, 0, width, gui_height-5))


        pygame.display.flip()

main()
