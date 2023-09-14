def dikstra(grid, current_box, queue, path):
    for neighbor in current_box.neighbors:
        if not neighbor.queued and not neighbor.wall:
            neighbor.queued = True
            queue.append(neighbor)
