#! /bin/sh
#
# update.sh
# Copyright (C) 2018 transpalette <transpalette@arch-cactus>
#
# Distributed under terms of the MIT license.
#


if [ "$(whoami)" == "root" ]; then
   	echo "[!] Don't run this installer as root you fool !"
   	exit 1;
fi

echo "[*] Stopping the service"
systemctl --user stop IRCNotificationBot.service

echo "[*] Removing previous version"
sudo rm -rf /opt/IRCNotificationBot/bin/*
cd /opt/IRCNotificationBot/bin

echo "[*] Downloading the service script from GitHub"
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/bin/__init__.py
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/bin/server.py
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/bin/utils.py
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/bin/watchdog.py
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/bin/img/irc_logo.png

sudo mkdir img
sudo mv irc_logo.png img/

echo "[*] Giving execution rights to the script"
sudo chmod 775 watchdog.py

echo "[*] Restarting the systemd service"
systemctl --user start IRCNotificationBot.service
