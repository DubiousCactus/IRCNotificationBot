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
import server
import utils
import json

class Watchdog:

    config_location = str(Path.home()) + "/.config/IRCNotificationBot/config.json"

    def __init__(self):
        with open(config_location) as config_file:
            config = json.load(config_file)

        self._currentUsers = []
        self._admin = config['admin']
        self._exitCode = config['exitCode']
        self._notifs = config['notifications']
        self.notifs['part']['body'] = self.notifs['part']['body'].replace('##CHANNEL##', config['channel'])
        self.notifs['join']['body'] = self.notifs['join']['body'].replace('##CHANNEL##', config['channel'])
        self._server = IRCServer(self)


    def user_left(self, user):
        if self._currentUsers.count(user) != 0:
            self._urrentUsers.remove(user)
             # Send desktop notification
             Util.notify(notifs['part']['title'], notifs['part']['body'].replace("##USER##", user))


    def user_joinned(self, user):
        if currentUsers.count(user) == 0 and user != self._admin:
            currentUsers.append(user)
             # Send desktop notification
             Util.notify(notifs['join']['title'], notifs['join']['body'].replace("##USER##", user))


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



# Run
watchdog = Watchdog()   
watchdog.run()
