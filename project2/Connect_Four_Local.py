import Connect_Four_Functions
def handle_commands()->None:
    '''Displays a menu and handles command'''
    response=input(Connect_Four_Functions.MENU)
    if response == 'n':
        Connect_Four_Functions._current_game(Connect_Four_Functions._new_game())
        return handle_commands()
    elif response == 'q':
        return
    else:
        Connect_Four_Functions.invalid_command(response)

if __name__ == '__main__':
    print('Welcome to Connect Four Local Program.')
    handle_commands()
