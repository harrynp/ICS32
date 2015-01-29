'''
Created on May 18, 2013

@author: Harry
'''
#Harry Pham 79422112

#User Input
import random
NONE = ' '
BLACK = 'B'
WHITE = 'W'
VALID = '*'
MODE = 'MOST'
TIE = 'T'
HELP = True
STARTING_PLAYER=BLACK
REVERSE = 'False'
BOARD_COLUMNS = 8
BOARD_ROWS = 8


class InvalidOthelloMoveError(Exception):
    '''Raised whenenver an invalid move is made'''
    pass

class NoMoveError(Exception):
    '''Raised whenever player has no valid moves'''
    pass

#RULES

def _is_valid_column_number(column_number:int)->bool:
    '''Returns True if the given column number is valid; returns False
    otherwise'''
    return 0 <= column_number < BOARD_COLUMNS

def _require_valid_column_number(column_number:int)->Exception:
    '''Raises a ValueError if its parameter is not a valid column number'''
    if type(column_number) != int or not _is_valid_column_number(column_number):
        raise ValueError('column_number must be int between 0 and {}'.format(BOARD_COLUMNS - 1))


def _is_valid_row_number(row_number:int)->bool:
    '''Returns True if the given row number is valid; returns False
    otherwise'''
    return 0 <= row_number < BOARD_ROWS

def _require_valid_row_number(row_number:int)->Exception:
    '''Raises a ValueError if its parameter is not a valid column number'''
    if type(row_number) != int or not _is_valid_column_number(row_number):
        raise ValueError('row_number must be int between 0 and {}'.format(BOARD_ROWS - 1))

