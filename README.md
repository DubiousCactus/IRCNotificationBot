# Description
IRCNotificationBot is a very simple bot which purpose is to send desktop notifications when a user JOIN or PART a predefined channel. It runs as a Systemd service, it is extremely easy to install, and offers some configuration parameters through a local config file. 

# Configuration
The configuration file is available at `~/.config/IRCNotificationBot/config`. Here is an example:
``
[
	"server": "chat.freenode.net",
	"port": 6667,
	"channel": "#github",
	"receiveTimeout": 2,
	"botName": "Cyber-Bot-9000",
	"admin": "johncena",
	"exiteCode" : "die bitch!",
	"usesWhitelist": false,
	"whitelist": {
		"user1",
		"user2",
		"user3"
	}
]
``

# Dependencies
This service does not require any modules other than the Python3 standard modules.

# Installation:

	curl -s https://raw.githubusercontent.com/M4gicT0/IRCNotificationBot/master/install.sh | bash
