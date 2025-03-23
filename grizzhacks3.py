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
SPEED = 5
WHITE, BLUE, BROWN, RED, BLACK = (255, 255, 255), (55, 55, 255), (150, 75, 0), (255, 0, 0), (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# 🎯 Player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("player.png.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def clamp(self, bounds):
        self.rect.clamp_ip(bounds)

# Fish sprite class
class Fish(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(self.image, (200, 200))  # Resize fish image
        self.rect = self.image.get_rect(topleft=(x, y))

# Create player sprite
player = Player(400, 100)

# Lake object
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
strikes = 0
game_over = False

# Images for fish and strike
fish_image = pygame.image.load("fish.png.png").convert_alpha()
fish_image_2 = pygame.image.load("fish-2.png.png").convert_alpha()
fish_image_3 = pygame.image.load("fish-3.png.png").convert_alpha()

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
        math_answer = num1 // num2 if num2 != 0 else 0  # Avoid division by zero
        math_question = f"{num1} / {num2} = ?"

# Reset fishing state
def reset_fishing():
    global fishing, fishing_result, show_math_question, user_input, waiting_for_bite
    fishing = False
    fishing_result = None
    show_math_question = False
    user_input = ""
    waiting_for_bite = False

# Game loop
run = True
fish_displayed = False  # Flag to track fish display
fish_group = pygame.sprite.Group()  # Create a group to manage fish sprites

while run:
    screen.fill((0, 150, 0))

    # Draw lake
    pygame.draw.rect(screen, BLUE, water)

    # Draw player sprite
    screen.blit(player.image, player.rect.topleft)

    # Display score and strikes
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    strike_text = font.render(f"Strikes: {strikes}/3", True, WHITE)
    screen.blit(strike_text, (SCREEN_WIDTH - 150, 10))

    # Check if player is near water
    near_water = player.rect.colliderect(water.inflate(50, 50))
    in_range = near_water

    # Display fishing prompt
    if near_water and not fishing and not show_math_question and not game_over:
        text = font.render("Press SPACE to fish!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))

    # Fishing animation
    if fishing:
        # Draw fishing line
        line_start = (player.rect.x + 35, player.rect.y + 2)
        line_end = random_bobber_pos
        pygame.draw.line(screen, WHITE, line_start, line_end, 3)

        # Draw bobber
        pygame.draw.circle(screen, BROWN, random_bobber_pos, 7)

        # Bobber animation
        if bobber_center:
            bobber_angle += 0.1
            bobber_x = bobber_center[0] + 5 * math.cos(bobber_angle)
            bobber_y = bobber_center[1] + 5 * math.sin(bobber_angle)
            random_bobber_pos = (int(bobber_x), int(bobber_y))

        # Check for bite
        if waiting_for_bite and pygame.time.get_ticks() > bite_time:
            fishing_result = random.choice([True, False])
            waiting_for_bite = False

            if fishing_result:
                show_math_question = True
                generate_math_question()
            else:
                # Show nothing message briefly
                pygame.time.delay(500)
                reset_fishing()

    # Display fish result
    if fishing_result and not show_math_question and not fish_displayed:
        # Show fish after answering correctly
        random_number = random.randint(1, 30)
        if random_number <= 100:
            fish_image_to_display = fish_image
        elif 101 <= random_number <= 200:
            fish_image_to_display = fish_image_2
        else:
            fish_image_to_display = fish_image_3

        fish = Fish(fish_image_to_display, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100)
        fish_group.add(fish)  # Add fish to sprite group
        fish_displayed = True  # Set flag to prevent multiple fish displays

        fishing_result = False  # Stop the fish from being shown again

    # Update and draw fish
    fish_group.update()  # Update fish states
    fish_group.draw(screen)  # Draw all fish in the group

    # Math question logic
    if show_math_question:
        # Display math question
        question_text = font.render(math_question, True, WHITE)
        screen.blit(question_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150))

        # Draw input box
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50)
        pygame.draw.rect(screen, BLACK, input_box)
        input_text = font.render(user_input, True, WHITE)
        screen.blit(input_text, (input_box.x + 10, input_box.y + 10))

    # Movement logic
    key = pygame.key.get_pressed()
    if not fishing and not show_math_question and not game_over:
        if key[pygame.K_LEFT]:
            player.move(-SPEED, 0)
        elif key[pygame.K_RIGHT]:
            player.move(SPEED, 0)
        if key[pygame.K_UP]:
            player.move(0, -SPEED)
        elif key[pygame.K_DOWN]:
            player.move(0, SPEED)

    # Keep player inside the screen boundaries
    player.clamp(screen.get_rect())

    # Handle fishing with SPACE
    if key[pygame.K_SPACE] and near_water and not fishing and not show_math_question and not game_over:
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
                if user_input == str(math_answer):  # Check if the user input matches the math answer
                    score += 1
                else:
                    strikes += 1
                    if strikes >= 3:
                        game_over = True
                reset_fishing()
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode

        # Remove fish if player moves or presses space
        if fish_displayed and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                fish_group.empty()  # Remove all fish
                fish_displayed = False  # Reset fish display flag

    # Quit game on 3 strikes
    if game_over:
        print("Game Over!")
        run = False

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
