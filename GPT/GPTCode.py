
import pygame
import random
from pygame.locals import *

pygame.init()

# Game window settings
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blue Dot Game")

# Dot settings
dot_radius = 10
dot_color = (0, 0, 255)
dot_position = [width // 2, height // 2]

# Enemies settings
enemy_radius = 10
enemy_color = (255, 0, 0)
enemy_count = 5
enemies = []

for _ in range(enemy_count):
    enemy_x = random.randint(enemy_radius, width - enemy_radius)
    enemy_y = random.randint(enemy_radius, height - enemy_radius)
    enemy_speed = [random.choice([-1, 1]), random.choice([-1, 1])]
    enemies.append({"position": [enemy_x, enemy_y], "speed": enemy_speed})

# Coins settings
coin_radius = 5
coin_color = (255, 255, 0)
coin_count = 10
coins = []

for _ in range(coin_count):
    coin_x = random.randint(coin_radius, width - coin_radius)
    coin_y = random.randint(coin_radius, height - coin_radius)
    coins.append([coin_x, coin_y])

# Game variables
score = 0
font = pygame.font.Font(None, 36)

# Check for collisions between the dot and the enemies or coins
def check_collision(dot_pos, other_pos, radius):
    x_diff = dot_pos[0] - other_pos[0]
    y_diff = dot_pos[1] - other_pos[1]
    distance = (x_diff**2 + y_diff**2)**0.5
    return distance <= radius * 2

# Game loop settings
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()

    # Move the dot using arrow keys
    if keys[K_UP] and dot_position[1] - dot_radius > 0:
        dot_position[1] -= 5
    if keys[K_DOWN] and dot_position[1] + dot_radius < height:
        dot_position[1] += 5
    if keys[K_LEFT] and dot_position[0] - dot_radius > 0:
        dot_position[0] -= 5
    if keys[K_RIGHT] and dot_position[0] + dot_radius < width:
        dot_position[0] += 5

    # Move and draw the enemies
    window.fill((0, 0, 0))
    for enemy in enemies:
        enemy['position'][0] += enemy['speed'][0] * 5
        enemy['position'][1] += enemy['speed'][1] * 5

        if enemy['position'][0] <= enemy_radius or enemy['position'][0] >= width - enemy_radius:
            enemy['speed'][0] *= -1
        if enemy['position'][1] <= enemy_radius or enemy['position'][1] >= height - enemy_radius:
            enemy['speed'][1] *= -1

        if check_collision(dot_position, enemy['position'], dot_radius):
            running = False

        pygame.draw.circle(window, enemy_color, enemy['position'], enemy_radius)

    # Collect coins and update score
    for coin in coins[:]:
        if check_collision(dot_position, coin, dot_radius):
            coins.remove(coin)
            score += 1

    # Draw coins
    for coin in coins:
        pygame.draw.circle(window, coin_color, coin, coin_radius)

    # Draw score
    score_text = font.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(score_text, (10, 10))

    # Draw the dot
    pygame.draw.circle(window, dot_color, dot_position, dot_radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
