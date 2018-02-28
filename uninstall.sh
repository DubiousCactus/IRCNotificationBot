#! /bin/sh
#
# uninstall.sh
# Copyright (C) 2018 transpalette <transpalette@translaptop>
#
# Distributed under terms of the MIT license.
#

rm -Rf ~/.config/IRCNotificationBot/
systemctl --user stop IRCNotificationBot.service
systemctl --user disable IRCNotificationBot.service
rm ~/.config/systemd/user/IRCNotificationBot.service

sudo rm -Rf /opt/IRCNotificationBot
