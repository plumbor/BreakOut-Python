from random import randint

import pygame
import random
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
class Player(pygame.Rect):  #silly change
    def __init__(self, x, y):
        super().__init__(x, y, 100, 25)   # arbitrary values TODO tweak
        self.vx = 0

    def draw(self):
        pygame.draw.rect(screen, 'orange', self, 0) # fill

    def update(self):
        self.x = pygame.mouse.get_pos()[0]-self.width/2
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width

class Ball(pygame.Rect):

    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = random.randint(0, 2) * random.choice([1, -1])
        self.vy = 8#random.randint(3, 4) # TODO tweak?

    def draw(self):
        pygame.draw.ellipse(screen, 'white', self, 0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 and self.vx < 0:
            self.vx *= -1
        elif self.x + self.w > screen.get_width() and self.vx > 0:
            self.vx *= -1
        if self.y < 0 and self.vy < 0:
            self.vy *= -1
        elif self.y  > screen.get_height():
            self. y = screen.get_height()//2

class Brick(pygame.Rect):
    WIDTH = 80
    HEIGHT = 20

    def __init__(self, x, y):
        super().__init__(x, y, Brick.WIDTH, Brick.HEIGHT)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.right_box = pygame.Rect(self.right-10, self.top+4, 8, 12)
        self.left_box = pygame.Rect(self.left+2, self.top + 4, 8, 12)


    def draw(self):
        pygame.draw.rect(screen, self.color, self, 0)

bricks = []
for x in range(10, screen.get_width()-Brick.WIDTH, Brick.WIDTH+4):
    for y in range(60, 300, Brick.HEIGHT+4):
        bricks.append(Brick(x, y))

player = Player(screen.get_width()/2 - 50, screen.get_height() - 50)
ball = Ball(screen.get_width()/2 - 10, screen.get_height()/2 +20, 20)

speed_player = 10
while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += -speed_player
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += speed_player
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += speed_player
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += -speed_player
    # Do logical updates here.
    player.update()
    ball.update()
    if ball.colliderect(player):
        ball.vy *= -1
        ball.y = player.y - ball.width # perhaps sideways collision would look better?
        diff = (ball.x + ball.w/2) - (player.x + player.w/2)
        ball.vx += diff // 10

    vy_bounce = False
    vx_bounce = False
    for brick in bricks:
        if ball.colliderect(brick):
            if ball.bottom > brick.bottom and ball.vy < 0:
                vy_bounce = True
            if ball.top < brick.top and ball.vy > 0:
                vy_bounce = True
            if not vy_bounce:
                if ball.colliderect(brick.right_box) and ball.right > brick.right_box.right and ball.vx < 0:
                    vx_bounce = True
                if ball.colliderect(brick.left_box) and ball.left < brick.left_box.left and ball.vx > 0:
                    vx_bounce = True
            bricks.remove(brick)

    if vy_bounce:
        ball.vy *= -1
    if vx_bounce:
        ball.vx *= -1


    screen.fill('grey')  # Fill the display with a solid color
    # Render the graphics here.
    player.draw()
    ball.draw()
    for b in bricks:
        b.draw()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)