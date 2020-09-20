import pygame

pygame.init()

# Window creation
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Snake")
# pygame.display.set_icon()

# Game Specific Variables
running = True
game_over = False

snake_x = 200
snake_y = 300
snake_size = 10
velocity_x = 5
velocity_y = 5

fps = 30
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Game Loop
while running:

    pygame.display.update()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                velocity_y = -10
            if event.key == pygame.K_DOWN:
                velocity_y = 10
            if event.key == pygame.K_LEFT:
                snake_x -= -10
            if event.key == pygame.K_RIGHT:
                snake_x += 10
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_UP:
        #         snake_y -= 10

    screen.fill(white)

    pygame.draw.rect(screen, black, [snake_x, snake_y, snake_size, snake_size])

    snake_x += velocity_x
    snake_y += velocity_y
    clock.tick(fps)


pygame.quit()
quit()
