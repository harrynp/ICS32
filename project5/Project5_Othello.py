'''
Created on May 31, 2013

@author: Harry
'''
#Harry Pham 79422112

import othello, tkinter, coordinate

def settings()->None:
    window=tkinter.Tk()
    window.title('Othello')
    window.resizable(width=False,height=False)
    setting=tkinter.Label(window,text="Settings")
    setting.grid(row=0,column=0)
    d=tkinter.Button(window,text='Change Board Dimensions',command=lambda i=window: dimensions(i))
    d.grid(row=1,column=0)
    s=tkinter.Label(window,text="Starting player:")
    s.grid(row=4,column=0)

    starting_player=tkinter.StringVar()
    starting_player.set(othello.STARTING_PLAYER)
    black=tkinter.Radiobutton(window,text='Black',value=othello.BLACK,
                              variable=starting_player)
    black.grid(row=5,column=0)
    
    white=tkinter.Radiobutton(window,text='White',value=othello.WHITE,
                              variable=starting_player)
    white.grid(row=6,column=0)
    
    a=tkinter.Label(window,text="Board Starting Arrangement")
    a.grid(row=7,column=0)

    reverse=tkinter.StringVar()
    reverse.set(othello.REVERSE)
    reverse_off=tkinter.Radiobutton(window,text='Normal Board Start',value='False',variable=reverse)
    reverse_off.grid(row=8,column=0,columnspan=2)
    reverse_on=tkinter.Radiobutton(window,text='Reversed Board Start',value='True',variable=reverse)
    reverse_on.grid(row=9,column=0,columnspan=2)
    w=tkinter.Label(window,text="Winning Condition")
    w.grid(row=10,column=0)

    winning_condition=tkinter.StringVar()
    winning_condition.set(othello.MODE)
    most=tkinter.Radiobutton(window,text="Winner has most discs",value='MOST',
                             variable=winning_condition)
    most.grid(row=11,column=0)

    least=tkinter.Radiobutton(window,text="Winner has least discs",value='LEAST',
                              variable=winning_condition)
    least.grid(row=12,column=0)
  
    def _apply_settings()->None:
        """Applies settings to othello module"""
        othello.REVERSE=reverse.get()
        othello.STARTING_PLAYER=starting_player.get()
        othello.MODE=winning_condition.get()

    def _double_function(function1,function2)->None:
        """Runs 2 functions in 1"""
        function1
        function2
    game_starter=lambda: _double_function(_apply_settings(),start_game(window))
    start_button=tkinter.Button(window,text='Start Game',
                                command=game_starter)
    start_button.grid(row=13,column=0)
    window.mainloop()




def dimensions(window)->None:
    """Opens a window to change dimensions"""
    top=tkinter.Toplevel()
    top.wm_attributes("-topmost",1)
    top.focus()
    top.title('Board Dimensions')
    top.resizable(width=False,height=False)
    r=tkinter.Label(top,text="Number of rows:")
    r.grid(row=0,column=0)

    rows=tkinter.Spinbox(top,values=(8,10,12,14,16,4,6),wrap=True,
                         state='readonly')
    rows.grid(row=1,column=0)
    
    c=tkinter.Label(top,text="Number of columns:")
    c.grid(row=2,column=0,)
    
    columns=tkinter.Spinbox(top,values=(8,10,12,14,16,4,6),wrap=True,
                            state='readonly')
    columns.grid(row=3,column=0)
    def change_dimensions(top):
        othello.BOARD_ROWS=int(rows.get())
        othello.BOARD_COLUMNS=int(columns.get())
        top.destroy()
    save=tkinter.Button(top,text='Apply Settings',
                        command=lambda a=top: change_dimensions(a))
    save.grid(row=4,column=0)

def start_game(window):
    """Starts the othello game"""
    window.destroy()
    game=othello.game()
    state=game_board(game)
    state.start()
    
