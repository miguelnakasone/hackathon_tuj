    for i in range(len(path) - 1, -1, -1):  # Iterate in reverse order
            rect, size, timestamp = path[i]
            if current_time - timestamp < LIFETIME:
                pygame.draw.rect(screen, SQUARE_COLOR, (rect[0] ,rect[1], size[0], size[1]))
            else:
                path.pop(i)