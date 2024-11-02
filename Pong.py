import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5  # Adjust paddle speed if needed
BALL_SPEED_X, BALL_SPEED_Y = 4, 4  # Slower ball
GRAVITY = 0.2  # Increased gravity effect

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Gravity Adjustments")

# Ball and paddle positions
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [random.choice([-BALL_SPEED_X, BALL_SPEED_X]), random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])]
player_paddle_pos = [PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2]
ai_paddle_pos = [WIDTH - 2 * PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2]

def reset_ball():
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_vel = [random.choice([-BALL_SPEED_X, BALL_SPEED_X]), random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])]

def draw():
    screen.fill(BLACK)
    # Draw player paddle
    pygame.draw.rect(screen, BLUE, (player_paddle_pos[0], player_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    # Draw AI paddle
    pygame.draw.rect(screen, RED, (ai_paddle_pos[0], ai_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    # Draw ball
    pygame.draw.ellipse(screen, GREEN, (ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2))
    pygame.display.flip()

def move_ball():
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Apply gravity to ball's vertical velocity
    ball_vel[1] += GRAVITY

    # Ball bouncing on top or bottom
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # Ball bouncing on paddles
    if (ball_pos[0] <= player_paddle_pos[0] + PADDLE_WIDTH and player_paddle_pos[1] < ball_pos[1] < player_paddle_pos[1] + PADDLE_HEIGHT) or \
       (ball_pos[0] >= ai_paddle_pos[0] - BALL_RADIUS and ai_paddle_pos[1] < ball_pos[1] < ai_paddle_pos[1] + PADDLE_HEIGHT):
        ball_vel[0] = -ball_vel[0]

def move_player(keys):
    if keys[pygame.K_w] and player_paddle_pos[1] > 0:
        player_paddle_pos[1] -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT:
        player_paddle_pos[1] += PADDLE_SPEED

def move_ai():
    # Enhanced AI movement
    if ai_paddle_pos[1] + PADDLE_HEIGHT / 2 < ball_pos[1] - 10:
        ai_paddle_pos[1] += PADDLE_SPEED
    elif ai_paddle_pos[1] + PADDLE_HEIGHT / 2 > ball_pos[1] + 10:
        ai_paddle_pos[1] -= PADDLE_SPEED

    ai_paddle_pos[1] = max(min(ai_paddle_pos[1], HEIGHT - PADDLE_HEIGHT), 0)

def main():
    running = True
    clock = pygame.time.Clock()
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Reset game on Spacebar press
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    reset_ball()

        keys = pygame.key.get_pressed()
        
        if not game_over:
            move_player(keys)
            move_ai()
            move_ball()
            draw()
        
        # Check if game over
        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
            game_over = True
            draw_text_middle("Press Space to Restart", 32, WHITE, screen)
            pygame.display.update()

        clock.tick(60)  # Set a reasonable frame rate

    pygame.quit()

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.fill(BLACK)
    surface.blit(label, (WIDTH / 2 - label.get_width() / 2, HEIGHT / 2 - label.get_height() / 2))

if __name__ == "__main__":
    main()