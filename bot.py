#! /usr/bin/python3 
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 transpalette <transpalette@arch-cactus>
#
# Distributed under terms of the MIT license.

"""
Small bot to notify me when Hannes logs in
"""

import socket
import os
import time
import signal

from threading import Thread, Lock

running = True
hannesHasJoinned = False
mutex = Lock()

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net"
channel = "#subseven"
botnick = "Cyber-Theo-9000"
admin = "transpalette"
exitCode = "die bitch!"

notifs = {
    "away": {
        "title": "AFK notice",
        "body": "##USER## went away"
    },
    "join": {
        "title": "Join notice",
        "body": "##USER## joinned the channel " + channel
    }
}

def heart_beat():
    while running:
        time.sleep(6) # Sleep 3 seconds between each check
        mutex.acquire()
        try:
            users = get_users_list()
        finally:
            mutex.release()

        # parse users list and if hannes joined, notify
        for user in users:
            print("[DEBUG] user: " + user)
            if ((user.lower().find("hannes") != -1) or (user.lower().find("bartle") != -1)) and (not hannesHasJoinned):
                user_joinned("Hannes")
                hannesHasJoinned = True
            

def init():
    print("[*] Connecting to {}...".format(server))

    # Connecting to the server
    ircsock.connect((server, 6667))


    print("[*] Authenticating as {}...".format(botnick))

    # Authenticating
    ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) #We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
    ircsock.send(bytes("NICK " + botnick + "\n", "UTF-8")) # Assign the nickname to the bot

# Join the channel
def join_chan(chan):
    print("[*] Joinning channel {}...".format(channel))

    ircsock.send(bytes("JOIN " + chan + "\n", "UTF-8"))
    ircmsg = ""

    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')

    print("[*] Channel successfuly joint !")

# Respond to pings
def ping():
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))
    print("[DEBUG] Sending PONG...")

# Kill the bot
def kill_bot():
    global running
    running = False
    print("[*] Received end of life order :(")


# Send a message
def send_msg(msg, target=channel):
    ircsock.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))
    print("[*] Sending message: {} to {}".format(msg, target))


# Receive and process a message
def recv_msg():
    ircmsg = ircsock.recv(2048).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    
    '''
    Format of a message from IRC:
        [Nick]!~[hostname]@[IP Address] PRIVMSG [channel] :[message]
    '''
    if ircmsg.find("PRIVMSG") != -1:
        sender = ircmsg.split('!', 1)[0][1:]
        message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1]
    else:
        message = '[ERROR]'
        sender = '[ERROR]'

    return {'body': message, 'sender': sender}

# Notify when a user goes away (afk)
def went_away(user):
    # Send desktop notification
    os.system("notify-send '{}' '{}' --icon=dialog-information".format(notifs['away']['title'], notifs['away']['body'].replace("##USER##", user)))


def user_joinned(user):
     # Send desktop notification
    os.system("notify-send '{}' '{}' --icon=dialog-information".format(notifs['join']['title'], notifs['join']['body'].replace("##USER##", user)))

def get_users_list():
    ircsock.send(bytes("NAMES " + channel + "\n", "UTF-8"))
    ircmsg = ""
    users = []
    
    ircmsg = ircsock.recv(1024).decode("UTF-8").strip('\n\r')
    print("[DEBUG] " + ircmsg)
    users = ircmsg.split(':')[-1].split(" ")

    return users

# Handle the incoming message depending on its content
def handle_msg(msg, sender):
    if len(msg) < 1:
        raise Error("/!\ Invalid message !")

    if msg.find('Hi ' + botnick) != -1:
        send_msg("What's up mah bitch {} ?!".format(sender))
    elif msg.lower().find('alright fam') != -1 and msg.find('?') != -1:
        send_msg("Yeah bruh, gotcha")
    elif msg.find("AWAY") != -1: # :nick!user@host AWAY [:message]
        print("[DEBUG] Attempting an AWAY")
        went_away(msg.split('!')[0][1:])
    elif msg.rstrip() == exitCode and sender.lower() == admin.lower():
        kill_bot()
    elif msg.find("PING :") != -1:
        ping()


def signal_handler(signal, frame):
    print("[!] Ctrl+C caught: Terminating...")
    kill_bot()

# Main loop...
def main_loop():

    init()
    join_chan(channel)
    # signal.signal(signal.SIGINT, signal_handler)

    # Start heart beat
    try:
        t_heartBeat = Thread(target=heart_beat)
        t_heartBeat.start()
    except:
        print("[!] Unable to start thread :/")

    while running:
       #  mutex.acquire()
        # try:
            # msg = recv_msg()
            # handle_msg(msg['body'], msg['sender'])
        # finally:
       #      mutex.release()
        
        # print("[*] Receiving message: {}".format(msg))
        time.sleep(1)

    print("[!] Quitting...")

    ircsock.send(bytes("QUIT \n", "UTF-8"))
    ircsock.close()
    return

main_loop()
