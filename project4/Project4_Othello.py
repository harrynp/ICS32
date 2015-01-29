'''
Created on May 18, 2013

@author: Harry
'''
#Harry Pham 79422112
#Going to fix the return to previous player's move in next project
import othello

#Menus

START_MENU="""
Othello Main Menu --- Choose one
 n: New Game
 a: Play against AI(Note: Player always plays as black and AI mode is not completely finished.)
 s: Settings to change dimensions, starting player, and winning conditions of the game
 q: Quits Othello Program
"""

SETTINGS_MENU="""
Settings Menu --- Choose one
 d: Change dimensions of the board
 s: Change starting player
 w: Change winning conditions
 o: Change board starting order
 h: Turn valid move indicator(*) on or off
 q: Return to main menu
"""

ENDGAME_MENU="""
End Game Menu --- Choose One
(To play online or change board dimensions, return to the main menu)
 n: New Game
 m: Returns to Main Menu
 q: Quits Connect Four Program
"""

def start()->None:
    """User interface for startup"""
    while True:
        response=input(START_MENU).strip().lower()
        if response=='n':
            _current_game(othello.HELP,False)
            return end_game(False)
        elif response=='a':
            _current_game(othello.HELP,True)
            return end_game(True)
        elif response=='s':
            settings()
        elif response=='q':
            return
        else:
            invalid_command(response)

def settings()->None:
    """User interface for settings"""
    while True:
        response=input(SETTINGS_MENU).strip().lower()
        if response=='d':
            column_number()
            row_number()
        elif response=='s':
            starting_player()
        elif response=='w':
            winning_conditions()
        elif response=='o':
            reverse()
        elif response=='h':
            helper()
        elif response=='q':
            return
        else:
            invalid_command(response)

def game_menu(board,turn)->list:
    """User interface for game moves"""
    while True:
        while True:
            while True:
                try:
                    column_number=int(input('Enter the column number: ').strip())-1
                    if column_number>othello.BOARD_COLUMNS or column_number<0:
                        raise ValueError
                    break
                except ValueError:
                    print('Invalid Command. Please enter a different command.')
            while True:
                try:
                    row_number=input('Enter the row number or enter nothing to return to column choice: ').strip()
                    if row_number=='':
                        break
                    else:
                        row_number=int(row_number)-1
                        if row_number>othello.BOARD_ROWS or row_number<0:
                            raise ValueError
                        break
                except ValueError:
                    print('Invalid Command. Please enter a different command.')
            break
        try:
            flip=othello._is_valid_move(board, turn, column_number, row_number)
        except (IndexError, ValueError):
            print('Invalid Move. Please try again.')
        if flip!=None:
            flip.append([column_number,row_number])
            return flip
        else:
            print('Invalid Move. Please try again.')

        
def end_game(ai)->None:
    """User interface when game ends"""
    while True:
        response=input(ENDGAME_MENU).strip().lower()
        if response=='n':
            _current_game(othello.HELP,ai)
            return end_game(ai)
        elif response=='m':
            return start()
        elif response=='q':
            return
        else:
            invalid_command(response)

def invalid_command(response)->None:
    """ Print message for invalid menu command.
    """
    print("Sorry; '" + response + "' isn't a valid command.  Please enter an option from the menu.")
    
"""GAME OPTIONS"""

def column_number()->None:
    '''Changes the number of columns in a board or if left blank, defaults to 8 columns'''
    while True:
        try:
            response=input('Enter number of columns or leave blank to play with default number of columns: ').strip()
            if response=='':
                othello.BOARD_COLUMNS=8
                break
            elif float.is_integer(int(response)/2)==False:
                raise ValueError
            elif int(response)<4 or int(response)>16:
                raise ValueError
            else:
                othello.BOARD_COLUMNS=int(response)
                break
        except:
            print("Incorrect input. Please enter a number that is even that is between 4-16.")

def row_number()->None:
    '''Changes the number of rows in a board or if left blank, defaults to 8 rows'''
    while True:
        try:
            response=input('Enter number of rows or leave blank to play with default number of rows: ').strip()
            if response=='':
                othello.BOARD_ROWS=8
                break
            elif float.is_integer(int(response)/2)==False:
                raise ValueError
            elif int(response)<4 or int(response)>16:
                raise ValueError
            else:
                othello.BOARD_ROWS=int(response)
                break
        except:
            print("Incorrect input. Please enter a number that is even that is between 4-16.")
            
