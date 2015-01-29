import connectfour, Connect_Four_Functions, ICFSP32

"""CLIENT"""
def client()->None:
    """Connects to a server for connect four game"""
    failure=False
    ip_address=input("Please enter an IP address or hostname: ").strip()
    while True:
        try:
            port=int(input("Please enter a port: ").strip())
            break
        except ValueError:
            print('You have inputted an invalid port. Please try again.')
    while True:
        try:
            username=input("Please enter a username that has no spaces: ").strip()
            if ' ' in username or username=='':
                raise ValueError("Invalid Username.")               
            else:
                break
        except ValueError:
            print("Invalid Username. Please try again.")
    print('Connecting...')
    try:
        connection=ICFSP32._initiate_connection(ip_address, port)
    except ConnectionRefusedError:
        print('Connection Refused')
        failure=True
        return handle_commands(failure)
    try:
        ICFSP32._send_message(connection, 'I32CFSP_HELLO {}'.format(username))
        ICFSP32._recieve_message(connection, 'WELCOME {}'.format(username))
        ICFSP32._send_message(connection, 'AI_GAME')
        print('Connection Successful.')
    except ICFSP32.I32CFSPError:
        print('Connection Failure.')
        failure=True
        return handle_commands(failure)
    try:
        Connect_Four_Functions._current_game(Connect_Four_Functions._new_game(), True, connection)
    except ConnectionResetError:
        ('Connection Closed By Other User.')
        failure=True
    finally:
        ICFSP32._close_connection(connection)
    return handle_commands(failure)

FAILMENU="""
Connection Failure Menu --- Choose One
 n: Try again
 q: Quits Connect Four Program
"""

def handle_commands(failure=False)->None:
    '''Displays Menu and handles commands'''
    while True:
        if failure == False:
            response=input(Connect_Four_Functions.MENU).strip().lower()
        elif failure== True:
            response=input(FAILMENU).strip().lower()
        if response=='n':
            return client()
        elif response=='q':
            return
        else:
            Connect_Four_Functions.invalid_command(response)

if __name__ == '__main__':
    print('Welcome to the Connect Four Network Program.')
    client()
