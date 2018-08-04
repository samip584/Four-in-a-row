from os import system
import random
import time
import Arrow


board = []		#matrix denoting the board of the 4 in a row game
player = ['*', 'o']		#players symbols
turn = 0		#defining turn and count as global
count = 0
insert_row = [0,0,0,0,0,0,0]		#defining the row which denotes the top bar where player can moove its symbol and select where to insert the symbol

def main_screan():
	index_count = 0		#tracks where the index is placed
	indicator_psition = ['->', 0, 0]		#the list which shows where the index is tracked
	#The below loop Displays the main screan
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
			system("clear")
			print("\tFOUR IN A ROW\n\n")
			display_board()
			print(player[(turn + 1) % 2],"player WON")
			Arrow.get()
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
			system("clear")
			print("\tFOUR IN A ROW\n\n")
			display_board()
			print(player[(turn + 1) % 2],"player WON")
			Arrow.get()
			return



def computer_enters():		#computer generates places to enter
	global turn
	global count
	title()
	display_board()
	time.sleep(0.25) 	# delays for 0.25 seconds
	title()
	while True:
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
		break	
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
	insert_row = [0,0,0,0,0,0,0]
	insert_row[count] = player[turn]		#to indicate whoose turn it is the players is shown above the board and indicates where the player is to insert 
	display_insert_row(insert_row)
	display_board()
	while True:		#This loop changes the index in the insert row according to right and left arrow pressed and tries to insert with down key 
		shift_dir = Arrow.get()
		if shift_dir == 'right':
			insert_row[(count + 1) % 7], insert_row[count] = insert_row[count], insert_row[(count + 1) % 7]
			count = (count + 1) % 7
			break
		elif shift_dir == 'left':
			temp_count = (count - 1)
			if(temp_count < 0): temp_count = 6
			insert_row[count], insert_row[temp_count] = insert_row[temp_count], insert_row[count]
			count = temp_count
			break
		elif shift_dir == 'down':
			change = board_enhancement_and_return_change_decision(count, player[turn])
			if(change == 'Yes'):
				turn = (turn + 1) % 2
			break

		

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

def display_board():		##displays the board
    print("-"*29)
    for index, row in enumerate(board):
        print(("|" + " {} |"*7).format(*[x if x != 0 else " " for x in row]))
        if index == 6:
            print("-"*29) 
        else:
        	print("|" + "---+"*6 + "---|")

def display_insert_row(insert_row):			#prints the row at which shows where the current symbol might be inserted
    print((" " + " {}  "*7).format(*[x if x != 0 else " " for x in insert_row]))


if __name__ == "__main__":
	main_screan()