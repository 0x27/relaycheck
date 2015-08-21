# relaycheck
Tool for checking the status and restarting my Tor relays

## What
This is a simple tool I developed in the morning to deal with the fact that 50% of my tor relays have fallen over in the past week, so I can quickly check their health and restart them 
periodically, along with check which version they are running. I am not a devops wizard or anything, but do intend to make this all ansible-y at some arbritary undefined date in the 
future when I can be bothered doing so or 
something.

## How to use
Firstly, set up your configuration file, as seen below. Now, I am using the root user in my examples, but if you have a special user like a "tor" user for restarting/managing tor, use 
that user. You can either set the config file as a commandline argument, or have it stored in ~/.relaycheck.conf where it will be automatically loaded if none is specified :)

There are only four possible commands at the moment. "status", which checks crudely if tor is running by issuing 'service tor status' command, and "restart" which kill -HUP's the tor 
process in order to restart it, then checks the process list to ensure tor is still there and has not fucked off or anything. There is also "version", which checks the version of the 
tor software on the relay, and "start" which starts the tor software if it has died. I have to make this more efficient later, but for some 
reason restarting with "service tor restart" didn't like being scripted.

## Commands
* status - returns if the relay in question is online or offline
* restart - restarts a relays tor instance (kill -HUP)
* start - starts a tor relay on an instance (service tor start)
* version - returns the version of Tor running on the host

## JSON Configuration File  
The JSON configuration file is incredibly simple. "example.json" included is an example one to use. The format is outlined below.  

```
{
    "hosts":[
            {
            "user": "root",
            "port": "22",
            "host": "127.0.0.1",
            "relayname": "Example"
        },
        {
            "user": "root",
            "port": "23",
            "host": "127.0.0.2",
            "relayname": "Example2"
        }
    ]
}
```
In "hosts" we define the hosts we want to be connecting to. Each host has 4 options: user, port, host, and relayname. The relayname is... Because I identify my relays by their name. 
Host, Port, and User are so SSH can access them. Fairly simples, eh? Its valid JSON, so you can use a JSON linter or somesuch to check if you got it right. I use [this one 
here][jsonlinter].

## Demo  
Check out the Asciicast demo!  
[![asciicast](https://asciinema.org/a/17999.png)](https://asciinema.org/a/17999)

## Licence  
Licenced under the [WTFPL][wtfpl], the only truly free licence so do whatever the fuck you like ;)

## Beer?  
If you want, send beermoniez to [13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V](bitcoin:13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V)

## Screenshots
Here we have a screenshot of the version checker.  
![Version Check](https://raw.githubusercontent.com/0x27/relaycheck/master/screenshots/screenshot-versioncheck-20150326.png)

Here we have a screenshot of the status checker.  
![Status Check](https://raw.githubusercontent.com/0x27/relaycheck/master/screenshots/screenshot-statuscheck-20150326.png)

## Bugs
Use the issue tracker. Github provides these things for a reason :)

## Awful Kludges
Ok, so I was not bothered with having some passwordprotected privkey handling so you need to add a key named .ssh/relay.key to the hosts authorized keys file. You can change this if 
you want, but I strongly advice not using password auth on SSH for obvious reasons. Stick with privkeys, its safer there. I will eventually work out an elegant solution to cache the 
privkey somehow after decrypting it with a password but cannot be bothered right now :)

## Roadmap
Next features to add include better SSH key/pass handling (as per "Awful Kludges"), automatic logfile downloading/saving, and possibly integration with Stem to do useful stuff like 
checking how much traffic has been passed through the relay, its speed, uptime, etc.

## Dependencies
Relies on python-paramiko, the rest should be standard python libs. Only written for Python2, as I cannot be bothered retooling my stuff for Python3 :P

## Contact
If for some arbritary reason you want to contact me, see [my contact details and stuff][contact].

## Changes
26-03-2015: Added 'start' command to start tor relays if they are down.  
26-03-2015: Added 'version' command to check tor versions that are running.

## Todo
* Python3 support/fork (oh god oh god)
* Port to Ansible
* Add deployment commands and the like
* ?????
* profit?

[jsonlinter]: http://jsonformatter.curiousconcept.com/
[asciinema]: https://asciinema.org/a/17999
[wtfpl]: http://wtfpl.net
[bitcoin:13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V]: bitcoin:13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V
[contact]: http://0x27.me/about/
