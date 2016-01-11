#!/usr/bin/python
import sys
import socket
import select
import argparse
from Crypto.Cipher import AES

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    GREEN_HI = '\033[102m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class chat_info:
    id = ""
    partner = ""
    key = ""
    iv = ""
    #key_exchange():
    def decrypt(mesage):
        return 0
        
current_id = "0"
current_cmd = "s"
chats = []

def messageprint(id, message):
    print "{}[{} {}{}".format(bcolors.PURPLE, id, bcolors.ENDC, message)
    sys.stdout.write('{}[Me]{} '.format(bcolors.BLUE, bcolors.ENDC)); sys.stdout.flush()

def errorprint(message):
    print "\n{}[Error]{} {}".format(bcolors.RED, bcolors.ENDC, message)

def infoprint(message):
    print "{}{}{}".format(bcolors.GREEN, message, bcolors.ENDC)

def pad(message):
    pad_length = 16 - (len(message)%16)
    message += pad_length*"\x90"
    return message

def format_message(input):
    global current_cmd
    global current_id
    command = ""
    command_prepended = False
    id = determine_id(input)
    message = ""
    if input[0] != "/":
        cmd = "/" + current_cmd
    elif input[0:2] == "/s":
        current_cmd = "s"
        command = "/s"
        command_prepended = True
    elif input[0:2] == "/e":
        command_prepended = True


def determine_id(message):
    if message[0] != "/":
        return "/s " + current_id + " " + message
    elif message[0:2] == "/e":
        message = message[1:].split(' ')[1]
        return "/e " + current_id + " " + encryptmessage(current_id, message)
    else:
        command = message[1:].split(' ')[0]
        if command == "nick":
            if len(message[1:].split(' ')) < 2:
                errorprint("Blank nickname")
            else:
                return message
        elif command == "s":
            id = message[1:].split(' ')[1]
            for chat in chats:
                if id == chat.id:
                    return message
            return None    
        elif command == "e":
            id = current_id
            message = message[1:].split(' ')[1]
            for chat in chats:
                if id == chat.id:
                    message = pad(message)
                    infoprint(len(message))
                    return encryptmessage(id, message)

def decryptmessage(id, message):
    aes = AES.new("This is a key123", AES.MODE_CBC, "This is an IV456")
    #infoprint("Message: {}\nLength: {}".format(message, len(message)))
    decrypt = aes.decrypt(message)
    result = "{}>{} {}".format(bcolors.GREEN_HI, bcolors.ENDC, decrypt)
    result = result.rstrip("\x90")
    result = result.rstrip("\n")
    messageprint(id, result)

def encryptmessage(id, message):
    message = pad(message)
    aes = AES.new("This is a key123", AES.MODE_CBC, "This is an IV456")
    ciphertext = aes.encrypt(message)
    return ciphertext

def list_ids():
    for chat in chats:
        print "{} with {}".format(chat.id, chat.partner)
    
def send(message,s):
    message_w_id = determine_id(message)
    print message_w_id
    if message_w_id is None:
        errorprint("Incorrect chat id")
    else:
        s.send(message_w_id)

def handle_received(data):
    split = data.split(' ')
    id_cmd_split = split[0].split('/')
    id = id_cmd_split[0]
    command = id_cmd_split[1]
    if command == "s":
        message = ' '.join(split[2:])
        messageprint(id, message)
    elif command == "e":
        message = ' '.join(split[2:])
        decryptmessage(id, message)

def chat_loop(s):
    infoprint("You have joined the chat")
    sys.stdout.write('[Me] '); sys.stdout.flush()
    while 1:
        socket_list = [sys.stdin, s]
        
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
        
        for sock in ready_to_read:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    errorprint('Disconnected from chat server')
                    sys.exit()
                else:
                    #print "Data received {}".format(data)
                    handle_received(data)
                    #sys.stdout.write('[Me] '); sys.stdout.flush()
            else:
                msg = sys.stdin.readline()
                send(msg,s) 
                sys.stdout.write('{}[Me]{} '.format(bcolors.BLUE, bcolors.ENDC)); sys.stdout.flush()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="Host to connect to", required=True)
    parser.add_argument("-p", "--port", help="Port to connect to", required=True)
    
    args = parser.parse_args()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((args.host, int(args.port)))
    except:
        errorprint('Unable to connect')
        sys.exit()
        
    chat_loop(s)
        
if __name__ == "__main__":
    main()
