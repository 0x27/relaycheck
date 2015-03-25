# relaycheck
Tool for checking the status and restarting my Tor relays

## What
This is a simple tool I developed in the morning to deal with the fact that 50% of my tor relays have fallen over in the past week, so I can quickly check their health and restart them 
periodically. I am not a devops wizard or anything, but do intend to make this all ansible-y at some arbritary undefined date in the future when I can be bothered doing so or 
something.

## How to use
Firstly, set up your configuration file, as seen below. Now, I am using the root user in my examples, but if you have a special user like a "tor" user for restarting/managing tor, use 
that user. You can either set the config file as a commandline argument, or have it stored in ~/.relaycheck.conf where it will be automatically loaded if none is specified :)

There are only two possible commands at the moment. "status", which checks crudely if tor is running by issuing 'service tor status' command, and "restart" which kill -HUP's the tor 
process in order to restart it, then checks the process list to ensure tor is still there and has not fucked off or anything. I have to make this more efficient later, but for some 
reason restarting with "service tor restart" didn't like being scripted.

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
Check out the [Elite As Fuck AsciiCast Demo!][asciinema]

## Licence  
Licenced under the [WTFPL][wtfpl], the only truly free licence so do whatever the fuck you like ;)

## Beer?  
If you want, send beermoniez to [13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V][bitcoin:13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V]


[jsonlinter]: http://jsonformatter.curiousconcept.com/
[asciinema]: https://asciinema.org/a/17999
[wtfpl]: http://wtfpl.net
[bitcoin:13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V]: bitcoin:13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V
