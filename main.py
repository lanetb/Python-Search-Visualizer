import pygame, sys, random, math #pygame and module systems
from collections import deque
from tkinter import messagebox, Tk #allows for small dialog boxes to be created

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
queue, visited = deque(), []
path = []

class Box:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.neighbors = []
        self.previous = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * w, self.y * h, w, h))

for row in range(cols):
    arr=[]
    for i in range(rows):
        arr.append(Box(row, i))
    grid.append(arr)

def main(): #main method houses the main loop
    while True:
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        win.fill((0, 0, 0)) #window fills color black

        for row in range(cols):
            for i in range(rows):
                box = grid[row][i]
                box.draw(win, (255, 255, 255))


        pygame.display.flip() #updates the screen can also use pygame.display.update()

main()
