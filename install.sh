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
wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/IRCNotificationBot.service
echo "[*] Setting the User parameter of the service"
# Set User=$(whoami) in the service file (so that it doesn't run as root and can access the user's home dir)
sed "s/##USER##/$(whoami)/g" IRCNotificationBot.service > IRCNotificationBot.service.tmp && mv IRCNotificationBot.service.tmp IRCNotificationBot.service

echo "[*] Asking for root priviledges to enable the service"
# Become root if not already
[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

mv IRCNotificationBot.service /usr/lib/systemd/system/

echo "[*] Creating /opt/IRCNotificationBot"
mkdir /opt/IRCNotificationBot
cd /opt/IRCNotificationBot

echo "[*] Downloading the service script from GitHub"
wget --quiet https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/watchdog.py

echo "[*] Giving execution rights to the script"
chmod +x watchdog.py

echo "[*] Enabling the systemd service"
# Enable the systemd service
systemctl enable IRCNotificationBot.service
systemctl start IRCNotificationBot.service
