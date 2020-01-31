import pygame
pygame.display.set_caption("Pong")
pygame.font.init()

face = """
   ___      ___   
  |   |    |   |
-- (o) ---- (o) --  
         />       
  <________ ___>  
           U     """

HEIGHT = 600
WIDTH = 1200
FPS = 200
BAR_HEIGHT = 100
BAR_WIDTH = 10
BALL_RADIUS = 20
FONT = pygame.font.SysFont("arial", 20)

class Ball:
	def __init__(self):
		self.x = WIDTH/2
		self.y = HEIGHT/2
		self.v_x = 1
		self.v_y = 3

	def draw(self, win):
		pygame.draw.circle(win, (255, 255, 0), (round(self.x), round(self.y)), BALL_RADIUS)

	def move(self):
		self.x += self.v_x
		self.y -= self.v_y

	def out(self, bar_left, bar_right):
		# if self.x+BALL_RADIUS >= bar_right.x-BAR_WIDTH and self.y >= bar_right.y+BAR_HEIGHT and self.y <= bar_right.y-BAR_HEIGHT:
		# 	return 2
		# elif self.x-BALL_RADIUS <= bar_left.x+BAR_WIDTH and self.y >= bar_left.y+BAR_HEIGHT and self.y <= bar_left.y-BAR_HEIGHT:
		# 	return 1
		if self.x >= bar_right.x:
			return 2
		if self.x <= bar_left.x:
			return 1
		return 0

	def top(self):
		return self.y <= 0+round(BALL_RADIUS)

	def bottom(self):
		return self.y >= HEIGHT-round(BALL_RADIUS)

	def left(self, bar):
		return self.x-BALL_RADIUS <= bar.x+BAR_WIDTH and self.y <= bar.y+BAR_HEIGHT and self.y >= bar.y-BAR_HEIGHT

	def right(self, bar):
		return self.x+BALL_RADIUS >= bar.x-BAR_WIDTH and self.y <= bar.y+BAR_HEIGHT and self.y >= bar.y-BAR_HEIGHT

	def bounce_border(self):
		self.v_y *= -1

	def bounce_bar(self):
		self.v_x *= -1

	def reset(self):
		self.x = WIDTH/2
		self.y = HEIGHT/2
		self.v_x = 1
		self.v_y = 3

class Bar:
	def __init__(self, right):
		self.y = HEIGHT/2
		if right == True:
			self.x = WIDTH-50
			self.isRight = True
		elif right == False:
			self.x = 50
			self.isRight = False

	def draw(self, win):
		rect = pygame.Rect(self.x-BAR_WIDTH/2, self.y-BAR_HEIGHT/2, BAR_WIDTH, BAR_HEIGHT)
		pygame.draw.rect(win, (255, 0, 0), rect)

	def up(self):
		self.y -= 15

	def down(self):
		self.y += 15

def draw_window(win, bar_right, bar_left, ball, score_left, score_right):
	win.fill((0, 0, 0))
	bar_right.draw(win)
	bar_left.draw(win)
	ball.draw(win)
	score_left = FONT.render(str(score_left), 1, (255, 255, 255))
	win.blit(score_left, (20, 20))
	score_right = FONT.render(str(score_right), 1, (255, 255, 255))
	win.blit(score_right, (WIDTH-score_right.get_width()-20, 20))
	pygame.display.update()

def main():
	clock = pygame.time.Clock()
	win = pygame.display.set_mode((WIDTH, HEIGHT))
	bar_right = Bar(True)
	bar_left = Bar(False)
	ball = Ball()
	score_left = 0
	score_right = 0

	run = True
	while(run):
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					bar_right.up()
				elif event.key == pygame.K_DOWN:
					bar_right.down()
				elif event.key == pygame.K_w:
					bar_left.up()
				elif event.key == pygame.K_s:
					bar_left.down()
		ball.move()
		if ball.out(bar_left, bar_right) == 1:
			score_right += 1
			ball.reset()
		elif ball.out(bar_left, bar_right) == 2:
			score_left += 1
			ball.reset()

		if ball.top() or ball.bottom():
			ball.bounce_border()
		elif ball.left(bar_left) or ball.right(bar_right):
			ball.bounce_bar()
		draw_window(win, bar_right, bar_left, ball, score_left, score_right)

	pygame.quit()

if __name__ == '__main__':
	print(face)
	main()