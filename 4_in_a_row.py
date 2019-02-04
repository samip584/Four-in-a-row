from os import system
import random
import time
import pygame
import Arrow
import sys

board = []		#matrix denoting the board of the 4 in a row game
player = ['*', 'o']		#players symbols
turn = 0		#defining turn and count as global
count = 0

pygame.init()
square_size = 50

largeText = pygame.font.Font('freesansbold.ttf',45)
width = square_size * 7
height = square_size * 9
play_ring_radious = int((square_size / 2) - 1)
size = (width, height)
screen = pygame.display.init()

def main_screan():
	global screen
	index_count = 0		#tracks where the index is placed
	indicator_psition = ['->', 0, 0]		#the list which shows where the index is tracked
	#The below loop Displays the main screen
	while True:
		system("clear")
		print("\t!!!! Four in a row !!!!\n\n")
		game_mode = ['Single Player', '2 Players', 'Exit']		#different gamemodes player can select
		for indicator,mode in zip(indicator_psition,game_mode):		#options display with index
			print(("\t" +" {}  "+mode).format(*[indicator if indicator != 0 else "  "]))
		#The below scripts changes the index according to up and down arrow pressed and selects usning the right arrow
		select_dir = Arrow.get()
		if select_dir == 'down':
				indicator_psition[(index_count + 1) % 3], indicator_psition[index_count] = indicator_psition[index_count], indicator_psition[(index_count + 1) % 3]
				index_count = (index_count + 1) % 3
		elif select_dir == 'up':
			temp_count = (index_count - 1)
			if(temp_count < 0): temp_count = 2
			indicator_psition[temp_count], indicator_psition[index_count] = indicator_psition[index_count], indicator_psition[temp_count]
			index_count = temp_count
		elif select_dir == 'right':
			screen = pygame.display.set_mode(size)
			if index_count == 0:
				single_player()
			elif index_count == 1:
				multi_player()
			elif index_count == 2:
				return 


def multi_player():		#multiplayer game play
	global turn
	global count
	board.clear()
	for i in range(7):		#this loop makes a 7*7 matrix with every element zero
		temp = []
		for j in range (7):
			temp.append(0)
		board.append(temp)
	turn = random.randint(0,1)		#random number to decide which player is first
	count = 0
	while(1): 
		player_enters()
		if check_victory() == 'WON':
			#below codes show which player won
			display_board()
			display_victory()
			return

		
def single_player():
	global turn
	global count
	board.clear()
	for i in range(7):		#this loop makes a 7*7 matrix with every element zero
		temp = []
		for j in range (7):
			temp.append(0)
		board.append(temp)
	turn = random.randint(0,1)		#random number to decide which player is first
	count = 0
	while True:  
		if(player[turn] == 'o'):
			computer_enters()
		else:
			player_enters()
		if check_victory() == 'WON':
			#below codes show which player won
			display_board()
			display_victory()
			return



def computer_enters():		#computer generates places to enter
	global turn
	global count
	title()
	display_board()
	time.sleep(0.25) 	# delays for 0.25 seconds
	title()
	spot = victory_spot()		#checks for any place where the computer can win 
	if(spot == 7):
		spot = dangerous_spot()		#checks for any place where the computer may loose
	if(spot == 7):
		spot = predict_for_next_victory()		#checks for any place where the computer can win in next turn
	if(spot == 7):
		spot = pick_random_spot()		#checks for any random place where the computer can wont loose in the players turn
	change = board_enhancement_and_return_change_decision(spot, player[turn]) 		#modifies the board
	if(change == 'Yes'):
		turn = (turn + 1) % 2
	display_board()


def dangerous_spot():		#checks for any place where the computer may loose
	for column in range(7):
		change = board_enhancement_and_return_change_decision(column, player[(turn + 1) % 2])
		if(change == 'Yes'):
			if check_victory() == 'WON':
				remove_what_was_added_for_testing(column)
				return column
			remove_what_was_added_for_testing(column)
	return 7

def victory_spot():		#checks for any place where the computer can win 
	for column in range(7):
		change = board_enhancement_and_return_change_decision(column, player[turn])
		if(change == 'Yes'):
			if check_victory() == 'WON':
				remove_what_was_added_for_testing(column)
				return column
			remove_what_was_added_for_testing(column)
	return 7

def predict_for_next_victory():		#checks for any place where the computer can win in next turn
	for column in range(7):
		change = board_enhancement_and_return_change_decision(column, player[turn])
		if(change == 'Yes'):
			if victory_spot() != 7 and dangerous_spot() == 7:
				remove_what_was_added_for_testing(column)
				return column
			remove_what_was_added_for_testing(column)
	return 7