class game_board:
    def __init__(self,state):
        self._state=state
        self._root_window=tkinter.Tk()
        self._root_window.title('Othello')
        self._root_window.wm_attributes("-topmost",1)
        self._root_window.focus()
        self._canvas=tkinter.Canvas(master=self._root_window,width=500,height=450,
                                    background='forest green')
        self._canvas.grid(row=0,column=0,padx=10,pady=10,sticky=tkinter.N+
                          tkinter.S+tkinter.E+tkinter.W,columnspan=2)
        self._canvas.bind('<Configure>', self._on_canvas_resize)
        self._canvas.bind('<Button-1>', self._on_mouse_click)
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._draw_board()
        self._draw_score()
        self._draw_turn()
        self._draw_pieces()
    def start(self)->None:
        self._root_window.mainloop()
    def _draw_board(self)->None:
        width=self._canvas.winfo_width()
        height=self._canvas.winfo_height()
        space_width=width/othello.BOARD_COLUMNS
        space_height=height/othello.BOARD_ROWS
        for col in range(othello.BOARD_COLUMNS):
            self._canvas.create_line(col*space_width,0,col*space_width,height,fill='black')
        for row in range(othello.BOARD_ROWS):
            self._canvas.create_line(0,row*space_height,width,row*space_height,fill='black')
    def _draw_score(self)->None:
        black_score,white_score=self._state.score()
        self._score=tkinter.Label(self._root_window,text='Score: Black: {}, White: {}'.format(black_score,white_score)
                                  ,padx=5,pady=5)
        self._score.grid(row=1,column=0,sticky=tkinter.N+tkinter.S+tkinter.W)
    def _draw_turn(self)->None:
        if self._state.turn()==othello.BLACK:
            turn='Black'
        elif self._state.turn()==othello.WHITE:
            turn='White'
        self._turn=tkinter.Label(self._root_window,text='Turn: {}'.format(turn),padx=5,pady=5)
        self._turn.grid(row=1,column=1,sticky=tkinter.N+tkinter.S+tkinter.E)
    def _on_canvas_resize(self,event)->None:
        self._redraw_board()
    def _on_mouse_click(self,event)->None:
        row_lines,column_lines=self._row_column_lists()
        for row in range(len(row_lines)):
            if event.y<row_lines[row]:
                current_row=row-1
                break
            elif event.y>row_lines[-1]:
                current_row=len(row_lines)-1
                break
        for col in range(len(column_lines)):
            if event.x<column_lines[col]:
                current_column=col-1
                break
            elif event.x>column_lines[-1]:
                current_column=len(column_lines)-1
        flip=othello._is_valid_move(self._state.board(),self._state.turn(),current_column,current_row)
        if flip==None:
            self._invalid_move()
        else:
            flip.append([current_column,current_row])
            for c, r in flip:
                self._state.drop_piece(c,r)
            self._state.change_turn()
        self._draw_game()
        status=self._game_over_check()
        if status==None:
            valid_moves=othello.valid_moves(self._state.board(),self._state.turn())
            if len(valid_moves)==0:
                self._state.no_moves()
                self._state.change_turn()
                self._draw_game()
    def _draw_game(self)->None:
        self._redraw_board()
        self._draw_score()
        self._draw_turn()
    def _redraw_board(self)->None:
        self._canvas.delete(tkinter.ALL)
        width=self._canvas.winfo_width()
        height=self._canvas.winfo_height()
        self._draw_board()
        self._draw_pieces()
    def _draw_pieces(self)->None:
        row_lines,column_lines=self._row_column_lists()
        index_list=self._check_board()
        for index in index_list:
            if index[0]==othello.BLACK:
                self._canvas.create_oval(column_lines[index[1]],row_lines[index[2]],
                                         column_lines[index[1]+1],row_lines[index[2]+1],
                                         fill='black')
            elif index[0]==othello.WHITE:
                self._canvas.create_oval(column_lines[index[1]],row_lines[index[2]],
                                         column_lines[index[1]+1],row_lines[index[2]+1],
                                         fill='white')
            elif index[0]==othello.VALID:
                self._canvas.create_rectangle(column_lines[index[1]],row_lines[index[2]],
                                              column_lines[index[1]+1],row_lines[index[2]+1],
                                              fill='gold')
    def _invalid_move(self)->None:
        top=tkinter.Toplevel()
        top.title('Invalid Move')
        top.wm_attributes("-topmost",1)
        top.focus()
        msg=tkinter.Label(top,text='This is an invalid move!')
        msg.grid(row=0,column=0)
        button=tkinter.Button(top,text="Dismiss",command=top.destroy)
        button.grid(row=1,column=0)
    def _game_over_check(self)->None:
        print('Remaining Moves: {}'.format(othello.full_board(self._state.board())))
        if othello.winning_player(self._state,othello.MODE)==othello.NONE:
            return None
        else:
            self._win_window()
    def _pass_window(self)->None:
        top=tkinter.Toplevel()
        top.title('No Valid Moves')
        top.wm_attributes("-topmost",1)
        top.focus()
        msg=tkinter.Label(top,text='Player passes. No valid moves.')
        msg.grid(row=0,column=0)
        button=tkinter.Button(top,text="Dismiss",command=top.destroy)
        button.grid(row=1,column=0)
    def _win_window(self)->None:
        if othello.winning_player(self._state,othello.MODE)==othello.BLACK:
            top=tkinter.Toplevel()
            top.title('Black player has won')
            top.wm_attributes("-topmost",1)
            top.focus()
            msg=tkinter.Label(top,text='Black player has won!')
            msg.grid(row=0,column=0)
            button=tkinter.Button(top,text="Close",
                                  command=lambda a=top,b=self._root_window: _destroy(a,b))
            button.grid(row=1,column=0)
        elif othello.winning_player(self._state,othello.MODE)==othello.WHITE:
            top=tkinter.Toplevel()
            top.title('White player has won')
            top.wm_attributes("-topmost",1)
            top.focus()
            msg=tkinter.Label(top,text='White player has won!')
            msg.grid(row=0,column=0)
            button=tkinter.Button(top,text="Close",
                                  command=lambda a=top,b=self._root_window: _destroy(a,b))
            button.grid(row=1,column=0)
        elif othello.winning_player(self._state,othello.MODE)==othello.TIE:
            top=tkinter.Toplevel()
            top.title('Tie')
            top.wm_attributes("-topmost",1)
            top.focus()
            msg=tkinter.Label(top,text='Tie!')
            msg.grid(row=0,column=0)
            button=tkinter.Button(top,text="Close",
                                  command=lambda a=top,b=self._root_window: _destroy(a,b))
            button.grid(row=1,column=0)
        def _destroy(window1,window2)->None:
            '''Destroys 2 windows'''
            window1.destroy()
            window2.destroy()
    def _check_board(self)->list:
        index_list=[]
        for y in range(othello.BOARD_ROWS):
            for x in range(othello.BOARD_COLUMNS):
                if othello.valid_moves_board(self._state.board(),self._state.turn())[x][y]!=othello.NONE:
                    index_list.append((othello.valid_moves_board(self._state.board(),self._state.turn())[x][y],x,y))
        return index_list
    def _row_column_lists(self)->(list,list):
        width=self._canvas.winfo_width()
        height=self._canvas.winfo_height()
        space_height=height/othello.BOARD_COLUMNS
        space_width=width/othello.BOARD_ROWS
        row_lines=[]
        column_lines=[]
        for row in range(othello.BOARD_ROWS):
            row_lines.append(row*space_height)
        row_lines.append(height)
        for col in range(othello.BOARD_COLUMNS):
            column_lines.append(col*space_width)
        column_lines.append(width)
        return row_lines,column_lines
if __name__ == '__main__':
    settings()

