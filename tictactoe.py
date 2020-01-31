import pygame

pygame.display.set_caption("TicTacToe")

TILE_WIDTH = 200
OFFSET = 20
STROKE = 1

class Board:
	EMPTY = 0
	P1 = True
	P1_x = 1
	P2 = False
	P2_x = 2


	def __init__(self):
		self.field = [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY]
		self.turn = Board.P1
		self.winner = self.EMPTY

	def move(self, i):
		if self.field[i-1] == self.EMPTY:
			if self.turn == Board.P1:
				self.field[i-1] = Board.P1_x
			else:
				self.field[i-1] = Board.P2_x
			self.turn = not self.turn

	def checkGameOver(self):
		a, b, c, d, e, f, g, h, i = self.field[0], self.field[1], self.field[2], self.field[3], self.field[4], self.field[5], self.field[6], self.field[7], self.field[8] 
		if  ( Board.P1_x==a and a==b and b==c ) or \
			( Board.P1_x==d and d==e and e==f ) or \
			( Board.P1_x==g and g==h and h==i ) or \
			( Board.P1_x==a and a==d and d==g ) or \
			( Board.P1_x==b and b==e and b==h ) or \
			( Board.P1_x==c and c==f and b==i ) or \
			( Board.P1_x==a and a==e and e==i ) or \
			( Board.P1_x==c and c==e and e==g ):
				self.winner = Board.P1_x
		elif ( Board.P2_x==a and a==b and b==c ) or \
			( Board.P2_x==d and d==e and e==f ) or \
			( Board.P2_x==g and g==h and h==i ) or \
			( Board.P2_x==a and a==d and d==g ) or \
			( Board.P2_x==b and b==e and b==h ) or \
			( Board.P2_x==c and c==f and b==i ) or \
			( Board.P2_x==a and a==e and e==i ) or \
			( Board.P2_x==c and c==e and e==g ):
				self.winner = Board.P2_x

def draw_window(win, board):
	for x in range(3):
		for y in range(3):
			pygame.draw.rect(win, (255, 255, 255), pygame.Rect(x*(STROKE+TILE_WIDTH)+OFFSET, y*(STROKE+TILE_WIDTH)+OFFSET, TILE_WIDTH, TILE_WIDTH))

	for i, t in enumerate(board.field):
		col = i%3
		row = i//3
		if t == Board.P1_x:
			pygame.draw.rect(win, (255, 0, 0), pygame.Rect(col*(STROKE+TILE_WIDTH)+OFFSET, row*(STROKE+TILE_WIDTH)+OFFSET, TILE_WIDTH, TILE_WIDTH))
		elif t == Board.P2_x:
			pygame.draw.rect(win, (255, 255, 0), pygame.Rect(col*(STROKE+TILE_WIDTH)+OFFSET, row*(STROKE+TILE_WIDTH)+OFFSET, TILE_WIDTH, TILE_WIDTH))

	if board.winner == Board.P1_x:
		pygame.draw.circle(win, (255, 255, 255), ((STROKE+TILE_WIDTH)+OFFSET+TILE_WIDTH//2, (STROKE+TILE_WIDTH)+OFFSET+TILE_WIDTH//2), 35)
		pygame.draw.circle(win, (255, 0, 0), ((STROKE+TILE_WIDTH)+OFFSET+TILE_WIDTH//2, (STROKE+TILE_WIDTH)+OFFSET+TILE_WIDTH//2), 30)
	elif board.winner == Board.P2_x:
		pygame.draw.circle(win, (255, 255, 255), ((STROKE+TILE_WIDTH)+OFFSET+TILE_WIDTH//2, (STROKE+TILE_WIDTH)+OFFSET+TILE_WIDTH//2), 35)
		pygame.draw.circle(win, (255, 255, 0), ((STROKE+TILE_WIDTH)+OFFSET+TILE_WIDTH//2, (STROKE+TILE_WIDTH)+OFFSET+TILE_WIDTH//2), 30)
	
	pygame.display.update()
	


def main():
	win = pygame.display.set_mode((700, 700))
	board = Board()

	run = True
	while(run):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					board.move(1)
				elif event.key == pygame.K_2:
					board.move(2)
				elif event.key == pygame.K_3:
					board.move(3)
				elif event.key == pygame.K_4:
					board.move(4)
				elif event.key == pygame.K_5:
					board.move(5)
				elif event.key == pygame.K_6:
					board.move(6)
				elif event.key == pygame.K_7:
					board.move(7)
				elif event.key == pygame.K_8:
					board.move(8)
				elif event.key == pygame.K_9:
					board.move(9)
		board.checkGameOver()
		draw_window(win, board)


if __name__ == '__main__':
	main()