def starting_player()->None:
    """Changes the starting player"""
    while True:
        response=input('Enter B to have black as starting player or enter W to have white as starting player: ').strip().lower()
        if response=='b':
            othello.STARTING_PLAYER=othello.BLACK
            break
        elif response=='w':
            othello.STARTING_PLAYER=othello.WHITE
            break
        else:
            invalid_command(response)

def winning_conditions()->None:
    """Changes the winning conditions"""
    while True:
        response=input('Enter L to have winner have least ammount of points or enter M to have winner have most ammount of points: ').strip().lower()
        if response=='l':
            othello.MODE='LEAST'
            break
        elif resonse=='m':
            othello.MODE='MOST'
            break
        else:
            invalid_command(response)

def reverse()->None:
    """Changes the boards starting arrangement"""
    while True:
        response=input('Enter W to have upper left corner start as white or enter B to have it start as Black: ').strip().lower()
        if response=='w':
            othello.REVERSE='False'
            break
        elif response=='b':
            othello.REVERSE='True'
            break
        else:
            invalid_command(response)

def helper()->None:
    """Changes the settings for hints"""
    while True:
        response=input('Enter Y to have help on and N to have help off: ').strip().lower()
        if response=='y':
            othello.HELP=True
        elif response=='n':
            othello.HELP=False
        else:
            invalid_command(response)
            
"""OTHELLO"""

def _current_game(helper, ai)->None:
    """Runs the main game"""
    if ai==True:
        othello.STARTING_PLAYER=othello.BLACK
    current_game=othello.game()
    current_game.new_game()
    if helper==True:
        _print_board(othello.valid_moves_board(current_game.board(),current_game.turn()))
    else:
        _print_board(current_game.board())
    _print_score(current_game)
    _print_turn(current_game.turn())
    while othello.winning_player(current_game, othello.MODE)==othello.NONE:
        if len(othello.valid_moves(current_game.board(),current_game.turn()))==0:
            if othello.full_board(current_game.board())!=0:
                print("{} player has no valid moves and passes.".format(current_game.turn()))
                current_game.no_moves()
                continue
        else:
            if ai==True:
                if current_game.turn()==othello.WHITE:
                    current_game.skip_reset()
                    column,row=othello.ai(current_game.board(),othello.WHITE)
                    flip=othello._is_valid_move(current_game.board(), current_game.turn(), column, row)
                    input("Enter anything to see AI's move")
                else:
                    flip=game_menu(current_game.board(),current_game.turn())
                for column,row in flip:
                    current_game.drop_piece(column,row)
            elif ai==False:
                current_game.skip_reset()
                flip=game_menu(current_game.board(),current_game.turn())
                for column,row in flip:
                    current_game.drop_piece(column,row)
            current_game.change_turn()
        if helper==True:
            _print_board(othello.valid_moves_board(current_game.board(),current_game.turn()))
        else:
            _print_board(current_game.board())
        _print_score(current_game)
        if othello.winning_player(current_game, othello.MODE)==othello.NONE:
            _print_turn(current_game.turn())
    if othello.winning_player(current_game, othello.MODE)==othello.WHITE:
        print('White player has won.')
    elif othello.winning_player(current_game, othello.MODE)==othello.BLACK:
        print('Black player has won.')
    elif othello.winning_player(current_game, othello.MODE)==othello.TIE:
        print('Tie')
    
        
    
def _print_board(board)->None:
    """Prints the board out on the screen"""
    horizontal_line='   +'+'---+'*othello.BOARD_COLUMNS
    vertical_line='   |'+'   |'*othello.BOARD_ROWS
    numbers='  '
    for i in range(othello.BOARD_COLUMNS):
	    numbers+='   '+str(i+1)
    print(numbers)
    print(horizontal_line)
    for y in range(othello.BOARD_ROWS):
        print(vertical_line)
        print('{:2}'.format(y+1), end=' ')
        for x in range(othello.BOARD_COLUMNS):
            print('| {}'.format(board[x][y]), end=' ')
        print('|')
        print(vertical_line)
        print(horizontal_line)

def _print_turn(turn)->None:
    """Prints the current turn"""
    if turn=='B':
        print("Black's Turn")
    else:
        print("White's Turn")

def _print_score(game)->None:
    """Prints the current turn"""
    black_score, white_score = game.score()
    print('Black Score: {}   White Score: {}'.format(black_score,white_score))
if __name__ == '__main__':
    start()
