import socket
import sys
from _thread import *
import threading
import time
import struct
from threading import Thread


localIP= "127.0.0.1"
port = 13117
buffer =2048
tcp_port = 12117
timer_10 =10
unicode_trans = 'utf-8'

global teams_dic
global firstTeam 
global secondTeam
lock=threading.Lock()

teams_dic = {}
firstTeam = {}
secondTeam = {}


def broadcast():
    """
    this function creates a udp connection using struct package
    """
    try:
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        udp_server.bind((localIP,port))
        udp_server.settimeout(0.2)
        magic_cookie = 0xfeedbeef
        localPort = 13117 
        message_type= 0x2
        message = struct.pack('QQQ', magic_cookie, message_type,localPort)
        server_address = (localIP, port)

        now = time.time()
        future = now + 15
 
        print("Server started, listening on IP address ​%s"%server_address[0])        

        while True:
            if time.time() > future:
                break
            udp_server.sendto(message, ('<broadcast>',port))
            time.sleep(1)
        udp_server.close()

    except Exception as e:
        udp_server.close()
        print(e)

def connectToClientThroughTCP(tcp_server_socket):
    """
    connect to all clients on tcp protcol
    @tcp_server_socket - a tcp connection from the start server
    """

    try:
        now = time.time()
        future = now + timer_10
        time_plus_10 = time.time() + timer_10
        tcp_server_socket.settimeout(time_plus_10 - time.time())
        while True:
            conn, address = tcp_server_socket.accept()
            data = conn.recv(buffer)
            team_name = data.decode(unicode_trans)
            lock.acquire()
            if len(teams_dic) > 0 and team_name == "Team gal gadot":
                team_name = "batmam"
            teams_dic[team_name] = conn,address 
            lock.release()

    except Exception as e:
        print(e)
    
def pre_game(teams_dic):
    """
    this fuction split the clients to two teams
    @teams_dic - dictionary of all names and ports of clients
    """
    i = 0
    message = ""
    for team in teams_dic.keys():
        if i % 2 == 0:
            firstTeam[team] = teams_dic[team]
        else:
            secondTeam[team] = teams_dic[team]
        i += 1

    message += 'Welcome To Keyboard Spamming Battle Royale. \nGroup 1:\n==\n'
    for team in firstTeam.keys():
        message += str(team) + "\n"
    message += "Group 2:\n==\n"
    for team in secondTeam.keys():
        message += str(team) + "\n"
    ###########server send a message to client
    message += 'Start pressing keys on your keyboard as fast as you can!!\n'
    return message

def start_game():
    """
    this fuction is getting inputs from clients and count it by te two groups
    """
    try:
        count_team1 = 0
        count_team2 = 0
        
        list_conn =[]
        for value_team in teams_dic.values():
            conn,address = value_team    
            list_conn.append(conn)
        now = time.time()
        future = now + 10
        final_list = []
        while time.time() < future:
            conn,address = teams_dic["Team gal gadot"]
            (data_1, address) = conn.recvfrom(buffer)
            if not data_1:
                continue
            is_in_team1 = False
            for team in firstTeam.keys():
                rrd = firstTeam[team][1]
                rr = firstTeam[team][1][1]
                if address[1] == firstTeam[team][1][1]:
                    count_team1 += 1
                    is_in_team1 =True
                    break
                if not is_in_team1:
                    count_team2 += 1    
        scores = (count_team1,count_team2)     
        return scores

    except Exception as e:
        print(e)

def post_game(scores):
    """
    this fuction prints the results of the game and the winners
    @scores- contains the toal score for each team
    """
    count_team1 = scores[0]
    count_team2 = scores[1]
    message = ""
    message += "Game over!\n"
    message += "Group 1 typed in " + str(count_team1) + " characters. Group 2 typed in " + str(count_team2) + " characters.\n"
    if count_team1>count_team2:
        message += "Group 1 wins!\n"
    else: 
        message += "Group 2 wins!\n"
    message += "Congratulations to the winners:\n==\n"
    if count_team1>count_team2:
        for team in firstTeam.keys():
            message += str(team)
    else:
        for team in secondTeam.keys():
            message += str(team)
    return message


def game():
    """
    this fuction manage the game- pre game, start game and post game
    """
    try:
        start_message = pre_game(teams_dic)
        for team_conn in teams_dic.values():
            team_conn[0].send(start_message.encode(unicode_trans))

        scores = start_game()

        end_message = post_game(scores)
        for team_conn in teams_dic.values():
            team_conn[0].send(end_message.encode(unicode_trans))
            
    except Exception as e:
        print(e) 
    print("Game over, sending out offer requests...")

def server_begin():
    """
    main method - open connections 
    """
    while True:
        try:
            tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_server_socket.bind((localIP,tcp_port))
            tcp_server_socket.listen(timer_10)

            udp_thread = Thread(target = broadcast,args = ())
            tcp_thread = Thread(target = connectToClientThroughTCP,args=(tcp_server_socket,))
            udp_thread.start()
            tcp_thread.start()
            udp_thread.join()
            tcp_thread.join()
            game()

            tcp_server_socket.close()

        except EOFError as error:
            print(error)

if __name__ == "__main__":
    server_begin() 


