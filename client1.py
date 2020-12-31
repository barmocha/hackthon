import socket
import struct
import random
import time 
import msvcrt
import os
 
localIP= "127.0.0.1"
buffer =2048
tcp_port = 12117
server_port = 13117
unicode_trans = 'utf-8'
timer_10 = 10

def client_program():
    """
    main method in which opens a connections in front of the server
    """
    while True:    
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ixd =random.randrange(255)
        client_socket.bind(("127.0.0.{}".format(ixd), server_port))
        print("​Client started, listening for offer requests...​")

        now = time.time()
        future = now + timer_10

        message, serverAddress = client_socket.recvfrom(buffer)
        address = struct.unpack('QQQ',message)
        print("Received offer from ​%s, attempting to connect..."%serverAddress[0])       
        client_socket.close()
        
        while True:
            if time.time() > future:
                break            
        connectToServerThroughTCP()

def connectToServerThroughTCP():
    # Create a TCP/IP socket
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("connecting to server %s"%localIP)
    tcp_sock.connect((localIP,tcp_port))

    try:   
        # Send data from client to server
        message = 'Team gal gadot'
        tcp_sock.send(message.encode(unicode_trans))

        (open_client_text, address) = tcp_sock.recvfrom(buffer)
        print(open_client_text.decode(unicode_trans))

        now = time.time()
        future = now + timer_10
        while True:
            if time.time() > future:
                break
            game_action_keyboard(tcp_sock, (localIP,tcp_port))

        (end_client_text, address) = tcp_sock.recvfrom(buffer)
        print(end_client_text.decode(unicode_trans))
        print("Server disconnected, listening for offer requests...")

    finally:
        tcp_sock.close()

def game_action_keyboard(tcp_sock, serverAddress):
    """
    part of game mode - collect characters and from the keyboard and send them over TCP. collect
    data from the network. Input input - typing from the customer
    """
    char_key = msvcrt.getch()
    print(char_key)
    tcp_sock.sendall(char_key)

if __name__ == '__main__':
    client_program()
