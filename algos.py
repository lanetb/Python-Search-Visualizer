def dijk (grid, current_box, queue):
    for neighbour in current_box.neighbors:
        if not neighbour.queued and not neighbour.wall:
            neighbour.queued = True
            neighbour.prior = current_box
            queue.append(neighbour)
