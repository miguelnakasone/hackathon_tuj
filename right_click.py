import pygame
import sys
import pygame.font

pygame.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze")
font = pygame.font.Font(None,size=50)
font2 = pygame.font.Font(None, size=40)

squares = []
LIFETIME = 1500 
SQUARE_COLOR = (255, 255, 255)  
won = False
checkPoint = False

pygame.mixer.music.load('Assets/8-bit-music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

path = [((50, 700), (50, 50), pygame.time.get_ticks()+600000),
        ((400, 400), (50, 50), pygame.time.get_ticks()+600000),
        ((650, 100), (100, 50), pygame.time.get_ticks()+600000)]
endpoint_x = 700;
endpoint_y = 125;
endpoint_radius = 10; 

rectangle_x = 50
rectangle_y = 50

def add_rectangle(path, x, y, width, height):
    timestamp = pygame.time.get_ticks()
    path.append(((x , y - height),(width,height), timestamp))

msg = font.render("Oh, no! You're trapped!",1,(200,0,0))
msg2 = font.render("Creating bridges is the 'right' way...",1,(0,200,0))
msg3 = font.render("You Win!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",1,(0,200,0))
msg4 = font2.render("<-- Mouse rest stop",1,(128,128,128))
msg5 = font2.render("  (Don't worry, it's a checkpoint)",1,(128,128,128))
msg6 = font2.render("Sike! it isn't",1,(128,128,128))

run = True
while run:
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()
    if won == False :
        screen.blit(msg,(75,100))
        screen.blit(msg2,(150,700))
        pygame.draw.circle(screen, (255,0,0),(endpoint_x , endpoint_y),endpoint_radius)
    else :
        screen.blit(msg3,(300,300))
        pygame.draw.circle(screen, (0,255,0),(endpoint_x , endpoint_y),endpoint_radius)
        
    if checkPoint == False: 
        screen.blit(msg4,(450,400))
        screen.blit(msg5,(300,450))
    else :
        screen.blit(msg6,(400,450))
        
    if(won == False):
        for i in range(len(path) - 1, -1, -1):  # Iterate in reverse order
            rect, size, timestamp = path[i]
            if current_time - timestamp < LIFETIME:
                pygame.draw.rect(screen, SQUARE_COLOR, (rect[0] ,rect[1], size[0], size[1]))
            else:
                path.pop(i)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right Click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if(checkPoint):
                    add_rectangle(path, mouse_x, mouse_y, rectangle_x/2,rectangle_y/2)
                else: 
                    add_rectangle(path, mouse_x, mouse_y, rectangle_x,rectangle_y)
                
    pygame.display.flip()
    if ((pygame.mouse.get_pos()[0]-endpoint_x)**2+(pygame.mouse.get_pos()[1]-endpoint_y)**2)<=endpoint_radius**2:
        print("you won")
        won = True
        
    if (pygame.mouse.get_pos()[0] >= 400 and pygame.mouse.get_pos()[0] <= 450) and (pygame.mouse.get_pos()[1] >= 400 and pygame.mouse.get_pos()[1] <= 450):
        checkPoint = True

    #check if you're out of bounds
    if any(b[0][0]<pygame.mouse.get_pos()[0]<b[1][0]+b[0][0] and b[0][1]<pygame.mouse.get_pos()[1]<b[1][1]+b[0][1] for b in path):
        print("True")
    else:
        print("False")
        if(won == False):
            pygame.mouse.set_pos((75, 725))
    pygame.display.update()
