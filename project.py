import pygame
import sys

pygame.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze")

#maze path (x,y),(width, height)
path=[((0,400), (200, 30))]
pygame.mouse.set_pos((15, 415))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #checks if you reach end
    if ((pygame.mouse.get_pos()[0]-185)**2+(pygame.mouse.get_pos()[1]-415)**2)<=10**2:
        print("you won")

    #check if you're out of bounds
    if any(b[0][0]<pygame.mouse.get_pos()[0]<b[1][0]+b[0][0] and b[0][1]<pygame.mouse.get_pos()[1]<b[1][1]+b[0][1] for b in path):
        print("True")
    else:
        print("False")

    #background color
    screen.fill((0, 0, 0))
    
    #creating maze
    for rect in path:
        pygame.draw.rect(screen, (255, 255, 255), rect)
    
    #end pposition ((color),(x,y), radius)
    pygame.draw.circle(screen, (255,0,0),(185 , 415),10)
    pygame.display.update()
