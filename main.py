import pygame
import random
import os

pygame.init()
screen_width = 450
screen_height = 400

# Window creation
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
# pygame.display.set_icon()

# Start the clock
clock = pygame.time.Clock()

# Font Styles
font_large = pygame.font.SysFont(None, 55)
font_normal = pygame.font.SysFont(None, 40)
font_small = pygame.font.SysFont(None, 32)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Renders text on the pygame surface


def text_write(text, color, x_pos, y_pos, font_set=font_normal):
    screen_text = font_set.render(text, True, color)
    screen.blit(screen_text, [x_pos, y_pos])

# Draws the snake


def draw_snake(surface, color, snake_pos_list, snake_size,):
    for x_pos, y_pos in snake_pos_list:
        pygame.draw.rect(screen, black, [x_pos, y_pos, snake_size, snake_size])


def draw_food(surface, color, food_x, food_y, size):
    pygame.draw.rect(
        screen, red, [food_x, food_y, size, size])


def game_loop():
    # Game Specific Variables
    running = True
    game_state = "Home"
    score = 0
    border = 75
    padding = 10
    fps = 30
    score_bar_y_pos = 50
    if(not os.path.exists("high_score.txt")):
        with open("high_score.txt", 'w') as f:
            f.write("0")    
    with open("high_score.txt", 'r') as f:
        high_score = int(f.read())

    # Snake
    snake_size = 10
    snake_x = random.randrange(0, screen_width + 1 - snake_size, 10)
    snake_y = random.randrange(
        score_bar_y_pos, screen_height + 1 - snake_size, 10)
    velocity_x = 0
    velocity_y = 0
    init_velocity = 10
    snake_pos_list = []
    snake_length = 1
    snake_direction = ""

    # Food
    food_x = random.randrange(0, screen_width-snake_size + 1 - padding, 10)
    food_y = random.randrange(
        score_bar_y_pos, screen_height + 1 - snake_size, 10)

    # Game Loop
    while running:

        # Home Screen
        if game_state == "Home":
            screen.fill(white)
            text_write("Welcome to Snakes", red, 45, 80, font_large)
            text_write("Press Enter", red, 120, 160, font_large)
            text_write("To Start", red, 145, 240, font_large)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = "Running"

        # Exit Screen
        elif game_state == "Game-Over":
            screen.fill(white)
            text_write('Game Over', red, 120, 80, font_large)
            text_write('Press "Enter"', red, 100, 150, font_large)
            text_write('To Continue...', red, 100, 220, font_large)
            with open("high_score.txt", 'w') as f:
                f.write(str(high_score))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = "Home"
                        game_loop()

        # Game Screen
        elif game_state == "Running":

            # Event Handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake_direction != 'DOWN':
                        snake_direction = 'UP'
                        velocity_x = 0
                        velocity_y = -init_velocity
                    if event.key == pygame.K_DOWN and snake_direction != 'UP':
                        snake_direction = 'DOWN'
                        velocity_x = 0
                        velocity_y = init_velocity
                    if event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                        snake_direction = 'LEFT'
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                        snake_direction = 'RIGHT'
                        velocity_x = init_velocity
                        velocity_y = 0

            # Score update if food eaten
            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 10
                snake_length += 1
                food_x = random.randrange(
                    0, screen_width-snake_size + 1 - padding, 10)
                food_y = random.randrange(
                    score_bar_y_pos, screen_height + 1 - snake_size, 10)

                if score > high_score:
                    high_score = score

                    # Display Settings
            screen.fill(white)
            # Score bar background
            pygame.draw.rect(
                screen, black, [0, 0, screen_width, score_bar_y_pos])

            # Print Score on screen
            text_write("Score : " + str(score), green,
                       5, 10)
            text_write("   High Score : " + str(high_score), green,
                       180, 10)

            # Snake's current position
            snake_head = []
            snake_head.append(snake_x)
            snake_head.append(snake_y)

            snake_pos_list.append(snake_head)

            # Delete old heads
            if len(snake_pos_list) > snake_length:
                del snake_pos_list[0]

            # Self collision for snake
            if snake_head in snake_pos_list[:-1]:
                game_state = "Game-Over"

            # Border Checking
            if snake_x < 0:
                snake_x = 0
                game_state = "Game-Over"
            elif snake_x > screen_width - snake_size:
                snake_x = screen_width - snake_size
                game_state = "Game-Over"
            if snake_y < score_bar_y_pos:
                snake_y = 0
                game_state = "Game-Over"
            elif snake_y > screen_height - snake_size:
                snake_y = screen_height - snake_size
                game_state = "Game-Over"

            draw_snake(screen, black, snake_pos_list, snake_size)
            draw_food(screen, red, food_x, food_y, snake_size)

            snake_x += velocity_x
            snake_y += velocity_y

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


game_loop()
