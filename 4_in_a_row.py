from os import system
import Arrow

board = [
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0]
		]

def main():
	system("clear")
	play()

def play():
	player = ['*', '#']
	turn = 0
	insert_row = [player[turn],0,0,0,0,0,0]
	count = 0
	while(1):
		print("\tFOUR IN A ROW\n\n")
		display_insert_row(insert_row)
		display_board()
		while(1):
			shift_dir = Arrow.get()
			if shift_dir == 'right' and count != 6:
				insert_row[count + 1], insert_row[count] = insert_row[count], insert_row[count + 1]
				count += 1
				break
			elif shift_dir == 'left' and count != 0:
				insert_row[count], insert_row[count - 1] = insert_row[count - 1], insert_row[count]
				count -= 1
				break
			elif shift_dir == 'down':
				change = board_enhancement_and_return_change_decision(count, player[turn])
				if(change == 'Yes'):
					if check_victory() == 'WON':
						system("clear")
						print("\tFOUR IN A ROW\n\n")
						display_board()
						print(player[turn],"player WON")
						return
					turn = (turn + 1) % 2
					count = 0
					insert_row = [player[turn],0,0,0,0,0,0]
				break
		system("clear")

def board_enhancement_and_return_change_decision(count, player):
	row = 6
	while(row >= 0):
		if board[row][count] == 0:
			board[row][count] = player
			return 'Yes'
		else:
			row -= 1
	return 'No'

def check_victory():
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

def display_board():
    print("-"*29)
    for index, row in enumerate(board):
        print(("|" + " {} |"*7).format(*[x if x != 0 else " " for x in row]))
        if index == 6:
            print("-"*29) 
        else:
        	print("|" + "---+"*6 + "---|")

def display_insert_row(insert_row):
    print((" " + " {}  "*7).format(*[x if x != 0 else " " for x in insert_row]))


if __name__ == "__main__":
	main()