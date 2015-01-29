'''
Created on Apr 17, 2013

@author: Harry
'''
#Harry Pham 79422112 and Kevin Nguyen 53581426
import connectfour, ICFSP32


MENU="""
Menu --- Choose One
 n: New Game
 q: Quits Connect Four Program
"""

"""CONNECT FOUR"""
GAME_MENU="""
Choose a Move
 d: Drop a Piece
 p: Pop a Piece Out
"""
def handle_game_menu(current_game:connectfour.ConnectFourGameState)->str:
    """Displays Startup Menu, accepts and processes commands
    """
    while True:
        response=input(GAME_MENU).strip().lower()
        if response=='d':
            while True:
                try:
                    column_number=input('Enter a Column to drop piece or enter nothing to return to previous menu: ').strip()
                    if column_number=='':
                        break
                    else:
                        column_number=int(column_number)-1
                    if column_number < 0:
                        raise connectfour.InvalidConnectFourMoveError()
                    else:
                        try:
                            if connectfour._find_bottom_empty_row_in_column(current_game.board,column_number)!= -1:
                                column_number+=1
                                return 'DROP {}'.format(column_number)
                            else:
                                raise connectfour.InvalidConnectFourMoveError()
                        except IndexError:
                            raise connectfour.InvalidConnectFourMoveError()
                except connectfour.InvalidConnectFourMoveError:
                    print("Cannot make this move. Please input a different move.")
                    break
                except ValueError:
                    print("Invalid Command. Please enter a different command.")
        elif response=='p':
            while True:
                try:
                    column_number=input('Enter a Column to pop piece out or enter nothing to return to previous menu: ').strip()
                    if column_number=='':
                        break
                    else:
                        column_number=int(column_number)-1
                    if column_number < 0:
                        raise connectfour.InvalidConnectFourMoveError()
                    else:
                        try:
                            if current_game.turn == current_game.board[int(column_number)][connectfour.BOARD_ROWS - 1]:
                                column_number+=1
                                return 'POP {}'.format(column_number)
                            else:
                                raise connectfour.InvalidConnectFourMoveError()
                        except IndexError:
                            raise connectfour.InvalidConnectFourMoveError()
                except connectfour.InvalidConnectFourMoveError:
                    print("Cannot make this move. Please input a different move.")
                    break
                except ValueError:
                    print("Invalid Command. Please enter a different command.")
        else:
            invalid_command(response)

def invalid_command(response:str)->None:
    """ Print message for invalid menu command.
    """
    print("Sorry; '" + response + "' isn't a valid command.  Please enter an option from the menu.")





def _new_game()->connectfour.ConnectFourGameState:
    '''Creates a new game'''
    game_state=connectfour.new_game_state()
    return game_state

def _current_game(current_game:connectfour.ConnectFourGameState,internet=False, connection=None)->None:
    '''Makes the moves on the game board'''
    _print_board(current_game)
    if internet==False:
        while connectfour.winning_player(current_game)==connectfour.NONE:
            split_command=handle_game_menu(current_game).split()
            if split_command[0]=='DROP':
                current_game=connectfour.drop_piece(current_game, int(split_command[1])-1)
            elif split_command[0]=='POP':
                current_game=connectfour.pop_piece(current_game, int(split_command[1])-1)
            _print_board(current_game)
        if connectfour.winning_player(current_game)=='R':
            print('Game Over. Red Player has won.')
        elif connectfour.winning_player(current_game)=='Y':
            print('Game Over. Yellow Player has won.')
    elif internet==True:
        status='OKAY'
        while status!='WINNER_RED' or 'WINNER_YELLOW':
            current_game, status=_send_game_move(connection, current_game)
            _print_board(current_game)
            if connectfour.winning_player(current_game) == 'R':
                status = 'WINNER_RED'
                break
            elif connectfour.winning_player(current_game) == 'Y':
                status = 'WINNER_YELLOW'
                break
            print('\n')
            print("Recieving AI's move...")
            current_game=_recieve_game_move(connection, current_game)
            print('Move recieved.')
            input("Please enter a key to see the AI's move")
            _print_board(current_game)
            if connectfour.winning_player(current_game) == 'R':
                status = 'WINNER_RED'
                break
            elif connectfour.winning_player(current_game) == 'Y':
                status = 'WINNER_YELLOW'
                break
        if status=='WINNER_RED':
            print('Game Over. Red Player has won.')
        elif status=='WINNER_YELLOW':
            print('Game Over. Yellow Player has won.')
        else:
            print(status)
            print('Error. Ending Game.')

def _print_board(game_state:connectfour.ConnectFourGameState)->None:
    '''Prints current game board and turn'''
    for col_number in range(connectfour.BOARD_COLUMNS):
        print('',col_number+1, end=' ')
    result=[]
    print('')
    for row in range(connectfour.BOARD_ROWS):
        line=''
        for column in range(connectfour.BOARD_COLUMNS):
            if game_state.board[column][row]==' ':
                line+=' . '
            else:
                line+=' '+game_state.board[column][row]+' '
        result.append(line)
    for row in result:
        print(row)
    if game_state.turn=='R':
        print("Red's Turn")
    else:
        print("Yellow's Turn")

def _send_game_move(connection:ICFSP32._I32CFSPConnection, current_game:connectfour.ConnectFourGameState)->connectfour.ConnectFourGameState:
    '''Sends Game Move'''
    status = 'INVALID'
    while status == 'INVALID':
        message=ICFSP32._recieve_message(connection)
        send_command=handle_game_menu(current_game)
        split_command=send_command.split()
        ICFSP32._send_message(connection, send_command)
        recieve_message=ICFSP32._recieve_message(connection)
        if recieve_message=='OKAY' or 'WINNER_RED' or 'WINNER_YELLOW':
            if split_command[0]=='DROP':
                current_game=connectfour.drop_piece(current_game, int(split_command[1])-1)
                return current_game, recieve_message
            elif split_command[0]=='POP':
                current_game=connectfour.pop_piece(current_game, int(split_command[1])-1)
                return current_game, recieve_message

def _recieve_game_move(connection:ICFSP32._I32CFSPConnection, current_game:connectfour.ConnectFourGameState)->connectfour.ConnectFourGameState:
    '''Recieves Game Move'''
    recieve_command=ICFSP32._recieve_message(connection)
    split_recieve_command=recieve_command.split()
    if split_recieve_command[0]=='DROP':
        current_game=connectfour.drop_piece(current_game, int(split_recieve_command[1])-1)
        return current_game
    elif split_recieve_command[0]=='POP':
        current_game=connectfour.pop_piece(current_game, int(split_recieve_command[1])-1)
        return current_game
