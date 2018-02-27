#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 transpalette <transpalette@arch-cactus>
#
# Distributed under terms of the MIT license.

from irc import IRCBot, run_bot

class GreeterBot(IRCBot):
    def greet(self, nick, message, channel):
        print "greeting"
        return 'What have you been up to %s ?' % nick

    def log(self, sender, message, channel):
        print('%s sent %s' % (sender, message))

    def command_patterns(self):
        return (
            self.ping('^hello', self.greet),
            ('.*', self.log)
        )

host = 'irc.freenode.net'
port = 6667
nick = 'Cyborg-Theo-9000'

run_bot(GreeterBot, host, port, nick, ['#subseven'])
