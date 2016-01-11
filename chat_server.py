#!/usr/bin/python
import sys
import socket
import select
import string
import random
import argparse
import traceback

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Client:
    nickname = ""
    socket = None
    def __init__(self, nickname, socket):
        self.nickname = nickname
        self.socket = socket

class Chat_info:
    participants  = []
    id = []
    chat_name = ""
    sockets = []
    def __init__(self, id, participants, sockets):
        self.id = id
        self.participants = participants
        self.sockets = sockets
    
    
debugprint = lambda *a: None
def errorprint(string):
    print bcolors.FAIL + "[Error] " + bcolors.ENDC + string
chats = []
clients = []

def id_generator(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))
    
def send(server_socket, socks, message):
    #print socks
    for socket in SOCKET_LIST:
        #print socket in socks
        if socket != server_socket and socket in socks:
            try:
                debugprint("Sending {}".format(message))
                socket.send(message)
            except:
                #socket.close()
                errorprint("Exception")
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

#determines who to send it to  
def handle_received(data, client, server_socket):
    #handle data
    #   private chat start /p <person>
    #   chat send /s <id> <message>
    global SOCKET_LIST
    debugprint("Received data {} from {}".format(data, client.nickname))
    if not data:
        errorprint("Empty data")
        return 0

    if not data[0] == "/":
        errorprint("Data not formatted properly {}".format(data))
        return 0

    split = data[1:].split(" ")
    if len(split) < 2:
        errorprint("Empty command")
        return 0

    command = split[0]

    if command == "nick":
        client.nickname = split[1][0:-1]

    elif command == "s" or command == "e":
        if len(split) < 3:
            errorprint("Improper send format")
            return 0
        chat_ids = [chat.id for chat in chats]
        if split[1] not in chat_ids:
            errorprint("Invalid chat id")
            #send error to client
        else:
            if command == "s":
                data = data[0:-1]
            debugprint("Sending data {}".format(data))
            chat = None
            for c in chats:
                if c.id == split[1]:
                    chat = c
            socks = list(chat.sockets)
            #print socks
            socks.remove(client.socket)
            try:
                send(server_socket, socks, "\r" + '[' + client.nickname + ']' + data)
            except:
                e = sys.exc_info()[0]
                print e
            #print len(socks)
    else:
        send(server_socket, SOCKET_LIST, "\r" + '[' + client.nickname + '] ' + data)
    
def server_loop():
    global debugprint
    global chats
    global SOCKET_LIST
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10)
    
    SOCKET_LIST.append(server_socket)
    
    debugprint("Chat server started on port " + str(PORT))
    
    chats.append(Chat_info("0", [], [])) #create group chat

    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST, [], [], 0)
        #debugprint(ready_to_read)
        #debugprint(server_socket)
        for sock in ready_to_read:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                debugprint("Client (%s, %s) connected" % addr)
                send(server_socket, SOCKET_LIST, "/s 0 [%s,%s] entered our chat \n" % addr)
                chats[0].sockets.append(sockfd)
                debugprint("Group chat sockets: {}".format(chats[0].sockets))
                clients.append(Client(id_generator(size=8), sockfd))
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    client = None
                    for c in clients:
                        if c.socket == sock:
                            client = c
                    if data:
                        handle_received(data, client, server_socket)
                    else:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                            debugprint("Client (%s, %s) left" % addr)
                            send(server_socket, sock, "Client (%s, %s) has left\n" % addr)
                            
                except:
                    #send(server_socket, sock, "Client (%s, %s) has left\n" % addr)
                    #print "Exception?"
                    continue
                    
    server_socket.close()
    
def main():
    global debugprint
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Display debug messages", default=False, action="store_true")
    args = parser.parse_args()
    if args.debug:
        def x(string):
            print bcolors.OKBLUE + "[Debug] " + bcolors.ENDC + string
        debugprint = x
        debugprint("Debug mode started")
        errorprint("Errors look like this") 
    server_loop()
    
if __name__ == "__main__":
    main()
    
