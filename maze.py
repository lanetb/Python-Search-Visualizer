
import random
def create_maze(grid):
    start_pos = grid[0][0]
    walls = all_walls(grid, start_pos)


def all_walls(grid, start_pos):
    walls = []
    for cols in range(len(grid)):
        for rows in range(len(grid[0])):
            if not grid[cols][rows] == start_pos:
                grid[cols][rows].wall = True
                walls.append(grid[cols][rows])
    return walls

def recursive_dfs(grid, walls, position):
    moves_avalible = ['up', 'down', 'left', 'right']
    x, y = position.x, position.y

    while moves_avalible:
        random_move = random.choice(moves_avalible)
    