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

def a_star(grid, queue, target_box, start_box, path, heristic):
    priority, current_box = queue.get()
    current_box.visited = True
    if current_box == target_box:
        print("done")
        while current_box.prior != start_box:
            path.append(current_box.prior)
            current_box = current_box.prior
        return False
    else:
        for neighbour in current_box.neighbors:
            if not neighbour.queued and not neighbour.wall and not neighbour.visited or current_box.cost < neighbour.reached:
                neighbour.queued = True
                neighbour.prior = current_box
                cost_g = current_box.cost
                neighbour.reached = cost_g
                match heristic:
                    case "manhatten":
                        cost_h = manhatten_heuristic(neighbour, target_box)
                    case "euclidean":
                        cost_h = euclidean_heuristic(neighbour, target_box)
                #cost_h *= (1 + random.randrange(0, 999)/1000)
                neighbour.cost = cost_g + cost_h
                print(neighbour.cost)
                queue.put((neighbour.get_cost(), neighbour))
        return True
