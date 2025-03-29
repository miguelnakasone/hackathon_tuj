import pygame
import sys
import pygame.font

pygame.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze")
font = pygame.font.Font(None,size=50)

LIFETIME = 1500 
SQUARE_COLOR = (255, 255, 255)  
first = False
won = False
caught = False

pygame.mixer.music.load('Assets/8-bit-music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

mouse_x, mouse_y = pygame.mouse.get_pos()

path = [((0, 600), (120, 10)),
        ((120, 325), (10, 285)),
        ((120, 325), (130, 10)),
        ((250, 300), (50, 50)),
        ((400, 400), (50, 50)),
        ((750, 700), (50, 50))]

    
endpoint_x = 425;
endpoint_y = 425;
endpoint_radius = 10; 

rectangle_x = 50
rectangle_y = 50

# def add_rectangle(path, x, y, width, height):
#     timestamp = pygame.time.get_ticks()
#     path.append(((x , y - height),(width,height))

msg = font.render("Think Outside The Box...",1,(200,0,0))
msg2 = font.render("That was an easy one...",1,(255,165,0))
msg3 = font.render("You Win!!1!!1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",1,(0,200,0))
msg4 = font.render("I didn't think you'd be 'that' smart...",1,(0,165,0))
msg5 = font.render("But now there's no 'escape'! Muahahaha",1,(128,128,128))
# msg6 = font2.render("Sike! it isn't",1,(128,128,128))

run = True
while run:
    screen.fill((0, 0, 0))
    if won == False :
        screen.blit(msg,(150,100))
        pygame.draw.circle(screen, (255,0,0),(endpoint_x , endpoint_y),endpoint_radius)
    else :
        first = False
        caught = False
        screen.blit(msg3,(100,200))
        pygame.draw.circle(screen, (0,255,0),(endpoint_x , endpoint_y),endpoint_radius)
                
    if first == True: 
        screen.blit(msg2,(100,700))
        screen.blit(msg5,(100,750))
        path.append((((700,300),(50,50))))
        
    if caught == True: 
        screen.blit(msg4,(200,500))
 
    

        
    for rect in path:
        pygame.draw.rect(screen, (255, 255, 255), rect)
        
    # if(won == False):
    #     for i in range(len(path) - 1, -1, -1):  # Iterate in reverse order
    #         rect, size, timestamp = path[i]
    #         if current_time - timestamp < LIFETIME:
    #             pygame.draw.rect(screen, SQUARE_COLOR, (rect[0] ,rect[1], size[0], size[1]))
    #         else:
    #             path.pop(i)
        
    pygame.draw.circle(screen, (255,0,0),(endpoint_x , endpoint_y),endpoint_radius)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # Check if a key is pressed
            if event.key == pygame.K_ESCAPE:  # Check if the ESC key is pressed
                print("Escape key pressed!")  # Replace this with your action
                path.extend( (((750,325),(50,10)), ((650,325),(50,10)) , ((650,335),(10,160)) , ((425,485),(225,10)) , ((425,450),(10,35))))
                caught = True
    pygame.display.flip()
    if ((pygame.mouse.get_pos()[0]-endpoint_x)**2+(pygame.mouse.get_pos()[1]-endpoint_y)**2)<=endpoint_radius**2:
        print("you won")
        won = True
        
    if (pygame.mouse.get_pos()[0] >= 750 and pygame.mouse.get_pos()[0] <= 800) and (pygame.mouse.get_pos()[1] >= 700 and pygame.mouse.get_pos()[1] <= 750):
        first = True
        
    if (pygame.mouse.get_pos()[0] >= 750 and pygame.mouse.get_pos()[0] <= 800) and (pygame.mouse.get_pos()[1] >= 700 and pygame.mouse.get_pos()[1] <= 750):
        first = True

    #check if you're out of bounds
    buffer = 1  # 1-pixel border

    if any(
        (b[0][0] - buffer) < pygame.mouse.get_pos()[0] < (b[1][0] + b[0][0] + buffer) and 
        (b[0][1] - buffer) < pygame.mouse.get_pos()[1] < (b[1][1] + b[0][1] + buffer) 
        for b in path
    ):
        print("True")
    else:
        print("False")
        if not won:
            pygame.mouse.set_pos((275, 325))
    # if any(b[0][0]<pygame.mouse.get_pos()[0]<b[1][0]+b[0][0] and b[0][1]<pygame.mouse.get_pos()[1]<b[1][1]+b[0][1] for b in path):
    #     print("True")
    # else:
    #     print("False")
    #     if(won == False):
    #         pygame.mouse.set_pos((75, 125))
    pygame.display.update()
