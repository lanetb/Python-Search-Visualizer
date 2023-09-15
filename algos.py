def dijk (grid, current_box, queue):
    for neighbour in current_box.neighbors:
        if not neighbour.queued and not neighbour.wall:
            neighbour.queued = True
            neighbour.prior = current_box
            queue.append(neighbour)

def manhatten_heuristic(box, target_box):
    return abs(box.x - target_box.x) + abs(box.y - target_box.y)

def a_star(grid, current_box, queue, target_box, heristic):
    pass
