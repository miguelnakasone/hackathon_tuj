# import pygame
# import time
# import sys
# # Initialize pygame
# pygame.init()

# # Create a window
# screen = pygame.display.set_mode((640, 480))

# rect_color = (255, 255, 255)
# rect_border_width = 1

# start_time = time.time()
# # Main loop
# while True:
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 3:  # Right mouse button
#                 # Display your own right-click menu here
#                 print("Right-clicked!")
#                 # Draw the menu using Pygame's drawing functions
#                 mouse_x, mouse_y = pygame.mouse.get_pos()
#                 x_coor , y_coor = mouse_x-25, mouse_y-25
#                 rect_color = (255, 255, 255)
#                 pygame.draw.rect(screen, rect_color, (x_coor, y_coor, 50, 50))
#                 # pygame.draw.rect(screen, (0, 0, 0), (mouse_x-25, mouse_y-25, 50, 50), 1)
#                 pygame.display.flip()
                
#                 start_time = pygame.time.get_ticks()
#                 while pygame.time.get_ticks() - start_time < 5000:
#                     pass
#                 # pygame.time.delay(50)
#                 rect_color = (0, 0, 0)
#                 pygame.draw.rect(screen, rect_color, (x_coor, y_coor, 50, 50))
#                 pygame.display.flip()
                
#     # if time.time() - start_time > 5:
#     #             # Make the rectangle disappear
#     #                 rect_color = (0, 0, 0)  # Make the rectangle white
#     #                 rect_border_width = 0  # Remove the border
#     #                 pygame.draw.rect(screen, rect_color, (x_coor, y_coor, 50, 50))
#     #                 pygame.display.flip()
                
import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Right Click to Create Timed Squares")

# Colors
black = (0, 0, 0)
SQUARE_COLOR = (255, 255, 255)  

# List to store squares and their timestamps
squares = []
LIFETIME = 3000  # 5000 milliseconds (5 seconds)

# Main loop
running = True
while running:
    screen.fill(black)  # Clear screen

    current_time = pygame.time.get_ticks()

    # Draw squares and filter out old ones
    squares = [(x, y, timestamp) for x, y, timestamp in squares if current_time - timestamp < LIFETIME]

    for x, y, _ in squares:
        pygame.draw.rect(screen, SQUARE_COLOR, (x, y, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right Click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                squares.append((mouse_x - 25, mouse_y - 25, pygame.time.get_ticks()))  # Store (x, y, timestamp)

    pygame.display.flip()  # Refresh screen

pygame.quit()
