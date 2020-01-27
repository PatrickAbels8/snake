import os
import pygame
import random
import neat
pygame.font.init()

WINDOW_WIDTH = 500
FPS = 5
OFFSET = 20
STROKE = 1
TILE_WIDTH = 7
TILES_PER_ROW = 50

FONT = pygame.font.SysFont("arial", 20)

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption("Snake")

gen = 0


class Snake:
    COLOR = (0, 0, 255)
    RADIUS = 3
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, body):
        self.body = body
        self.direction = self.UP
        self.x, self.y = body[0]

    def draw(self, win):
        for x, y in self.body:
            position = (x*(STROKE+TILE_WIDTH)+OFFSET-round(TILE_WIDTH/2),
                        y*(STROKE+TILE_WIDTH)+OFFSET-round(TILE_WIDTH/2))
            pygame.draw.circle(win, self.COLOR, position, self.RADIUS)

    def move(self):
        cur_x, cur_y = self.body[0]
        for i in range(len(self.body)-1, 0, -1):
            self.body[i] = self.body[i-1]

        if self.direction == self.RIGHT:
            self.body[0] = (cur_x+1, cur_y)
        elif self.direction == self.LEFT:
            self.body[0] = (cur_x-1, cur_y)
        elif self.direction == self.UP:
            self.body[0] = (cur_x, cur_y-1)
        elif self.direction == self.DOWN:
            self.body[0] = (cur_x, cur_y+1)

    def turn(self, direction):
        if direction == self.RIGHT:
            self.direction = (self.direction+1) % 4
        elif direction == self.LEFT:
            self.direction = (self.direction-1) % 4

    def grow(self):
        tail_x, tail_y = self.body[len(self.body)-1]
        if self.direction == self.RIGHT:
            self.body.append((tail_x-1, tail_y))
        elif self.direction == self.LEFT:
            self.body.append((tail_x+1, tail_y))
        elif self.direction == self.UP:
            self.body.append((tail_x, tail_y+1))
        elif self.direction == self.DOWN:
            self.body.append((tail_x, tail_y-1))

    def dead(self):
        head_x, head_y = self.body[0]
        tail_x, tail_y = self.body[len(self.body)-1]
        if head_x < 1 or head_x > 50 or head_y > 50 or head_y < 1:
            return True
        for i in range(1, len(self.body)-1):
            x, y = self.body[i]
            if x == tail_x and y == tail_y or x == head_x and y == head_y:
                return True
        return False


class Apple:
    COLOR = (255, 0, 0)
    RADIUS = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.eaten = False

    def draw(self, win):
        position = (self.x * (STROKE + TILE_WIDTH) + OFFSET - round(TILE_WIDTH / 2),
                    self.y * (STROKE + TILE_WIDTH) + OFFSET - round(TILE_WIDTH / 2))
        pygame.draw.circle(win, self.COLOR, position, self.RADIUS)

    def collide(self, snake):
        x, y = snake.body[0]
        return self.x == x and self.y == y

    def next(self):
        self.x = random.randint(1, TILES_PER_ROW)
        self.y = random.randint(1, TILES_PER_ROW)


def draw_window(win, snakes, apple, score, gen):
    for x in range(TILES_PER_ROW):
        for y in range(TILES_PER_ROW):
            rect = pygame.Rect(x*(STROKE+TILE_WIDTH)+OFFSET, y*(STROKE+TILE_WIDTH)+OFFSET, TILE_WIDTH, TILE_WIDTH)
            pygame.draw.rect(win, (255, 255, 255), rect)
    for snake in snakes:
        snake.draw(win)
    apple.draw(win)

    score_text = FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_text, (WINDOW_WIDTH-score_text.get_width()-10, WINDOW_WIDTH-20))
    gen_text = FONT.render("Gens: " + str(gen-1), 1, (255, 255, 255))
    win.blit(gen_text, (10, 10))
    alive_text = FONT.render("Alive: " + str(len(snakes)), 1, (255, 255, 255))
    win.blit(alive_text, (10, 50))

    pygame.display.update()


def eval_genomes(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1

    nets = []
    snakes = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake([(round(TILES_PER_ROW/2), round(TILES_PER_ROW/2))]))
        ge.append(genome)

    clock = pygame.time.Clock()
    apple = Apple(random.randint(1, TILES_PER_ROW), random.randint(1, TILES_PER_ROW))
    score = 0

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

        for snake in snakes:
            snake.move()

            if apple.collide(snake):
                ge[snakes.index(snake)].fitness += 1
                score += 1
                apple.next()
                snake.grow()
                output = nets[snakes.index(snake)].activate(snake.x, snake.y, apple.x, apple.y)
                if output[0] > 0.5:
                    snake.turn(Snake.RIGHT)
                elif output[0] < -0.5:
                    snake.turn(Snake.LEFT)

            if snake.dead():
                ge[snakes.index(snake)].fitness -= 1
                nets.pop(snakes.index(snake))
                ge.pop(snakes.index(snake))
                snakes.pop(snakes.index(snake))

        draw_window(win, snake, apple, score)

    print("score: " + str(score))


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    winner = p.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
