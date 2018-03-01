#! /bin/sh
#
# install.sh
# Copyright (C) 2018 transpalette <transpalette@translaptop>
#
# Distributed under terms of the MIT license.
#

if [ "$(whoami)" == "root" ]; then
   	echo "[!] Don't run this installer as root you fool !"
   	exit 1;
fi

echo "[*] Creating ~/.config/IRCNotificationBot"
mkdir -p ~/.config/IRCNotificationBot/
cd ~/.config/IRCNotificationBot
echo "[*] Downloading config.json from GitHub"
wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/config.json

echo "[*] Downloading systemd service file from GitHub"
mkdir -p ~/.config/systemd/user
cd ~/.config/systemd/user/
wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/IRCNotificationBot.service

echo "[*] Creating /opt/IRCNotificationBot"
sudo mkdir /opt/IRCNotificationBot
cd /opt/IRCNotificationBot

echo "[*] Downloading the service script from GitHub"
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/src/__init__.py
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/src/server.py
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/src/utils.py
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/src/watchdog.py
sudo wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/src/img/irc_logo.png

sudo mkdir img
sudo mv irc_logo.png img/

echo "[*] Giving execution rights to the script"
sudo chmod 775 watchdog.py

echo "[*] Enabling the systemd service"
# Enable the systemd service
systemctl --user enable IRCNotificationBot.service
systemctl --user start IRCNotificationBot.service
