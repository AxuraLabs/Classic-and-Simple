import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

# Bird settings
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_X = 50
BIRD_Y = 300
BIRD_FLAP_VEL = -9
BIRD_DROP_VEL = 1
MAX_DROP_SPEED = 10
FLAP_POWER = -9

# Pipe settings
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 200  # Increased gap
PIPE_VEL = -4
NEW_PIPE_SPACE = 200

# Frame settings
FPS = 60

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = BIRD_Y
        self.vel = 0
        self.color = RED

    def flap(self):
        self.vel = BIRD_FLAP_VEL

    def move(self):
        self.vel += BIRD_DROP_VEL
        if self.vel > MAX_DROP_SPEED:
            self.vel = MAX_DROP_SPEED
        self.y += self.vel
        self.y = min(self.y, SCREEN_HEIGHT - BIRD_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, 350)
        self.top = self.height - PIPE_HEIGHT
        self.bottom = self.height + PIPE_GAP
        self.color = GREEN

    def move(self):
        self.x += PIPE_VEL

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.top, PIPE_WIDTH, PIPE_HEIGHT))
        pygame.draw.rect(screen, self.color, (self.x, self.bottom, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom))

    def get_rects(self):
        top_rect = pygame.Rect(self.x, self.top, PIPE_WIDTH, PIPE_HEIGHT)
        bottom_rect = pygame.Rect(self.x, self.bottom, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom)
        return top_rect, bottom_rect

def game():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH), Pipe(SCREEN_WIDTH + NEW_PIPE_SPACE)]
    score = 0
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.move()

        new_pipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                new_pipe = True

        if new_pipe:
            pipes.append(Pipe(SCREEN_WIDTH))
            score += 1

        bird_rect = bird.get_rect()
        for pipe in pipes:
            top_rect, bottom_rect = pipe.get_rects()
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                running = False

        if bird.y >= SCREEN_HEIGHT - BIRD_HEIGHT:
            running = False

        screen.fill(CYAN)
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        pygame.display.update()

    print("Game Over! Your score was:", score)
    pygame.time.wait(1000)  # Wait for a second before restarting
    return True

def main():
    while game():
        pass

if __name__ == '__main__':
    main()