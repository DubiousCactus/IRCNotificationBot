#! /bin/sh
#
# install.sh
# Copyright (C) 2018 transpalette <transpalette@translaptop>
#
# Distributed under terms of the MIT license.
#


[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

mkdir /opt/irc_notifier
cd /opt/irc_notifier

wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/watchdog.py
wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/irc_notifier.service

mv irc_notifier.service /etc/systemd/system/
systemctl enable irc_notifier.service
systemctl start irc_notifier.service
