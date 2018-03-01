#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 transpalette <transpalette@arch-cactus>
#
# Distributed under terms of the MIT license.

"""
Utility class
"""

import os

class Util:
    
    @staticmethod
    def notify(title, body):
        os.system("/usr/bin/notify-send '" + title + "' '" + body + "' -t 5000 --icon=img/irc_logo.png")


