import pygame

pygame.init()

##Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LAKE_WIDTH = 400
LAKE_HEIGHT = 300

#our screen to display on
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#variables such for our objects
player = pygame.Rect((400,50,50,50))
water = pygame.Rect((SCREEN_WIDTH/2-LAKE_WIDTH/2, SCREEN_HEIGHT/2-LAKE_HEIGHT/2, LAKE_WIDTH, LAKE_HEIGHT))

#the loop the game runs in
run = True
while run:

    screen.fill("green")

    #draws the lake and player on the screen
    pygame.draw.rect(screen, (255,0,0), player)
    pygame.draw.rect(screen, (55,55,255), water)

    #this is our key inputs
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move_ip(-1,0)
    elif key[pygame.K_RIGHT]:
        player.move_ip(1,0)
    if key[pygame.K_UP]:
        player.move_ip(0,-1)
    elif key[pygame.K_DOWN]:
        player.move_ip(0,1)

    #allows you to close the aplication
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

#ends the game
pygame.quit() 