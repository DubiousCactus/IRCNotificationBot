! /bin/sh
#
# install.sh
# Copyright (C) 2018 transpalette <transpalette@translaptop>
#
# Distributed under terms of the MIT license.
#

mkdir -p ~/.config/IRCNotificationBot/
cd ~/.config/IRCNotificationBot
wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/config.json

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

mkdir /opt/IRCNotificationBot
cd /opt/IRCNotificationBot

wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/watchdog.py
wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/IRCNotificationBot.service

chmod +x watchdog.py
mv IRCNotificationBot.service /etc/systemd/system/
systemctl enable IRCNotificationBot.service
systemctl start IRCNotificationBot.service
