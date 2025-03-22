import pygame

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.load("fishing_music.wav")
pygame.mixer.music.play(-1)
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LAKE_WIDTH = 400
LAKE_HEIGHT = 300
LINE_LENGTH = 30

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Player and lake objects
player = pygame.Rect(400, 50, 50, 50)
water = pygame.Rect((SCREEN_WIDTH/2 - LAKE_WIDTH/2, SCREEN_HEIGHT/2 - LAKE_HEIGHT/2, LAKE_WIDTH, LAKE_HEIGHT))
direction = "east"

# Variables for the line
line_start = player.center
line_end = line_start

# Game loop
run = True
while run:
    screen.fill("green")

    # Draw player and lake
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (55, 55, 255), water)

    # Store old position
    old_x, old_y = player.x, player.y

    # Movement logic
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move_ip(-1, 0)
        direction = "west"
    elif key[pygame.K_RIGHT]:
        player.move_ip(1, 0)
        direction = "east"
    elif key[pygame.K_UP]:
        player.move_ip(0, -1)
        direction = "north"
    elif key[pygame.K_DOWN]:
        player.move_ip(0, 1)
        direction = "south"

    # Keep player inside the screen boundaries
    if player.left < 0:
        player.left = 0
    if player.right > SCREEN_WIDTH:
        player.right = SCREEN_WIDTH
    if player.top < 0:
        player.top = 0
    if player.bottom > SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

    # Collision with the lake
    if player.colliderect(water):
        player.x, player.y = old_x, old_y

    # Line logic
    if key[pygame.K_SPACE]:
        # Set line start at the player center
        line_start = player.center

        # Calculate the line end based on direction
        if direction == "east":
            line_end = (line_start[0] + LINE_LENGTH, line_start[1])
        elif direction == "west":
            line_end = (line_start[0] - LINE_LENGTH, line_start[1])
        elif direction == "north":
            line_end = (line_start[0], line_start[1] - LINE_LENGTH)
        elif direction == "south":
            line_end = (line_start[0], line_start[1] + LINE_LENGTH)

        # Check if the line is in the water
        line_rect = pygame.Rect(min(line_start[0], line_end[0]),
                                min(line_start[1], line_end[1]),
                                abs(line_end[0] - line_start[0]),
                                abs(line_end[1] - line_start[1]))

        if line_rect.colliderect(water):
            # Line stays extended
            pygame.draw.line(screen, (0, 0, 0), line_start, line_end, 3)
        else:
            # Line retracts
            line_end = line_start

    # Draw the line
    pygame.draw.line(screen, (0, 0, 0), line_start, line_end, 3)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

# Quit the game
pygame.quit()
