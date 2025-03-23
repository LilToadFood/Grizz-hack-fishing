import pygame
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.load("fishing_music.mp3")
pygame.mixer.music.play(-1)

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
LAKE_WIDTH, LAKE_HEIGHT = 400, 300
SPEED = 5  # Player movement speed
WHITE, BLUE, BROWN, YELLOW, BLACK = (255, 255, 255), (55, 55, 255), (150, 75, 0), (255, 255, 0), (0, 0, 0)

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
bobber_angle = 0
fishing_result = None
bite_time = 0
waiting_for_bite = False
random_bobber_pos = None
bobber_center = None

# Math variables
show_math_question = False
math_question = ""
math_answer = 0
user_input = ""
score = 0

# Generate random math question
def generate_math_question():
    global math_question, math_answer
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(["+", "-", "*", "/"])

    if operation == "+":
        math_answer = num1 + num2
        math_question = f"{num1} + {num2} = ?"
    elif operation == "-":
        math_answer = num1 - num2
        math_question = f"{num1} - {num2} = ?"
    elif operation == "*":
        math_answer = num1 * num2
        math_question = f"{num1} x {num2} = ?"
    else:
        # Ensure division results in an integer
        math_answer = num1
        num1 = num1 * num2
        math_question = f"{num1} / {num2} = ?"

# Game loop
run = True
while run:

    screen.fill((0, 150, 0))

    # Draw lake
    pygame.draw.rect(screen, BLUE, water)

    # Draw player
    pygame.draw.rect(screen, (255, 0, 0), player)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Check if player is near water
    near_water = player.colliderect(water.inflate(50, 50))
    in_range = near_water

    # Display fishing prompt
    if near_water and not fishing and not show_math_question:
        text = font.render("Press SPACE to fish!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))

    # Fishing animation
    if fishing:
        # Draw fishing line
        line_start = player.midbottom
        line_end = random_bobber_pos
        pygame.draw.line(screen, YELLOW, line_start, line_end, 3)

        # Draw bobber
        pygame.draw.circle(screen, BROWN, random_bobber_pos, 7)

        # Bobber spinning animation
        if bobber_center:
            bobber_angle += 0.1
            bobber_x = bobber_center[0] + 5 * math.cos(bobber_angle)
            bobber_y = bobber_center[1] + 5 * math.sin(bobber_angle)
            random_bobber_pos = (int(bobber_x), int(bobber_y))

        # Check for bite
        if waiting_for_bite and pygame.time.get_ticks() > bite_time:
            fishing_result = random.choice([True, False])
            fishing = False
            waiting_for_bite = False

            if fishing_result:
                show_math_question = True
                generate_math_question()

    # Display fish result
    if fishing_result is not None and not show_math_question:
        result_text = "You caught a fish!" if fishing_result else "Nothing bit this time..."
        color = (200, 200, 200) if fishing_result else BLACK
        fish = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100, 200, 200)
        pygame.draw.rect(screen, color, fish)
        text = font.render(result_text, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100))

    # Math question logic
    if show_math_question:
        # Display math question and input box
        question_text = font.render(math_question, True, WHITE)
        screen.blit(question_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))

        # Draw input box
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50)
        pygame.draw.rect(screen, BLACK, input_box)
        input_text = font.render(user_input, True, WHITE)
        screen.blit(input_text, (input_box.x + 10, input_box.y + 10))

    # Movement logic
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and not fishing and not show_math_question:
        player.move_ip(-SPEED, 0)
    elif key[pygame.K_RIGHT] and not fishing and not show_math_question:
        player.move_ip(SPEED, 0)
    if key[pygame.K_UP] and not fishing and not show_math_question:
        player.move_ip(0, -SPEED)
    elif key[pygame.K_DOWN] and not fishing and not show_math_question:
        player.move_ip(0, SPEED)

    # Keep player inside the screen boundaries
    player.clamp_ip(screen.get_rect())

    # Start fishing
    if key[pygame.K_SPACE] and near_water and not fishing and not show_math_question:
        fishing = True
        fishing_result = None
        waiting_for_bite = True
        bite_time = pygame.time.get_ticks() + random.randint(2000, 4000)

        # Randomize bobber position within the lake
        random_bobber_pos = (
            random.randint(water.left + 20, water.right - 20),
            random.randint(water.top + 20, water.bottom - 20)
        )
        bobber_center = random_bobber_pos

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if show_math_question and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_input.isdigit() and int(user_input) == math_answer:
                    score += 1
                    show_math_question = False
                else:
                    print("Game Over")
                    run = False
                user_input = ""
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
