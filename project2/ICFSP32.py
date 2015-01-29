'''
Created on Apr 17, 2013

@author: Harry
'''
#Harry Pham 79422112 and Kevin Nguyen 53581426
import collections, socket

"""SOCKET HANDLING"""
_I32CFSPConnection=collections.namedtuple(
    '_I32CFPConnection', ['socket', 'socket_input', 'socket_output'])

class I32CFSPError(Exception):
    pass

def _initiate_connection(ip_address,port):
    """Given a IP address and a port, this function initiates a connection and
    returns an _I32CFPConnection object describing that connection. This
    function may raise exceptions that are related to socket connectivity if
    the attempt to connect fails."""
    connect_socket=socket.socket()
    connect_socket.connect((ip_address, port))
    return _build_connection_object(connect_socket)

def _accept_connection(ip_address, port):
    """Given a IP adress and a port, this function waits for a connection to
    arrive on that port. It then builds an I32CFSPConnection object describing
    that connection."""
    listen_socket=socket.socket()
    listen_socket.bind((ip_address,port))
    listen_socket.listen(0)
    connect_socket, from_address = listen_socket.accept()
    listen_socket.close()
    return _build_connection_object(connect_socket)

def _build_connection_object(connect_socket):
    """Takes a socket and builds an _I32CFSPConnection namedtuple from it."""
    connect_socket_input=connect_socket.makefile('r')
    connect_socket_output=connect_socket.makefile('w')
    return _I32CFSPConnection(
        socket=connect_socket, socket_input=connect_socket_input,
        socket_output=connect_socket_output)

def _close_connection(connection):
    """Closes a connection."""
    connection.socket_input.close()
    connection.socket_output.close()
    connection.socket.close()

def _send_message(connection, message):
    """Sends a message"""
    connection.socket_output.write(message+'\n')
    connection.socket_output.flush()

def _recieve_message(connection, message=True):
    """Recieves a message, raising an ICFPError if anything other than the
    message given is recieved"""
    if message==True:
        return connection.socket_input.readline()[:-1]
    elif connection.socket_input.readline()[:-1] != message:
        raise I32CFSPError()
