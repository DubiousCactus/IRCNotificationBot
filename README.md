# Description
IRCNotificationBot is a very simple bot which purpose is to send desktop notifications when a user `JOIN` or `PART` a predefined channel. It runs as a Systemd service, it is extremely easy to install *and* uninstall, and offers some configuration parameters through a local config file. A whitelist can be used to limit which users will trigger notifications, and the notification messages can be entirely customized :) 

# Configuration
The configuration file is available at `~/.config/IRCNotificationBot/config`. Here is an example:

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
				"title": "",
				"body":  ""
			},
			"part": {
				"title": "",
				"body": ""
			}		
		}
	}


# Dependencies
This service does not require any modules other than the Python3 standard modules.

# Installation:

	curl -s https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/install.sh | bash

# Uninstallation:

	curl -s https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/uninstall.sh | bash

