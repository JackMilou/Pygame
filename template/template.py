import pygame, random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("temp")


FPS = 60
clock = pygame.time.Clock()

#valuse

#color
COLOR = (0, 0, 0)

#font
font = pygame.font.Font("Burger-dog/Other/Burger-text.ttf")

#text

#sound

#images

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #get pressed keys
        keys = pygame.key.get_pressed()
        #move 
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                print("movement")
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                print("movement")
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                print("movement")
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                print("movement")


    #fill surface
    display_surface.fill(COLOR)

    #Update HUD


    #Blit the HUD


    #blit assets


    pygame.display.update()

    #tick the clock
    clock.tick(FPS)

pygame.quit()