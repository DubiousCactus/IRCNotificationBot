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

import signal
import re

from server import IRCServer
from utils import Util
from sys import argv

class Watchdog:

    debug = False

    def __init__(self, debug = False):
        self.debug = debug
        self._currentUsers = []
        self._server = IRCServer(self, debug)
        self._admin = Util.config('admin', debug)
        self._exitCode = Util.config('exitCode', debug)
        self._importantCode = Util.config('importantCode', debug)
        self._notifs = Util.config('notifications', debug)
        self._whitelist = Util.config('whitelist', debug)
        self._usesWhitelist = Util.config('usesWhitelist', debug)
        self._viplist = Util.config('viplist', debug)

        self._server.join_channel()


    def user_left(self, user):
        if self._currentUsers.count(user) != 0:
            self._currentUsers.remove(user)
            # Send desktop notification
            Util.notify(self._notifs['part']['title'], self._notifs['part']['body'].replace("##USER##", user))


    def user_joinned(self, user):
        if self._currentUsers.count(user) == 0 and user != self._admin and ((self._usesWhitelist and self._whitelist.count(user)) or not self._usesWhitelist):
            self._currentUsers.append(user)
            # Send desktop notification
            Util.notify(self._notifs['join']['title'], self._notifs['join']['body'].replace("##USER##", user))


    def important(self, message, sender):
        if self._viplist.count(sender):
            Util.notify(self._notifs['important']['title'], self._notifs['important']['body'].replace("##USER##", sender).replace("##MSG##", message))


    # Handle the incoming message depending on its content
    def process_message(self, msg, sender):
        if self.debug: print("[DEBUG] Processing message \"{}\" from [{}]".format(msg, sender))
        if len(msg) < 1:
            raise Error("/!\ Invalid message !")

        if msg.rstrip() == self._exitCode and sender.lower() == self._admin.lower():
            self._server.stop()
        elif re.match('^{} {}: .+'.format(self._importantCode, self._admin), msg):
            # Important message: <importantCode> <this_admin>: <message>
            self.important(msg.split(':')[1][1:], sender)


    def signal_handler(self, signal, frame):
        print("[!] Ctrl+C caught: Terminating...")
        self._server.stop()

    
    def run(self):
        self._server.watch()


if __name__ == "__main__":
    if len(argv) > 1 and argv[1].lower() == "debug":
        print("[INFO] Running in debug mode")
        watchdog = Watchdog(True)
    else:
        print("[INFO] Running in production mode")
        watchdog = Watchdog()

    signal.signal(signal.SIGINT, watchdog.signal_handler)
    watchdog.run()
