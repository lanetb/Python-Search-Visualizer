
import random
def create_maze(grid):
    start_pos = grid[0][0]
    walls = all_walls(grid, start_pos)
    recursive_dfs(grid, walls, start_pos)


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
        moves_avalible.remove(random_move)
        x_temp, y_temp = x, y
        match random_move:
            case 'up':
                y_temp -= 2
            case 'down':
                y_temp += 2
            case 'left':
                x_temp -= 2
            case 'right':
                x_temp += 2
        if x_temp < 0 or x_temp > len(grid) - 1 or y_temp < 0 or y_temp > len(grid[0]) - 1:
            continue

        new_pos = grid[x_temp][y_temp]
        if new_pos in walls:
            new_pos.wall = False
            walls.remove(new_pos)

            x_diff = new_pos.x - position.x
            y_diff = new_pos.y - position.y

            middle_wall = grid[position.x + x_diff // 2][position.y + y_diff // 2]
            middle_wall.wall = False
            walls.remove(middle_wall)

            recursive_dfs(grid, walls, new_pos)
    return