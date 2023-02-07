import pygame
import random
import sys

screen_width = 600
screen_height = 600
grid_size = 20
grid_adet_x = int(screen_width / grid_size)
grid_adet_y = int(screen_height / grid_size)

up = (0,-1)
down = (0,1)
right = (1,0)
left = (-1,0)

snake_color = (34,34,34)
food_color = (250,200,0)


class Snake:
    def __init__(self, color):
        self.positions = [(random.randint(0,(grid_adet_x)-1)*grid_size, random.randint(0,(grid_adet_y)-1)*grid_size)]
        self.lenght = 1
        self.color = color
        self.direction = random.choice([up,down,right,left])
        self.score = 0
    def update(self, surface):
        for pos in self.positions:
            part = pygame.Rect(pos, (grid_size, grid_size))
            pygame.draw.rect(surface, self.color, part)
    def move(self):
        head = self.positions[0]
        new_pos = (head[0] + (self.direction[0])*grid_size, head[1] + (self.direction[1]*grid_size))
        if new_pos[0] in range(screen_width) and new_pos[1] in range(screen_height) and new_pos not in self.positions[2:]:
            self.positions.insert(0, new_pos) #yeni kafa
            if len(self.positions) > self.lenght:
                self.positions.pop()
        else:
            self.reset()
    def reset(self):
        self.lenght = 1
        self.positions = [(screen_width/2, screen_height/2)]
        self.direction = random.choice([right, left, up, down])
        self.score = 0

    def go(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        else:
            self.direction = direction
        
    def handle_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.go(up)
                elif event.key == pygame.K_DOWN:
                    self.go(down)
                elif event.key == pygame.K_RIGHT:
                    self.go(right)
                elif event.key == pygame.K_LEFT:
                    self.go(left)

class Enemy:
    def __init__(self, color, positions):
        self.color = color
        self.positions = positions
    def update(self, surface):
        for pos in self.positions:
            part = pygame.Rect(pos, (grid_size, grid_size))
            pygame.draw.rect(surface, self.color, part)

class Food:
    def __init__(self):
        self.position = (0,0)
        self.color = food_color
        self.randomly()
    def randomly(self):
        rnd_x = random.randint(0,(grid_adet_x)-1)*grid_size
        rnd_y = random.randint(0,(grid_adet_y)-1)*grid_size
        self.position = (rnd_x, rnd_y)
    def update(self, surface):
        my_food = pygame.Rect((self.position), (grid_size, grid_size))
        pygame.draw.rect(surface, self.color, my_food)