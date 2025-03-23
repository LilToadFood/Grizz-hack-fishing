import pygame
import random
import math

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.load("fishing_music.mp3")
pygame.mixer.music.play(-1)

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
LAKE_WIDTH, LAKE_HEIGHT = 400, 300
SPEED = 5  # Player movement speed
WHITE, BLUE, BROWN, YELLOW = (255, 255, 255), (55, 55, 255), (150, 75, 0), (255, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Player and lake objects
player = pygame.Rect(400, 100, 50, 50)
water = pygame.Rect((SCREEN_WIDTH / 2 - LAKE_WIDTH / 2, SCREEN_HEIGHT / 2 - LAKE_HEIGHT / 2, LAKE_WIDTH, LAKE_HEIGHT))

# Fishing variables
fishing = False
in_range = False
bobber_x_offset = 0
bobber_y_offset = 0
bobber_angle = 0  # Start angle for the circular movement
fishing_result = None
bite_time = 0
waiting_for_bite = False
random_bobber_pos = None  # Store random bobber position
bobber_center = None  # Center point for spinning bobber

# Game loop
run = True
while run:

    screen.fill((0,150,0))

    # Draw lake
    pygame.draw.rect(screen, BLUE, water)

    # Draw player
    pygame.draw.rect(screen, (255,0,0), player)

    # Check if player is near water
    near_water = player.colliderect(water.inflate(50, 50))
    in_range = near_water  # Set in_range to True if the player is near the water

    # Display fishing prompt
    if near_water and not fishing:
        text = font.render("Press SPACE to fish!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))

    # Fishing animation
    if fishing:
        # Draw fishing line
        line_start = (player.x+25, player.y+25)
        line_end = random_bobber_pos  # Set line end to random bobber position
        pygame.draw.line(screen, YELLOW, line_start, line_end, 3)

        # Draw bobber (small red circle)
        pygame.draw.circle(screen, BROWN, random_bobber_pos, 7)

        # Bobber spinning in a circle (5px radius)
        if bobber_center:
            bobber_angle += 0.1  # Adjust speed of spinning
            bobber_x = bobber_center[0] + 5 * math.cos(bobber_angle)  # X offset using cosine
            bobber_y = bobber_center[1] + 5 * math.sin(bobber_angle)  # Y offset using sine
            random_bobber_pos = (int(bobber_x), int(bobber_y))

        # Check for bite
        if waiting_for_bite and pygame.time.get_ticks() > bite_time:
            fishing_result = random.choice([True, False])  # 50% chance
            fishing = False
            waiting_for_bite = False

    # Fishing result message
    if fishing_result is not None:
        result_text = "You caught a fish!" if fishing_result else "Nothing bit this time..."
        text = font.render(result_text, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100))

    # Movement logic
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and not fishing:
        player.move_ip(-SPEED, 0)
    elif key[pygame.K_RIGHT] and not fishing:
        player.move_ip(SPEED, 0)
    if key[pygame.K_UP] and not fishing:
        player.move_ip(0, -SPEED)
    elif key[pygame.K_DOWN] and not fishing:
        player.move_ip(0, SPEED)

    # Keep player inside the screen boundaries
    player.clamp_ip(screen.get_rect())

    # Collision with the lake
    if player.colliderect(water):
        player.x -= SPEED if key[pygame.K_RIGHT] else -SPEED if key[pygame.K_LEFT] else 0
        player.y -= SPEED if key[pygame.K_DOWN] else -SPEED if key[pygame.K_UP] else 0

    # Start fishing
    if key[pygame.K_SPACE] and near_water and not fishing and in_range:
        fishing = True
        fishing_result = None
        bobber_x_offset = 0
        bobber_y_offset = 0
        waiting_for_bite = True
        bite_time = pygame.time.get_ticks() + random.randint(2000, 4000)  # Random wait 2-4 sec
        
        # Randomize bobber position within the lake
        if player.centerx < water.centerx:  # Player is to the left of the lake
            random_bobber_pos = (random.randint(water.left + 20, water.right - 20), random.randint(water.top + 20, water.bottom - 20))
        elif player.centerx > water.centerx:  # Player is to the right of the lake
            random_bobber_pos = (random.randint(water.left + 20, water.right - 20), random.randint(water.top + 20, water.bottom - 20))
        elif player.centery < water.centery:  # Player is above the lake
            random_bobber_pos = (random.randint(water.left + 20, water.right - 20), random.randint(water.top + 20, water.bottom - 20))
        else:  # Player is below the lake
            random_bobber_pos = (random.randint(water.left + 20, water.right - 20), random.randint(water.top + 20, water.bottom - 20))

        # Set the bobber center for spinning
        bobber_center = random_bobber_pos  # Store the center point to spin around

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)  # Maintain FPS

# Quit the game
pygame.quit()
