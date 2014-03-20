__author__ = 'a.kozlowski'

import pygame
from pygame.locals import *
from random import randint


class Snake(object):
    game_speed = 10 #fps limit
    screen_w = 800
    screen_h = 640
    map_margin_y = 40 #space for displaying score during game
    map_w = 40 #tiles x
    map_h = 30 #tiles y
    surface_color = (55, 55, 55)
    last_update_time = 0
    window_caption = "GeekSnake"

    def __init__(self):
        pygame.init()

        #init game vars
        self.map = None
        self.snake = None
        self.dir = 'r'
        self.new_dir = 'r' #we use htis var to keep store button pressed beetwen frames
        self.apple = None
        self.running = False
        self.score = -1 #-1 means its first game
        self.img_apple = pygame.image.load('data/apple.png')
        self.img_border = pygame.image.load('data/border.png')
        self.img_snake = pygame.image.load('data/snake.png')
        self.img_logo = pygame.image.load('data/logo.png')

        self.tile_h = (self.screen_h - self.map_margin_y) / self.map_h
        self.tile_w = self.screen_w / self.map_w

        #inti pygame window
        flag = DOUBLEBUF
        self.surface = pygame.display.set_mode((self.screen_w, self.screen_h), flag)

        pygame.display.set_caption(self.window_caption)
        self.font = pygame.font.SysFont('Arial', 20)
        self.clock = pygame.time.Clock()

        self.start()

    def _start_new_game(self):
        self.score = 0
        self.dir = 'r'
        self.running = True
        self.snake = [(10, 10), (11, 10), (12, 10)]
        self.map = []

        #generate new map
        self.map.append([1] * self.map_w)
        for i in range(self.map_h - 2):
            row = [0] * (self.map_w - 2)
            row.insert(0, 1)
            row.append(1)
            self.map.append(row)
        self.map.append([1] * self.map_w)

        #create first apple
        self._create_apple()

    def _update_game(self):
        snake_head = self.snake[-1]

        if self.dir == 'r':
            snake_new_point = (snake_head[0] + 1, snake_head[1]) #direction right
        elif self.dir == 'l':
            snake_new_point = (snake_head[0] - 1, snake_head[1]) #direction left
        elif self.dir == 't':
            snake_new_point = (snake_head[0], snake_head[1] - 1) #direction top
        else:
            snake_new_point = (snake_head[0], snake_head[1] + 1) #direction down

        if (snake_new_point in self.snake) or (self.map[snake_new_point[1]][snake_new_point[0]] == 1):
            self.running = False
            return

        self.snake.append(snake_new_point)

        if snake_new_point == self.apple:
            self._create_apple()
            self.score += 10
        else:
            del self.snake[0]

    def _draw_game(self):
        self._draw_map()
        self._draw_snake()
        self._draw_apple()
        label_score = self.font.render("SCORE: " + str(self.score), 1, (255, 255, 0))
        self.surface.blit(label_score, (5, 8))

    def _draw_map(self):
        for y in range(self.map_h):
            for x in range(self.map_w):
                tile = int(self.map[y][x])
                if tile == 1:
                    self._drawBlock(self.img_border, x, y)

    def _draw_snake(self):
        for b in self.snake:
            self._drawBlock(self.img_snake, b[0], b[1])

    def _draw_apple(self):
        self._drawBlock(self.img_apple, self.apple[0], self.apple[1])

    def _create_apple(self):
        while True:
            appleY = randint(1, self.map_h - 2)
            appleX = randint(1, self.map_w - 2)
            collid = False
            for i in range(len(self.snake)):
                if appleX == self.snake[i][0] and appleY == self.snake[i][1]:
                    collid = True
            if not collid:
                break

        self.apple = (appleX, appleY)

    def _drawBlock(self, img, x, y):
        self.surface.blit(img, self._cord2screen(x, y))

    def _cord2screen(self, x, y):
        return self.tile_w * x, (y * self.tile_h) + self.map_margin_y

    def _drawMenu(self):
        self.surface.blit(self.img_logo, (self.screen_w / 2 - self.img_logo.get_rect().w / 2, 20))
        if self.score >= 0:
            label_score = self.font.render("Game Over! Score: " + str(self.score), 1, (255, 255, 0))
            lscw, lsch = label_score.get_size()
            self.surface.blit(label_score, ((self.screen_w / 2 - lscw / 2), 150))

        label_start = self.font.render("Press `S` to start new game", 1, (255, 255, 0))
        lsw, lsh = label_start.get_size()
        self.surface.blit(label_start, ((self.screen_w / 2 - lsw / 2), self.screen_h / 2 - lsh))

    def _handle_events(self):
        keys = pygame.key.get_pressed()
        if self.running:
            if keys[pygame.K_w] and not self.dir == 'd':
                self.new_dir = 't'
            if keys[pygame.K_s] and not self.dir == 't':
                self.new_dir = 'd'
            if keys[pygame.K_a] and not self.dir == 'r':
                self.new_dir = 'l'
            if keys[pygame.K_d] and not self.dir == 'l':
                self.new_dir = 'r'
        else:
            if keys[pygame.K_s]:
                self._start_new_game()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return True
                #cleer screen
            self.surface.fill(self.surface_color)
            self._handle_events()
            self.last_update_time += self.clock.tick(30)
            if self.running:
                if self.last_update_time > (1000 / self.game_speed):
                    self.last_update_time = 0
                    self.dir = self.new_dir
                    self._update_game()
                self._draw_game()
            else:
                self._drawMenu()
                #update screen
            pygame.display.flip()


if __name__ == "__main__":
    game = Snake()

