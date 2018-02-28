# Description
IRCNotificationBot is a very simple bot which purpose is to send desktop notifications when a user `JOIN` or `PART` a predefined channel. It runs as a Systemd service, it is extremely easy to install *and* uninstall, and offers some configuration parameters through a local config file. A whitelist can be used to limit which users will trigger notifications, and the notification messages can be entirely customized :) 

# Usage
Simply start the service via systemd if it is not running already, and you should get a first notification indicating that the bot successfuly joinned your channel. You can configure the bot however you want, as shown in the section below. If you modify the configuration, simply restart the service :)

# Configuration
The configuration file is available at `~/.config/IRCNotificationBot/config.json`. Here is an example:

	{
		"server": "chat.freenode.net",
		"port": 6667,
		"channel": "#github",
		"receiveTimeout": 2,
		"botName": "Cyber-Bot-9000",
		"admin": "johncena",
		"exitCode" : "die bitch!",
		"usesWhitelist": false,
		"whitelist": [
			"user1",
			"user2",
			"user3"
		],
		"notifications": {
			"join": {
				"title": "IRC Notification",
				"body": "##USER## joinned the channel ##CHANNEL##"
			},
			"part": {
				"title": "IRC Notification",
				"body": "##USER## has left the channel ##CHANNEL##"
			}	
		}
	}


# Dependencies
This service does not require any modules other than the Python3 standard modules.

# Installation
## Automatic installation
Simply run the following command (if you don't trust me, and you shouldn't, just read through the install script, it is commented and pretty straight-forward):

	curl -s https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/install.sh | bash

## Manual installation
The script can be used on its own, as long as you move the `config.json` to `~/.config/IRCNotificationBot/`. You can just run it as an executable script, or by passing it to Python3:
	./watchdog.py
or
	python3 watchdog.py

However, if you want it to run at boot time as a service, you can simply move the `IRCNotificationBot.service` to `~/.config/systemd/user/`, and then run `systemctl --user enable IRCNotification.service` to enable it (it will then start on boot). Don't forget to append `--user` to systemctl, because the service runs in user mode ;)

# Uninstallation
## Automatic uninstallation
Simply run the following command (if you don't trust me, and you shouldn't, just read through the uninstall script, it is commented and pretty straight-forward):

	curl -s https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/uninstall.sh | bash && echo 'Good riddance !'

## Manual uninstallation
* Disable the service: `systemctl --user disable IRCNotificationBot.service`
* Delete the service: `rm ~/.config/systemd/user/IRCNotificationBot.service`
* Delete the bot and the config: `rm -rf /opt/IRCNotificationBot && rm -rf ~/.config/IRCNotificationBot`
