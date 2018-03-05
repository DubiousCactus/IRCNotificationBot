#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 transpalette <transpalette@arch-cactus>
#
# Distributed under terms of the MIT license.

"""
IRC Server class: handles the connection, the configuration...
"""

import urllib2
import socket
import select
import time
import json
import sys
import re

from utils import Util

class IRCServer:
 
    debug = False

    def __init__(self, callback, debug):
        self.debug = debug

        self._channel = Util.config('channel', debug)
        self._botName = Util.config('botName', debug)
        self.check_nickname()
        self._timeout = Util.config('receiveTimeout', debug)
        self._notifs = Util.config('notifications', debug)

        self._running = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((Util.config('server', debug), Util.config('port', debug)))
        self._sock.setblocking(0)

        self._callback = callback


    def check_nickname(self):
        chars = set("!@#$%&*()+=';/,.<>\"")

        if any((c in chars) for c in self._botName):
            print("[ERROR] Unsupported special characters found in botName")
            Util.notify("IRC Notification bot [ERROR]", "The chosen nickname contains special characters.")
            sys.exit(1)


    def join_channel(self):
        if self.debug: print("[DEBUG] Authenticating...")
        # Authenticating
        self._sock.send(bytes("USER "+ self._botName +" "+ self._botName +" "+ self._botName + " " + self._botName + "\n", "UTF-8")) #We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
        self._sock.send(bytes("NICK " + self._botName + "\n", "UTF-8")) # Assign the nickname to the bot

        if self.debug: print("[DEBUG] Joinning channel {}...".format(self._channel))
        self._sock.send(bytes("JOIN " + self._channel + "\n", "UTF-8"))
        ircmsg = ""

        while ircmsg.find("End of /NAMES list.") == -1 and ircmsg.find("Nickname is already in use") == -1:
            if select.select([self._sock], [], [], self._timeout)[0]:
                ircmsg = self._sock.recv(2048).decode("UTF-8").strip('\n\r')

        if ircmsg.find("Nickname is already in use") != -1:
            print("[ERROR] Nickname already in use")
            Util.notify("IRC Notification bot [ERROR]", "The chosen nickname is already in use.")
            sys.exit(1)

        if self.debug: print("[DEBUG] Channel joinned.")
        Util.notify('IRC Notifier', 'Successfuly joinned {}'.format(self._channel))


    # Respond to pings
    def pong(self):
        if self.debug: print("[DEBUG] Pong")
        self._sock.send(bytes("PONG :pingis\n", "UTF-8"))


    # Receive a command / message
    def recv(self):
        last_ping = time.time()
        threshold = 256 # 256 seconds on Freenode
        while self._running:
            ready = select.select([self._sock], [], [], self._timeout)

            if ready[0]:
                if self.debug: print("[DEBUG] Receiving 1024 bytes...")
                ircmsg = self._sock.recv(1024).decode("UTF-8").strip('\n\r')
                if self.debug: print("[DEBUG] {}".format(ircmsg))
            
                '''
                Format of a private message from IRC:
                    [Nick]!~[hostname]@[IP Address] PRIVMSG [channel] :[message]
                '''
                if re.match("^:.+!.+@.+ PRIVMSG {} :".format(self._botName), ircmsg):
                    if self.debug: print("[DEBUG] Received private message")
                    sender = ircmsg.split('!', 1)[0][1:]
                    message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1]
                    self._callback.process_message(message, sender)
                elif re.match("^PING :.+", ircmsg):
                    if self.debug: print("[DEBUG] Ping")
                    last_ping = time.time()
                    self.pong()
                elif re.match("^:.+!.+@.+ JOIN #.+", ircmsg):
                    self._callback.user_joinned(ircmsg.split('!')[0][1:])
                elif re.match("^:.+!.+@.+ PART #.+", ircmsg):
                    self._callback.user_left(ircmsg.split('!')[0][1:])
            else:
                if self.debug: print("[DEBUG] Not ready to receive")
                if (time.time() - last_ping) > threshold and not self.is_connected():
                    self.reconnect()
                    break


    def is_connected(self):
        self._sock.send(bytes("/names\n", "UTF-8"))
        ready = select.select([self._sock], [], [], self._timeout)
        
        return ready[0]

    def reconnect(self):
        if self.debug: print("[DEBUG] Reconnecting...")
        self._sock.close()
        while not internet_on(): time.sleep(1)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((Util.config('server', self.debug), Util.config('port', self.debug)))
        self._sock.setblocking(0)
        self.join_channel()
        self.watch()


    def internet_on():
        try:
            urllib2.urlopen('http://216.58.192.142', timeout=1) # Google's IP
            return True
        except urllib2.URLError as err:
            return False
 

    def watch(self):
        if self.debug: print("[DEBUG] Starting the watch...")
        self._running = True
        self.recv()


    def stop(self):
        if self.debug: print("[DEBUG] Stopping the watch...")
        self._running = False
        self._sock.send(bytes("QUIT \n", "UTF-8"))
        self._sock.close()
        if self.debug: print("[DEBUG] Socket closed.")
        sys.exit(0)

