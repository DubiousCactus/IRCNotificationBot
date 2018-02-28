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
import json

from pathlib import Path
from server import IRCServer
from utils import Util

class Watchdog:

    config_location = str(Path.home()) + "/.config/IRCNotificationBot/config.json"

    def __init__(self):
        with open(self.config_location) as config_file:
            config = json.load(config_file)

        self._currentUsers = []
        self._admin = config['admin']
        self._exitCode = config['exitCode']
        self._notifs = config['notifications']
        self._notifs['part']['body'] = self._notifs['part']['body'].replace('##CHANNEL##', config['channel'])
        self._notifs['join']['body'] = self._notifs['join']['body'].replace('##CHANNEL##', config['channel'])
        self._server = IRCServer(self)


    def user_left(self, user):
        if self._currentUsers.count(user) != 0:
            self._currentUsers.remove(user)
            # Send desktop notification
            Util.notify(self._notifs['part']['title'], self._notifs['part']['body'].replace("##USER##", user))


    def user_joinned(self, user):
        if self._currentUsers.count(user) == 0 and user != self._admin:
            self._currentUsers.append(user)
            # Send desktop notification
            Util.notify(self._notifs['join']['title'], self._notifs['join']['body'].replace("##USER##", user))


    # Handle the incoming message depending on its content
    def process_message(self, msg, sender):
        if len(msg) < 1:
            raise Error("/!\ Invalid message !")

        if msg.rstrip() == self._exitCode and sender.lower() == self._admin.lower():
            self._server.stop()


    def signal_handler(self, signal, frame):
        print("[!] Ctrl+C caught: Terminating...")
        self._server.stop()

    
    def run(self):
        self._server.watch()


if __name__ == '__main__':
    watchdog = Watchdog()
    signal.signal(signal.SIGINT, watchdog.signal_handler)
    watchdog.run()
