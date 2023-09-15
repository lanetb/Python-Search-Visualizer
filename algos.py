import random
import math

def dijk (grid, queue, target_box, path, start_box):
    current_box = queue.popleft()
    current_box.visited = True
    if current_box == target_box:
        while current_box.prior != start_box:
            path.append(current_box.prior)
            current_box = current_box.prior
        return False
    else:
        for neighbour in current_box.neighbors:
            if not neighbour.queued and not neighbour.wall:
                neighbour.queued = True
                neighbour.prior = current_box
                queue.append(neighbour)
        return True

def manhatten_heuristic(box, target_box):
    return abs(box.x - target_box.x) + abs(box.y - target_box.y)

def euclidean_heuristic(box, target_box):
    return math.sqrt((box.x - target_box.x)**2 + (box.y - target_box.y)**2)

def a_star(grid, open_set, closed_set, target_box, start_box, path, heristic):
    winner = 0

    for i in range(len(open_set)):
        if open_set[i].f_cost < open_set[winner].f_cost:
            winner = i
    
    current_box = open_set[winner]
    open_set.remove(current_box)
    closed_set.append(current_box)
    current_box.visited = True

    if current_box == target_box:
        print("done")
        while current_box.prior != start_box:
            path.append(current_box.prior)
            current_box = current_box.prior
        return False
    else:
        for neighbor in current_box.neighbors:
            if neighbor.wall or neighbor in closed_set:
                continue
            if neighbor not in open_set and current_box.g_cost >= neighbor.g_cost:
                neighbor.prior = current_box
                match heristic:
                    case "manhatten":
                        neighbor.h_cost = manhatten_heuristic(neighbor, target_box)
                    case "euclidean":
                        neighbor.h_cost = euclidean_heuristic(neighbor, target_box)
                neighbor.g_cost = current_box.g_cost + 1
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                if neighbor not in open_set:
                    open_set.append(neighbor)
        return True
