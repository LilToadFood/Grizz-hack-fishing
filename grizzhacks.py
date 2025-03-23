import pygame
import random
import time
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36

display_duration = 10  # Seconds
 
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fishing Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Player setup
player_size = 40
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_size - 10]
player_speed = 5

# Fishing variables
fishing = False
bite_time = None
word = ""
words = ["deceitful", "perseverance", "quizzical", "surreptitious", "ubiquitous", "voracious", "acrimonious", "belligerent", "capricious"]
typed_word = ""
word_appear_time = None
show_word = False

def draw():
    screen.fill(GREEN)
    pygame.draw.rect(screen, BLUE, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    pygame.draw.rect(screen, WHITE, (*player_pos, player_size, player_size))
    
    if fishing:
        pygame.draw.line(screen, BLACK, (player_pos[0] + player_size // 2, player_pos[1] + player_size),
                         (player_pos[0] + player_size // 2, SCREEN_HEIGHT // 2), 2)
    
    if show_word and time.time() - word_appear_time < display_duration:
        word_surf = font.render(word, True, BLACK)
        screen.blit(word_surf, (SCREEN_WIDTH // 2 - word_surf.get_width() // 2, 50))
    elif word:
        # Display typing box
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 150, 50, 300, 50))
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 150, 50, 300, 50), 2)
        typed_surf = font.render(typed_word, True, BLACK)
        screen.blit(typed_surf, (SCREEN_WIDTH // 2 - 140, 60))
    
    pygame.display.flip()

def handle_input():
    global fishing, bite_time, word, typed_word, word_appear_time, show_word
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT // 2 - player_size:
        player_pos[1] += player_speed
    
    # Cast fishing rod
    if keys[pygame.K_SPACE] and not fishing and player_pos[1] < SCREEN_HEIGHT // 2:
        fishing = True
        bite_time = time.time() + random.randint(2, 10)
        word = ""
        typed_word = ""
        show_word = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            elif event.key == pygame.K_RETURN:
                if typed_word == word:
                    print("Correct!")
                    word = ""
                    typed_word = ""
                    show_word = False
                else:
                    print("Try again!")
            else:
                typed_word += event.unicode

def fishing_logic():
    global fishing, word, word_appear_time, show_word
    if fishing and time.time() >= bite_time:
        fishing = False
        word = random.choice(words)
        word_appear_time = time.time()
        show_word = True

def main():
    while True:
        handle_input()
        fishing_logic()
        draw()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