def _new_game_board(reverse:str)->list:
    '''Creates a new game board.  Initially, a game board has the size
    BOARD_COLUMNS x BOARD_ROWS and is comprised only of strings with the
    value NONE and the 4 middle spaces with the strings BLACK and WHITE'''
    board = []
    if reverse=='False':
        for col in range(BOARD_COLUMNS):
            board.append([])
            for row in range(BOARD_ROWS):
                board[-1].append(NONE)
        board[BOARD_COLUMNS//2][BOARD_ROWS//2]=WHITE
        board[(BOARD_COLUMNS//2)-1][(BOARD_ROWS//2)-1]=WHITE
        board[(BOARD_COLUMNS//2)-1][BOARD_ROWS//2]=BLACK
        board[BOARD_COLUMNS//2][(BOARD_ROWS//2)-1]=BLACK
    elif reverse=='True':
        for col in range(BOARD_COLUMNS):
            board.append([])
            for row in range(BOARD_ROWS):
                board[-1].append(NONE)
        board[BOARD_COLUMNS//2][BOARD_ROWS//2]=BLACK
        board[(BOARD_COLUMNS//2)-1][(BOARD_ROWS//2)-1]=BLACK
        board[(BOARD_COLUMNS//2)-1][BOARD_ROWS//2]=WHITE
        board[BOARD_COLUMNS//2][(BOARD_ROWS//2)-1]=WHITE
    return board

def _is_valid_move(board:list, turn:str, column:int, row:int)->list:
    """Checks if the move is valid on the board and turn given"""
    _require_valid_column_number(column)
    _require_valid_row_number(row)
    flip=[]
    if board[column][row] != NONE:
        return None
    board[column][row]=turn
    if turn == BLACK:
        opposite=WHITE
    elif turn == WHITE:
        opposite=BLACK
    for coldir in [-1,0,1]:
        for rowdir in [-1,0,1]:
            x,y=column,row
            x+=coldir
            y+=rowdir
            if _is_valid_column_number(x) and _is_valid_row_number(y) and board[x][y]==opposite:
                x+=coldir
                y+=rowdir
                if not _is_valid_column_number(x) and not _is_valid_row_number(y):
                    continue
                try:
                    while board[x][y]==opposite:
                        x+=coldir
                        y+=rowdir
                        if not _is_valid_column_number(x) and not _is_valid_row_number(y):
                            break
                except:
                    pass
                if not _is_valid_column_number(x) and not _is_valid_row_number(y):
                    continue
                try:
                    if board[x][y]==turn:
                        while True:
                            x-=coldir
                            y-=rowdir
                            if x==column and y==row:
                                break
                            flip.append([x,y])
                except:
                    pass
    board[column][row]=NONE
    if len(flip)==0:
        return None
    return flip

def valid_moves(board:list, turn:str)->list:
    """Returns a list of valid moves"""
    valid=[]
    for column in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS):
            if _is_valid_move(board,turn,column,row)!=None:
                valid.append([column,row])
    return valid

def valid_moves_board(board:list,turn:str)->list:
    """Returns a board with valid moves marked with '*'"""
    validboard=boardcopy(board)
    for col,row in valid_moves(validboard,turn):
        validboard[col][row]=VALID
    return validboard

def boardcopy(board:list)->list:
    """Copies the board given"""
    copy=_new_game_board(REVERSE)
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS):
            copy[col][row]=board[col][row]
    return copy

def full_board(board:list)->int:
    """Returns a interger of how many empty spaces remain on the board"""
    empty_space=0
    for col in range(BOARD_COLUMNS):
        for row in range(BOARD_ROWS):
            if board[col][row]==NONE:
                empty_space+=1
    return empty_space

def ai(board:list, turn:str)->(int,int):
    """AI for playing a game, chooses a random move from all valid moves available"""
    moves=valid_moves(board, turn)
    if len(moves)>0:
        random.shuffle(moves)
        move=moves[0]
        column,row=move
        return column, row
    else:
        return

class game():
    def __init__(self,board=_new_game_board(REVERSE),turn=STARTING_PLAYER):
        self._board=board
        self._turn=turn
        self._skip=0
    def new_game(self)->None:
        """Creates a new game board"""
        self._board=_new_game_board(REVERSE)
    def board(self)->None:
        return self._board
    def turn(self)->None:
        return self._turn
    def skip(self)->None:
        return self._skip
    def change_turn(self)->None:
        """Changes the current turn"""
        if self._turn==BLACK:
            self._turn=WHITE
        elif self._turn==WHITE:
            self._turn=BLACK
    def no_moves(self)->None:
        """Keeps track of how many skips have taken place"""
        self._skip+=1
    def skip_reset(self)->None:
        """Resets the skip counter"""
        self._skip=0
    def drop_piece(self, column, row)->None:
        """Makes the moves on the board"""
        self._board[column][row]=self._turn
    def score(self)->(int,int):
        """Returns current scores"""
        black_score=0
        white_score=0
        for col in range(BOARD_COLUMNS):
            for row in range(BOARD_ROWS):
                if self._board[col][row]==BLACK:
                    black_score+=1
                elif self._board[col][row]==WHITE:
                    white_score+=1
        return black_score, white_score

def winning_player(game:game, mode:str)->str:
    """Returns the current winner of the game if game is over, else returns an
    empty string"""
    winner=NONE
    if mode=='LEAST':
        for col in range(BOARD_COLUMNS):
            for row in range(BOARD_ROWS):
                if full_board(game.board())==0 or game.skip()==2:
                    black_score, white_score=game.score()
                    if black_score>white_score:
                        winner=WHITE
                    elif black_score<white_score:
                        winner=BLACK
                    elif black_score==white_score:
                        winner=TIE
    if mode=='MOST':
        for col in range(BOARD_COLUMNS):
            for row in range(BOARD_ROWS):
                if full_board(game.board())==0 or game.skip()==2:
                    black_score, white_score=game.score()
                    if black_score>white_score:
                        winner=BLACK
                    elif black_score<white_score:
                        winner=WHITE
                    elif black_score==white_score:
                        winner=TIE
    return winner
