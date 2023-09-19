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

def a_star(grid, frontier, unique, target_box, start_box, path, heristic):
    current_box = frontier.get()[2]
    current_box.visited = True
    if current_box == target_box:
        print("done")
        while current_box.prior != start_box:
            path.append(current_box.prior)
            current_box = current_box.prior
        return False
    else:
        for neighbor in current_box.neighbors:
            if not neighbor.wall:
                neighbor.g_cost = current_box.g_cost + 1
                match heristic:
                    case "manhatten":
                        neighbor.h_cost = manhatten_heuristic(neighbor, target_box)
                    case "euclidean":
                        neighbor.h_cost = euclidean_heuristic(neighbor, target_box)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                if not neighbor.queued or neighbor.f_cost < current_box.f_cost:
                    neighbor.prior = current_box
                    neighbor.queued = True
                    frontier.put((neighbor.f_cost, next(unique), neighbor))

        return True
