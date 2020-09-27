# flake8: noqa = E501

import random
import os
import sys

from pygame.locals import *
import pygame

# Window creation
pygame.init()
pygame.font.init()
screen_width = 450
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
icon = pygame.image.load("data/images/snake.png")
pygame.display.set_icon(icon)

# Start the clock
clock = pygame.time.Clock()
fps = 30

# Font Styles
font_large = pygame.font.SysFont('comicsansms', 45)
font_normal = pygame.font.SysFont('comicsansms', 30)
font_small = pygame.font.SysFont('comicsansms', 22)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (50, 50, 50)
GRAY = (192, 192, 192)
RED = (220, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# Helper Functions


def text_write(text, color, x_pos, y_pos, font_set=font_normal):
    screen_text = font_set.render(text, True, color)
    screen.blit(screen_text, [x_pos, y_pos])


def draw_snake(surface, color, snake_pos_list, snake_size,):
    for x_pos, y_pos in snake_pos_list:
        pygame.draw.rect(screen, BLACK, [x_pos, y_pos, snake_size, snake_size])


def draw_food(surface, color, food_x, food_y, size):
    pygame.draw.rect(
        screen, RED, [food_x, food_y, size, size])


def pause():
    running = True
    while running:

        # screen.fill((GRAY))
        text_write("Paused", RED, 150, 150, font_large)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(5)


# Screens

def main_menu():

    clicked = False
    while True:
        screen.fill(GRAY)
        text_write("Welcome to Snakes", RED, 20, 80, font_large)

        button_start = pygame.Rect(84, 223, 96, 45)
        button_quit = pygame.Rect(270, 223, 96, 45)

        mx, my = pygame.mouse.get_pos()

        # Check collision of Mouse and Button
        if button_start.collidepoint((mx, my)):
            pygame.draw.rect(screen, (RED), button_start)
            if clicked:
                game()
        else:
            pygame.draw.rect(screen, (DARKGRAY), button_start)
        if button_quit.collidepoint((mx, my)):
            pygame.draw.rect(screen, (RED), button_quit)
            if clicked:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, (DARKGRAY), button_quit)

        text_write("Start", GREEN, 92, 223)
        text_write("Quit", GREEN, 285, 223)

        # Event Handling
        clicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        pygame.display.update()
        clock.tick(fps)


def game():
    # Game Screen

    #  Game Specific Variables
    running = True
    score = 0
    padding = 10
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

    while running:

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

        # Set display properties
        screen.fill(GRAY)
        pygame.draw.rect(
            screen, DARKGRAY, [0, 0, screen_width, score_bar_y_pos])

        # Display Score
        text_write("Score : " + str(score), GREEN,
                   5, 5)
        text_write("   High Score : " + str(high_score), GREEN,
                   180, 5)

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
            game_end(high_score)
            break

        # Border Checking
        if snake_x < 0:
            snake_x = 0
            game_end(high_score)
            break
        elif snake_x > screen_width - snake_size:
            snake_x = screen_width - snake_size
            game_end(high_score)
            break
        if snake_y < score_bar_y_pos:
            snake_y = 0
            game_end(high_score)
            break
        elif snake_y > screen_height - snake_size:
            snake_y = screen_height - snake_size
            game_end(high_score)
            break
        
        # Draw particles
        draw_snake(screen, DARKGRAY, snake_pos_list, snake_size)
        draw_food(screen, RED, food_x, food_y, snake_size)

        # Handling snake movement
        snake_x += velocity_x
        snake_y += velocity_y

        # Event Handling
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP and snake_direction != 'DOWN':
                    snake_direction = 'UP'
                    velocity_x = 0
                    velocity_y = -init_velocity
                if event.key == K_DOWN and snake_direction != 'UP':
                    snake_direction = 'DOWN'
                    velocity_x = 0
                    velocity_y = init_velocity
                if event.key == K_LEFT and snake_direction != 'RIGHT':
                    snake_direction = 'LEFT'
                    velocity_x = -init_velocity
                    velocity_y = 0
                if event.key == K_RIGHT and snake_direction != 'LEFT':
                    snake_direction = 'RIGHT'
                    velocity_x = init_velocity
                    velocity_y = 0
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause()

        pygame.display.update()
        clock.tick(fps)


def game_end(high_score):
    clicked = False
    running = True
    while running:
        screen.fill(GRAY)
        text_write('Game Over', RED, 120, 60, font_large)

        # Saving high Score
        with open("high_score.txt", 'w') as f:
            f.write(str(high_score))

        button_restart = pygame.Rect(175, 150, 100, 45)
        button_menu = pygame.Rect(175, 220, 100, 45)
        button_quit = pygame.Rect(175, 290, 100, 45)

        mx, my = pygame.mouse.get_pos()

        # Restart Button
        if button_restart.collidepoint((mx, my)):
            pygame.draw.rect(screen, (RED), button_restart)
            if clicked:
                running = False
                game()
                break
        else:
            pygame.draw.rect(screen, (DARKGRAY), button_restart)

        # Menu Bottom
        if button_menu.collidepoint((mx, my)):
            pygame.draw.rect(screen, (RED), button_menu)
            if clicked:
                running = False
                break
        else:
            pygame.draw.rect(screen, (DARKGRAY), button_menu)

        # Quit Button
        if button_quit.collidepoint((mx, my)):
            pygame.draw.rect(screen, (RED), button_quit)
            if clicked:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, (DARKGRAY), button_quit)

        text_write("Restart", GREEN, 185, 155, font_small)
        text_write("Menu", GREEN, 195, 225, font_small)
        text_write("Quit", GREEN, 200, 295, font_small)

        # Event Handling
        clicked = False
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        pygame.display.update()
        clock.tick(fps)

# Entry Point
main_menu()
