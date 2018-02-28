#! /bin/sh
#
# install.sh
# Copyright (C) 2018 transpalette <transpalette@translaptop>
#
# Distributed under terms of the MIT license.
#


[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

mkdir /opt/IRCNotificationBot
cd /opt/IRCNotificationBot

wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/watchdog.py
wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/IRCNotificationBot.service
wget https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/config.json

chmod +x watchdog.py
mkdir -p ~/.config/IRCNotificationBot/
cp config.json ~/.config/IRCNotificationBot/
mv IRCNotificationBot.service /etc/systemd/system/
systemctl enable IRCNotificationBot.service
systemctl start IRCNotificationBot.service
