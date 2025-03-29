import pygame
import sys
import math


pygame.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze")



pygame.mixer.music.load('Assets//background-copy.mp3')
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1) 

# Maze path (x, y), (width, height)
path = [((0, 400), (200, 30)), ((200, 400), (30, 350)), ((200, 750), (100, 30)), ((300, 50), (30, 730)),
        ((300, 50), (100, 30)), ((400, 50), (30, 600)), ((400, 650), (100, 30)), ((500, 150), (30, 530)),
        ((500, 150), (100, 30)), ((600, 150), (30, 400)), ((600, 550), (100, 30)), ((700, 300), (30, 280)),
        ((700, 300), (100, 30))]

end_x, end_y = 775, 315
start_x, start_y = 15, 415
run = True
part2 = False
clock = pygame.time.Clock()

# Load and scale the spike image
spike = pygame.image.load('Assets/spike.png').convert_alpha()
spike = pygame.transform.scale(spike, (30, 50))

carpet = pygame.image.load('Assets/carpet.png').convert_alpha()
carpet = pygame.transform.scale(carpet, (100, 30))

hani = pygame.image.load('Assets/hani.png').convert_alpha()
hani = pygame.transform.scale(hani, (200, 200))

farid1 = pygame.image.load('Assets/farid.png').convert_alpha()
farid1 = pygame.transform.scale(farid1, (50, 50))

farid2 = pygame.image.load('Assets/farid.png').convert_alpha()
farid2 = pygame.transform.scale(farid2, (50, 50))

farid3 = pygame.image.load('Assets/farid.png').convert_alpha()
farid3 = pygame.transform.scale(farid3, (50, 50))

# Initial spike position & properties
spike_x, spike_y = 600, 100
drop_speed = 5
spike_dropped = False

carpet_x, carpet_y = 400, 650
carpet_dropped = False
carpet_trigger_time = 0  # Time when the carpet was triggered
carpet_hidden = False  # Flag to ensure the carpet stays hidden

hani_x, hani_y = 50, 100

farid1_x, farid1_y = 770, 50
farid2_x, farid2_y = 770, 400
farid3_x, farid3_y = 770, 750

# Trigger points
trigger_point1 = (600, 130)
trigger_point2 = (500, 650)
trigger_point3 = (400, 400)  # Trigger point to start chasing

# Flag to check if Farids should start chasing
farids_chasing = False

# Constant speed for Farid's movement
farid_speed = 100  # Speed in pixels per second

played1=False 
played2=False 
monkey = False

def reset():
    global spike_x, spike_y, drop_speed, spike_dropped, part2, end_x, end_y, carpet_dropped, carpet_trigger_time, carpet_hidden, farids_chasing
    global farid1_x, farid1_y, farid2_x, farid2_y, farid3_x, farid3_y
    spike_x, spike_y = 600, 100  
    drop_speed = 10  
    spike_dropped = False  
    part2 = False  
    end_x, end_y = 775, 315  
    carpet_dropped = False  # Reset carpet
    carpet_trigger_time = 0  # Reset carpet trigger time
    carpet_hidden = False  # Reset carpet hidden status
    pygame.mouse.set_pos(start_x, start_y)
    farid1_x, farid1_y = 770, 50
    farid2_x, farid2_y = 770, 400
    farid3_x, farid3_y = 770, 750
    farids_chasing = False  # Reset the chasing flag
    print("Game reset!")

