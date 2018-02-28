#! /bin/sh
#
# install.sh
# Copyright (C) 2018 transpalette <transpalette@translaptop>
#
# Distributed under terms of the MIT license.
#


mkdir ~/.irc_notifier && cd ~/.irc_notifier
wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/watchdog.py .
wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/irc_notifier.service
mv irc_notifier.service /etc/sysctl.d/
systemctl enable irc_notifier.service

