import pygame
import random

pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.load("fishing_music.mp3")
pygame.mixer.music.play(-1)
# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
LAKE_WIDTH, LAKE_HEIGHT = 400, 300
SPEED = 5  # Player movement speed
WHITE, BLUE, RED, YELLOW = (255, 255, 255), (55, 55, 255), (255, 0, 0), (255, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Player and lake objects
player = pygame.Rect(400, 100, 50, 50)
water = pygame.Rect((SCREEN_WIDTH / 2 - LAKE_WIDTH / 2, SCREEN_HEIGHT / 2 - LAKE_HEIGHT / 2, LAKE_WIDTH, LAKE_HEIGHT))

# Fishing variables
fishing = False
fishing_timer = 0
bobber_y_offset = 0
bobber_direction = 1  # 1 = down, -1 = up
fishing_result = None
bite_time = 0
waiting_for_bite = False

# Game loop
run = True
while run:
    screen.fill("green")

    # Draw lake
    pygame.draw.rect(screen, BLUE, water)

    # Draw player
    pygame.draw.rect(screen, RED, player)

    # Check if player is near water
    near_water = player.colliderect(water.inflate(20, 20))

    # Display fishing prompt
    if near_water and not fishing:
        text = font.render("Press SPACE to fish!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))

    # Fishing animation
    if fishing:
        # Draw fishing line
        line_start = player.midbottom
        line_end = (player.centerx, water.top + 40 + bobber_y_offset)
        pygame.draw.line(screen, YELLOW, line_start, line_end, 3)

        # Draw bobber (small red circle)
        pygame.draw.circle(screen, RED, line_end, 7)

        # Bobber movement (up & down)
        if waiting_for_bite:
            bobber_y_offset += bobber_direction
            if bobber_y_offset >= 10 or bobber_y_offset <= -10:
                bobber_direction *= -1  # Reverse movement

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
    if key[pygame.K_LEFT]:
        player.move_ip(-SPEED, 0)
    elif key[pygame.K_RIGHT]:
        player.move_ip(SPEED, 0)
    if key[pygame.K_UP]:
        player.move_ip(0, -SPEED)
    elif key[pygame.K_DOWN]:
        player.move_ip(0, SPEED)

    # Keep player inside the screen boundaries
    player.clamp_ip(screen.get_rect())

    # Collision with the lake
    if player.colliderect(water):
        player.x -= SPEED if key[pygame.K_RIGHT] else -SPEED if key[pygame.K_LEFT] else 0
        player.y -= SPEED if key[pygame.K_DOWN] else -SPEED if key[pygame.K_UP] else 0

    # Start fishing
    if key[pygame.K_SPACE] and near_water and not fishing:
        fishing = True
        fishing_result = None
        bobber_y_offset = 0
        bobber_direction = 1
        waiting_for_bite = True
        bite_time = pygame.time.get_ticks() + random.randint(2000, 4000)  # Random wait 2-4 sec

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)  # Maintain FPS

# Quit the game
pygame.quit()