flag = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dt = clock.get_time() / 1000.0
    mouse_x, mouse_y = pygame.mouse.get_pos()

    buffer = 2  
    in_path = False
    for rect in path:
        rect_x, rect_y = rect[0]
        rect_w, rect_h = rect[1]
        if (rect_x - buffer) < mouse_x < (rect_x + rect_w + buffer) and (rect_y - buffer) < mouse_y < (rect_y + rect_h + buffer):
            in_path = True
            break  

    # If the mouse is not in the maze path (not inside any of the path areas), reset
    if not in_path:
        reset()

    # Spike trigger
    distance1 = math.sqrt((mouse_x - trigger_point1[0]) ** 2 + (mouse_y - trigger_point1[1]) ** 2)

    if part2 and distance1 < 70:
        spike_dropped = True
        if not played1: 
            played1 = True
            pygame.mixer.music.load('Assets/spike.mp3')
            pygame.mixer.music.set_volume(0.5)  
            pygame.mixer.music.play() 

    # Spike action
    if spike_dropped and spike_y < screen_height:
        drop_speed += 5  
        spike_y += drop_speed * dt  

    # Carpet trigger
    distance2 = math.sqrt((mouse_x - trigger_point2[0]) ** 2 + (mouse_y - trigger_point2[1]) ** 2)

    # Trigger the carpet to drop if part2 is active, mouse is near the trigger point and carpet hasn't been hidden
    if part2 and distance2 < 20 and not carpet_dropped and not carpet_hidden:
        carpet_dropped = True
        carpet_trigger_time = pygame.time.get_ticks()  # Record the time when carpet is triggered
        if not played2:
            played2 = True
            pygame.mixer.music.load('Assets/carpet.mp3')
            pygame.mixer.music.set_volume(0.5)  
            pygame.mixer.music.play() 

    # Hide carpet after 2 seconds, regardless of mouse position
    if carpet_dropped and pygame.time.get_ticks() - carpet_trigger_time > 2000:  # 2000ms = 2 seconds
        carpet_dropped = False  # Carpet disappears
        carpet_hidden = True  # Set the flag so it stays hidden forever

    # Part2 trigger
    if ((mouse_x - end_x + 40) ** 2 + (mouse_y - end_y) ** 2) <= 15 ** 2:
        end_x = start_x
        end_y = start_y
        part2 = True
        pygame.mixer.music.load('Assets/laugh.mp3')
        pygame.mixer.music.set_volume(0.5)  
        pygame.mixer.music.play() 

    # Check if player reaches trigger_point3 (400, 400) to start chasing
    distance3 = math.sqrt((mouse_x - trigger_point3[0]) ** 2 + (mouse_y - trigger_point3[1]) ** 2)
    if distance3 < 30 and part2:  # Distance is small enough to consider the player has reached the point
        farids_chasing = True  # Start the Farids chasing the mouse

    # Reset if touching Farid or spike
    if (spike_x < mouse_x < spike_x + spike.get_width() and spike_y < mouse_y < spike_y + spike.get_height()):
        reset()
    if (farid1_x < mouse_x < farid1_x + farid1.get_width() and farid1_y < mouse_y < farid1_y + farid1.get_height()) or \
       (farid2_x < mouse_x < farid2_x + farid2.get_width() and farid2_y < mouse_y < farid2_y + farid2.get_height()) or \
       (farid3_x < mouse_x < farid3_x + farid3.get_width() and farid3_y < mouse_y < farid3_y + farid3.get_height()):
        reset()

    # Draw
    screen.fill((0, 0, 0))

 
    for rect in path:
        pygame.draw.rect(screen, (255, 255, 255), rect)

    pygame.draw.circle(screen, (255, 0, 0), (end_x, end_y), 12)
    distance_to_end = math.sqrt((mouse_x - end_x) ** 2 + (mouse_y - end_y) ** 2)

    if distance_to_end <= 12:
        flag = True

    if spike_dropped:
        screen.blit(spike, (spike_x, spike_y))

    if carpet_dropped:
        screen.blit(carpet, (carpet_x, carpet_y))

    screen.blit(hani, (hani_x, hani_y))


    if farids_chasing:
        monkey = True
        def move_towards(farid_x, farid_y, target_x, target_y, speed):
            dx = target_x - farid_x
            dy = target_y - farid_y
            distance = math.sqrt(dx**2 + dy**2)


            if distance == 0:
                return farid_x, farid_y

            dx /= distance
            dy /= distance
            farid_x += dx * speed * dt
            farid_y += dy * speed * dt

            return farid_x, farid_y

        # Move the Farids toward the player (mouse)
        farid1_x, farid1_y = move_towards(farid1_x, farid1_y, mouse_x, mouse_y, farid_speed)
        farid2_x, farid2_y = move_towards(farid2_x, farid2_y, mouse_x, mouse_y, farid_speed)
        farid3_x, farid3_y = move_towards(farid3_x, farid3_y, mouse_x, mouse_y, farid_speed)
        pygame.mixer.music.load('Assets/monkey.mp3')
        pygame.mixer.music.set_volume(0.5)  
        pygame.mixer.music.play() 
    
        
        

    screen.blit(farid1, (farid1_x, farid1_y))
    screen.blit(farid2, (farid2_x, farid2_y))
    screen.blit(farid3, (farid3_x, farid3_y))

    left_eye, right_eye = (140, 170), (163, 170)
    eye_radius = 5
    pygame.draw.circle(screen, (255, 255, 255), left_eye, eye_radius)
    pygame.draw.circle(screen, (255, 255, 255), right_eye, eye_radius)

    pupil_radius = 3
    left_distance_x = (mouse_x - left_eye[0]) // 150
    left_distance_y = (mouse_y - left_eye[1]) // 150

    pygame.draw.circle(screen, (0, 0, 0), (left_eye[0] + left_distance_x, left_eye[1] + left_distance_y), pupil_radius)
    pygame.draw.circle(screen, (0, 0, 0), (right_eye[0] + left_distance_x, right_eye[1] + left_distance_y), pupil_radius)


    pygame.display.update()
    clock.tick(60)

    if flag == True:
        break
pygame.display.quit()