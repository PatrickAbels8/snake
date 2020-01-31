import pygame
import random


FPS = 5
WINDOW_WIDTH = 500
TILES_PER_WIDTH = 11
TILES_PER_HEIGHT = 20
OFFSET = 20
STROKE = 1
TILE_WIDTH = 15


class Block:
    LONG = 0
    BIGL = 1
    REC = 2
    ARROW = 3
    NOSE = 4
    SMALLL = 5

    RIGHT = 0
    LEFT = 1

    def __init__(self, form):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.form = form
        shift = round(TILES_PER_WIDTH/5)
        if form == Block.LONG:
            self.body = [[0, 0], [1, 0], [2, 0], [3, 0]]
        elif form == Block.BIGL:
            self.body = [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]]
        elif form == Block.REC:
            self.body = [[0, 0], [0, 1], [1, 1], [1, 0]]
        elif form == Block.ARROW:
            self.body = [[0, 0], [1, 0], [1, 1], [2, 1]]
        elif form == Block.NOSE:
            self.body = [[0, 0], [0, 1], [0, 2], [1, 1]]
        elif form == Block.SMALLL:
            self.body = [[0, 0], [0, 1], [0, 2], [1, 2]]

        for i in range(len(self.body)):
            self.body[i] = [self.body[i][0]+shift, self.body[i][1]]

    def draw(self, win):
        for x, y in self.body:
            rect = pygame.Rect(x * (STROKE + TILE_WIDTH) + OFFSET,
                               y * (STROKE + TILE_WIDTH) + OFFSET, 
                               TILE_WIDTH, TILE_WIDTH)
            pygame.draw.rect(win, self.color, rect)

    def move(self):
        for i in range(len(self.body)):
            self.body[i] = [self.body[i][0], self.body[i][1]+1]

    def bottom(self):
        for x, y in self.body:
            if y == TILES_PER_HEIGHT-1:
                return True
        return False

    # todo buggy
    def collide(self, blocks):
        for x, y in self.body:
            for block in blocks:
                for x_b, y_b in block.body:
                    if x==x_b and y+1==y_b:
                        print("colllllll")
                        return True
        return False

    def sidestep(self, direction):
        for i in range(len(self.body)):
            if direction == Block.RIGHT:
                self.body[i] = [self.body[i][0]+1, self.body[i][1]]
            if direction == Block.LEFT:
                self.body[i] = [self.body[i][0]-1, self.body[i][1]]

    def turn(self):
        head_x, head_y = self.body[0]
        for i in range(len(self.body)):
            x, y = self.body[i]
            dis_x, dis_y = head_x-x, head_y-y
            self.body[i] = [head_x-dis_y, head_y+dis_x]


def draw_window(win, blocks):
    for x in range(TILES_PER_WIDTH):
        for y in range(TILES_PER_HEIGHT):
            rect = pygame.Rect(x*(STROKE+TILE_WIDTH)+OFFSET, y*(STROKE+TILE_WIDTH)+OFFSET, TILE_WIDTH, TILE_WIDTH)
            pygame.draw.rect(win, (255, 255, 255), rect)
    for block in blocks:
        block.draw(win)
    pygame.display.update()



def main():
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
    blocks = []
    blocks.append(Block(random.randint(0, 5)))

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    blocks.__getitem__(len(blocks)-1).sidestep(Block.LEFT)
                elif event.key == pygame.K_RIGHT:
                    blocks.__getitem__(len(blocks)-1).sidestep(Block.RIGHT)
                elif event.key == pygame.K_SPACE:
                    blocks.__getitem__(len(blocks)-1).turn()
        if not (blocks.__getitem__(len(blocks)-1).bottom() and blocks.__getitem__(len(blocks)-1).collide(blocks)):
            blocks.__getitem__(len(blocks)-1).move()
        else:
            blocks.append(Block(random.randint(0, 5)))
        draw_window(win, blocks)

    pygame.quit()


if __name__ == '__main__':
    main()