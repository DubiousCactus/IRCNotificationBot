#! /usr/bin/python3 
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 transpalette <transpalette@arch-cactus>
#
# Distributed under terms of the MIT license.

"""
Small bot that sends desktop notifications when users log in/out
"""

import socket
import os
import signal
import select
import json
from pathlib import Path

running = True
currentUsers = []

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config_location = str(Path.home()) + "/.config/IRCNotificationBot/config.json"
timeout = 1
server = ""
channel = ""
botName = ""
admin = ""
exitCode = ""

notifs = {
    "join": {
        "title": "IRC Notification",
        "body": "##USER## joinned the channel ##CHANNEL##"
    },
    "part": {
        "title": "IRC Notification",
        "body": "##USER## has left the channel ##CHANNEL##"
    }
}


def init():
    with open(config_location) as config_file:
        config = json.load(config_file)

    global server, port, botName, admin, exitCode, timeout, channel
    server = config['server']
    port = config['port']
    channel = config['channel']
    botName = config['botName']
    admin = config['admin']
    exitCode = config['exitCode']
    timeout = config['receiveTimeout']

    print("[*] Connecting to {}...".format(server))

    # Connecting to the server
    ircsock.connect((server, port))
    ircsock.setblocking(0)

    print("[*] Authenticating as {}...".format(botName))
    # Authenticating
    ircsock.send(bytes("USER "+ botName +" "+ botName +" "+ botName + " " + botName + "\n", "UTF-8")) #We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
    ircsock.send(bytes("NICK " + botName + "\n", "UTF-8")) # Assign the nickname to the bot


# Join the channel
def join_chan(chan):
    print("[*] Joinning channel {}...".format(chan))

    ircsock.send(bytes("JOIN " + chan + "\n", "UTF-8"))
    ircmsg = ""

    while ircmsg.find("End of /NAMES list.") == -1:
        if select.select([ircsock], [], [], timeout)[0]:
            ircmsg = ircsock.recv(2048).decode("UTF-8").strip('\n\r')

    print("[*] Channel successfuly joint !")


# Respond to pings
def pong():
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))


# Kill the bot
def kill_bot():
    global running
    running = False
    print("[*] Received death sentence :(")


# Receive a command / message
def recv():
    ready = select.select([ircsock], [], [], timeout)

    if ready[0]:
        ircmsg = ircsock.recv(1024).decode("UTF-8").strip('\n\r')
    
        '''
        Format of a private message from IRC:
            [Nick]!~[hostname]@[IP Address] PRIVMSG [channel] :[message]
        '''
        if ircmsg.find("PRIVMSG") != -1:
            sender = ircmsg.split('!', 1)[0][1:]
            message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1]
            handle_msg(message, sender)
        elif ircmsg.find("PING") != -1:
            pong()
        elif ircmsg.find("JOIN") != -1:
            user_joinned(ircmsg.split('!')[0][1:])
        elif ircmsg.find("PART") != -1:
            user_left(ircmsg.split('!')[0][1:])


def user_left(user):
    if currentUsers.count(user) != 0:
        currentUsers.remove(user)
         # Send desktop notification
        os.system("notify-send '{}' '{}' --icon=dialog-information".format(notifs['part']['title'], notifs['part']['body'].replace("##USER##", user).replace("##CHANNEL", channel)))



def user_joinned(user):
    if currentUsers.count(user) == 0:
        currentUsers.append(user)
         # Send desktop notification
        os.system("notify-send '{}' '{}' --icon=dialog-information".format(notifs['join']['title'], notifs['join']['body'].replace("##USER##", user).replace("##CHANNEL", channel)))


# Handle the incoming message depending on its content
def handle_msg(msg, sender):
    if len(msg) < 1:
        raise Error("/!\ Invalid message !")

    if msg.rstrip() == exitCode and sender.lower() == admin.lower():
        kill_bot()


def signal_handler(signal, frame):
    print("[!] Ctrl+C caught: Terminating...")
    kill_bot()


# Main loop...
def main_loop():

    init()
    join_chan(channel)
    signal.signal(signal.SIGINT, signal_handler)

    while running:
        recv()

    print("[!] Quitting...")

    ircsock.send(bytes("QUIT \n", "UTF-8"))
    ircsock.close()
    return

main_loop()
