import pygame
import tkinter as tk
from tkinter import Menu
import threading

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Right Click Menu in Pygame")

# Tkinter Setup in a Thread
def init_tkinter():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    menu = Menu(root, tearoff=0)
    menu.add_command(label="Option 1", command=lambda: print("Option 1 Selected"))
    menu.add_command(label="Option 2", command=lambda: print("Option 2 Selected"))
    menu.add_separator()
    menu.add_command(label="Exit", lambda: root.quit())

    def show_menu(position):
        """Show the Tkinter menu at the given screen position."""
        menu.post(position[0], position[1])

    return root, show_menu

# Start Tkinter in a Separate Thread
root, show_menu = init_tkinter()

def run_tk():
    root.mainloop()

threading.Thread(target=run_tk, daemon=True).start()

# Pygame Main Loop
running = True
while running:
    screen.fill((255, 255, 255))  # White background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right Click
                show_menu(pygame.mouse.get_pos())  # Show Tkinter menu

    pygame.display.flip()

pygame.quit()
