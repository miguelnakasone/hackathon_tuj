import pygame
import sys
import math
import random

pygame.init()
pygame.mixer.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Runner")

# Load and scale background image
background_image = pygame.image.load('Assets/background-image2.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

START_POS = (10, 400)
END_POS = (10, 730)
game_won = False

font = pygame.font.Font(None, 36)

# Load and play background music
pygame.mixer.music.load('Assets/background.mp3')
pygame.mixer.music.set_volume(0.5)  # Set volume 50%
pygame.mixer.music.play(-1)  # loop indefinitely

# Warning sound
warning_sound = pygame.mixer.Sound('Assets/Siren.mp3')
warning_sound.set_volume(0.7)

# Dynamic path settings
MIN_THICKNESS = 10
MAX_THICKNESS = 20 
THICKNESS_SPREAD = MAX_THICKNESS - MIN_THICKNESS

# Flashlight settings
FLASHLIGHT_RADIUS = 100

# Create a surface for the dark overlay
dark_overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, 255))

#maze path (x,y),(width, height), thickness, is_dynamic
path=[
    ((0,400), (200, 20), 20, False),((200, 200), (20, 220), 20, True),((200,200), (220, 20), 20, False),((400, 200), (20, 320), 20, False),((200, 500), (200, 20), 20, False),((100, 500), (200, 20), 20, False),
    ((100, 500), (20, 100), 20, True),((100, 600), (400, 20), 20, False),((100, 600), (400, 20), 20, False),((500, 120), (20, 500), 20, True),((100, 120), (420, 20), 20, False),((100, 60), (20, 80), 20, True),
    ((100, 60), (480, 20), 20, False),((570, 60), (20, 600), 20, False),((570, 650), (70, 20), 20, False),((640, 90), (20, 580), 20, False),((640, 90), (100, 20), 20, True),((740, 90), (20, 650), 20, False),((0, 720), (750, 20), 20, False)
]

clock = pygame.time.Clock()
time = 0

# Earthquake variables
earthquake_active = False
earthquake_timer = 0
earthquake_duration = 2  # seconds
shake_intensity = 5  # pixels
shake_offset = [0, 0]

# Add near the top with other variables
show_intro = True
intro_timer = 4
intro_start_time = 0

def is_on_path(mouse_pos, rect):
    pos, size, thickness, is_dynamic = rect
    if is_dynamic:
        current_thickness = max(MIN_THICKNESS, MIN_THICKNESS + THICKNESS_SPREAD * math.sin(time))
    else:
        current_thickness = thickness
        
    x, y = mouse_pos

    if size[0] > size[1]:
        path_center = pos[1] + size[1]/2
        if abs(y - path_center) > current_thickness/2:
            return False
        return pos[0] <= x <= pos[0] + size[0]
    else:
        path_center = pos[0] + size[0]/2
        if abs(x - path_center) > current_thickness/2:
            return False
        return pos[1] <= y <= pos[1] + size[1]

def start_earthquake():
    global earthquake_active, earthquake_timer
    earthquake_active = True
    earthquake_timer = earthquake_duration
    # Pause background music and play warning sound
    pygame.mixer.music.pause()
    warning_sound.play()

def update_earthquake():
    global earthquake_active, earthquake_timer, shake_offset
    if earthquake_active:
        # Update shake offset with random values
        shake_offset[0] = random.randint(-shake_intensity, shake_intensity)
        shake_offset[1] = random.randint(-shake_intensity, shake_intensity)
        
        # Update timer
        earthquake_timer -= 1/60
        if earthquake_timer <= 0:
            earthquake_active = False
            shake_offset = [0, 0]
            # Stop warning sound and resume background music
            warning_sound.stop()
            pygame.mixer.music.unpause()

run = True
earthquake_interval = 20
last_earthquake = 0

flag = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Update intro timer
    if show_intro:
        if time - intro_start_time >= intro_timer:
            show_intro = False
    
    # Update earthquake
    update_earthquake()
    
    # Check if it's time for a new earthquake
    if time - last_earthquake >= earthquake_interval and not earthquake_active:
        start_earthquake()
        last_earthquake = time
    
    # Get current mouse position
    current_pos = pygame.mouse.get_pos()
    
    # Check win condition
    if not game_won and ((current_pos[0]-END_POS[0])**2+(current_pos[1]-END_POS[1])**2)<=10**2:
        game_won = True
        # Pause background music when game is won
        pygame.mixer.music.stop()

    # Only check for out of bounds if game is not won
    if not game_won:
        if not any(is_on_path(current_pos, b) for b in path):
            print("False")
            # Reset to starting position
            pygame.mouse.set_pos(START_POS)
            
        else:
            print("True")

    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((0, 0, 0))
    
    # Only draw maze elements if game is not won
    if not game_won:
        #creating maze
        for rect in path:
            pos, size, thickness, is_dynamic = rect
            if is_dynamic:
                dynamic_thickness = max(MIN_THICKNESS, MIN_THICKNESS + THICKNESS_SPREAD * math.sin(time))
            else:
                dynamic_thickness = thickness
                
            if size[0] > size[1]:
                pygame.draw.rect(screen, (10, 10, 10), 
                               (pos[0] + shake_offset[0], 
                                pos[1] - dynamic_thickness/2 + size[1]/2 + shake_offset[1], 
                                size[0], dynamic_thickness))
            else:
                pygame.draw.rect(screen, (10, 10, 10), 
                               (pos[0] - dynamic_thickness/2 + size[0]/2 + shake_offset[0], 
                                pos[1] + shake_offset[1], 
                                dynamic_thickness, size[1]))
        
        # Draw "Start" text and end point
        start_text = font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, (10 + shake_offset[0], 400 + shake_offset[1]))
        pygame.draw.circle(screen, (255,0,0),
                          (END_POS[0] + shake_offset[0], END_POS[1] + shake_offset[1]), 10)
        
        # Apply flashlight effect
        mouse_pos = pygame.mouse.get_pos()
        current_overlay = dark_overlay.copy()
        pygame.draw.circle(current_overlay, (0, 0, 0, 0), mouse_pos, FLASHLIGHT_RADIUS)
        screen.blit(current_overlay, (0, 0))
        
        # Draw warning text during earthquake
        if earthquake_active:
            warning_font = pygame.font.Font(None, 60)
            warning_text = warning_font.render("! EARTHQUAKE !", True, (255, 0, 0))
            text_rect = warning_text.get_rect(center=(screen_width/2, 50))
            screen.blit(warning_text, text_rect)
    else:
        # Draw victory screen
        victory_font = pygame.font.Font(None, 84)
        congrats_text = victory_font.render("CONGRATULATIONS!", True, (255, 215, 0))
        congrats_rect = congrats_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
        screen.blit(congrats_text, congrats_rect)
        
        complete_text = font.render("You've complted the Final Challenge!", True, (255, 255, 255))
        complete_rect = complete_text.get_rect(center=(screen_width/2, screen_height/2 + 50))
        screen.blit(complete_text, complete_rect)
    
    # Intro
    if show_intro:
        intro_font = pygame.font.Font(None, 72)
        intro_text = intro_font.render("FINAL CHALLENGE", True, (255, 255, 255))
        text_rect = intro_text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(intro_text, text_rect)
    
    pygame.display.update()
    time += 0.05
    clock.tick(60)
