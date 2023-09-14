import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk

# Initialize pygame
size = (width, height) = (850, 480)
pygame.init()

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



