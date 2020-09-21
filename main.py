import pygame
import random

pygame.init()
screen_width = 400
screen_height = 400

# Window creation
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
# pygame.display.set_icon()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def text_write(text, color, x_pos, y_pos):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, [x_pos, y_pos])


def draw_snake(surface, color, snake_pos_list, snake_size,):
    for x_pos, y_pos in snake_pos_list:
        pygame.draw.rect(screen, black, [x_pos, y_pos, snake_size, snake_size])

# Game Loop


def game_loop():
    # Game Specific Variables
    running = True
    game_over = False
    score = 0
    border = 75
    padding = 10
    fps = 30
    score_bar_y_pos = 45

    # Snake
    snake_size = 10
    snake_x = random.randint(0, screen_width - snake_size)
    snake_y = random.randint(score_bar_y_pos, screen_height - snake_size)
    velocity_x = 0
    velocity_y = 0
    init_velocity = 10
    snake_pos_list = []
    snake_length = 1
    snake_direction = ""
    # Food
    food_x = random.randint(0, screen_width-snake_size - padding)
    food_y = random.randint(score_bar_y_pos, screen_height - snake_size)

    while running:
        if game_over:
            screen.fill(white)
            text_write('Game Over', red, 90, 100)
            text_write('Press "Enter"', red, 80, 170)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_over = False
                        game_loop()
                
        else:
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

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 1
                snake_length += 1
                food_x = random.randint(0, screen_width-snake_size - padding)
                food_y = random.randint(score_bar_y_pos, screen_height - snake_size)

            # Display Settings
            screen.fill(white)
            pygame.draw.rect(screen, black, [0, 0, screen_width, score_bar_y_pos]) # Score bar background
            text_write("Score : " + str(score * 10), green, 5, 5)   # Print Score on screen

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
                game_over = True

            # Border Checking
            if snake_x < 0:
                snake_x = 0
                game_over = True
            elif snake_x > screen_width - snake_size:
                snake_x = screen_width - snake_size
                game_over = True
            if snake_y < score_bar_y_pos:
                snake_y = 0
                game_over = True
            elif snake_y > screen_height - snake_size:
                snake_y = screen_height - snake_size
                game_over = True

            draw_snake(screen, black, snake_pos_list, snake_size)

            pygame.draw.rect(
                screen, red, [food_x, food_y, snake_size, snake_size])

            snake_x += velocity_x
            snake_y += velocity_y

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


game_loop()