def pick_random_spot():	
	spot = random.randint(0,6)
	for i in range(7):
		change = board_enhancement_and_return_change_decision(spot, player[turn])
		if(change == 'Yes'):
			if dangerous_spot() == 7:
				remove_what_was_added_for_testing(spot)
				return spot
			remove_what_was_added_for_testing(spot)
		spot = (spot + 1) % 7
	return (spot)


def remove_what_was_added_for_testing(column):		#removes the symbol which was added to the board during the testing
	for row in range(7):
		if board[row][column] != 0:
			board[row][column] = 0	
			return



def player_enters():	#humans enter the place to insurt
	global turn
	global count
	title()
	display_board()
	while True:		#This loop changes the index in the insert row according to right and left arrow pressed and tries to insert with down key 
		for event in pygame.event.get():
			if event.type ==pygame.QUIT:
				sys.exit()
			key = pygame.key.get_pressed()
			if key[pygame.K_RIGHT]:
				count = (count + 1) % 7
				break
			elif key[pygame.K_LEFT]:
				temp_count = (count - 1)
				if(temp_count < 0): temp_count = 6
				count = temp_count
				break
			elif key[pygame.K_DOWN]:
				change = board_enhancement_and_return_change_decision(count, player[turn])
				if(change == 'Yes'):
					turn = (turn + 1) % 2
					return
				break
			display_insert_row(count)


		

def board_enhancement_and_return_change_decision(count, player):		#attempts to make changes in board and returns if the board has changed or not 
	row = 6
	while(row >= 0):
		if board[row][count] == 0:
			board[row][count] = player
			return 'Yes'
		else:
			row -= 1
	return 'No'

def check_victory():		#checks if the current player won
	for i in range(7):
		for j in range(4):
			if board[i][j] == board[i][j+1] and board[i][j] == board[i][j+2] and board[i][j] == board[i][j+3] and board[i][j] != 0:
				return("WON")
			if board[j][i] == board[j+1][i] and board[j][i] == board[j+2][i] and board[j][i] == board[j+3][i] and board[j][i] != 0:
				return("WON")
	for i in range(4):
		for j in range(4):
			if board[i][j] == board[i+1][j+1] and board[i][j] == board[i+2][j+2] and board[i][j] == board[i+3][j+3] and board[i][j] != 0:
				return("WON")
			if board[6-i][j] == board[5-i][j+1] and board[6-i][j] == board[4-i][j+2] and board[6-i][j] == board[3-i][j+3] and board[6-i][j] != 0:
				return("WON")

def title():		#displays the title of the game
	system("clear")
	print("\tFOUR IN A ROW\n")
	print("      Arrow keys to play\n\n")

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()


def display_board():		##displays the board
	TextSurf, TextRect = text_objects("FOUR IN A ROW", largeText)
	TextRect.center = ((width/2),int(30))
	screen.blit(TextSurf, TextRect)
	for column in range(7):
		for row in range(7):
			pygame.draw.rect(screen,(50, 0, 200), (column* square_size, row*square_size + 2 * square_size, square_size, square_size))
			pygame.draw.circle(screen,(0, 0, 0), (int(column* square_size + (square_size / 2)), int(row*square_size + (5 * square_size / 2))), play_ring_radious)
			if(board[row][column] == '*'):
				pygame.draw.circle(screen,(200, 200, 0), (int(column* square_size + (square_size / 2)), int(row*square_size + (5 * square_size / 2))), play_ring_radious)
			elif(board[row][column] == 'o'):
				pygame.draw.circle(screen,(200, 0, 0), (int(column* square_size + (square_size / 2)), int(row*square_size + (5 * square_size / 2))), play_ring_radious)
	pygame.display.update()

def display_insert_row(count):			#prints the row at which shows where the current symbol might be inserted
	pygame.draw.rect(screen,(0, 0, 0), (0, square_size, square_size * 7, square_size))
	pygame.draw.circle(screen,(200, 200, 0) if player[turn] == "*"  else (200, 0, 0), (int(count* square_size + (square_size / 2)), int(1*square_size + (square_size / 2))), play_ring_radious)
	pygame.display.update()

def display_victory():
	screen.fill((0, 0, 0))
	TextSurf, TextRect = text_objects("FOUR IN A ROW", largeText)
	TextRect.center = ((width/2),int(30))
	screen.blit(TextSurf, TextRect)
	pygame.draw.circle(screen,(200, 200, 0) if player[(turn + 1) % 2 ] == "*"  else (200, 0, 0), (int(width / 2 - 120), int(height/2 - 5)), play_ring_radious)
	TextSurf, TextRect = text_objects(" WON", largeText)
	TextRect.center = ((width/2),(height/2))
	screen.blit(TextSurf, TextRect)

	pygame.display.update()

	time.sleep(2)


if __name__ == "__main__":
	main_screan()