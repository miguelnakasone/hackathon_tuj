import pygame

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((640, 480))

# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                # Display your own right-click menu here
                print("Right-clicked!")