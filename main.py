import pygame

# Game window------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
pygame.display.set_caption("MikunXL")
#------------------------------------------------------------------

def draw_window():
    



# Main Loop-------------------------------------
def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill("Purple")
        pygame.display.update()

        clock.tick(60)


    pygame.quit()

#-----------------------------------------------
if __name__ == "__main__":
    main()