#Importing the required libraries
import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants for the game window and game settings
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GAME_DURATION = 30  # in seconds

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Game")

# Clock to control FPS
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5

    def update(self):
        # Basic movement controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Wrap around screen edges
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.speed = random.randint(1, 3)
        self.direction = random.uniform(0, math.pi * 2)

    def update(self):
        # Move the asteroid
        self.rect.x += self.speed * math.cos(self.direction)
        self.rect.y += self.speed * math.sin(self.direction)

        # Wrap around screen edges
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

# Create sprites groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Score counter
score = 0

# Function to create new asteroids
def create_asteroid():
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

# Timer variables
game_start_time = pygame.time.get_ticks()
game_over = False

# Main game loop
while not game_over:
    # Keep loop running at the right speed
    clock.tick(FPS)

    # Calculate elapsed time
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - game_start_time) / 1000  # convert to seconds

    # Process input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Check if time is up
    if elapsed_time >= GAME_DURATION:
        game_over = True

    # Spawn asteroids randomly
    if random.random() < 0.01:
        create_asteroid()

    # Update
    all_sprites.update()

    # Check for collisions (player with asteroids)
    hits = pygame.sprite.spritecollide(player, asteroids, True)
    if hits:
        # Increment score for each hit
        score += len(hits) * 10

    # Render/Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Display the timer
    timer_text = font.render(f"Time: {max(GAME_DURATION - int(elapsed_time), 0)}", True, WHITE)
    screen.blit(timer_text, (WIDTH - 150, 10))

    # After drawing everything, flip the display
    pygame.display.flip()

# Main loop has ended, display a goodbye message briefly
goodbye_font = pygame.font.Font(None, 50)
goodbye_text = goodbye_font.render("Thanks for playing!", True, WHITE)
screen.fill(BLACK)
screen.blit(goodbye_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

# Display final score
final_score_font = pygame.font.Font(None, 36)
final_score_text = final_score_font.render(f"Final Score: {score}", True, WHITE)
screen.blit(final_score_text, (WIDTH // 2 - 120, HEIGHT // 2 + 10))

pygame.display.flip()

# Pause briefly before exiting
pygame.time.wait(5000)

# Exit the game
pygame.quit()
sys.exit()
