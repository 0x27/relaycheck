#!/usr/bin/python2
# coding: utf-8
# relaytool: Check if relay is running, and restart relays.
# written in response to my fucking tor relays falling over.
# Author: Darren Martyn
# Version: 20150325.1
# BTC: 13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V
# TODO: Port to Ansible once I figure out how2ansible
# By default will use ~/.ssh/relay.key, un-passworded ssh key
# as I have yet to implement unwrapping logic in this script out
# of lack of time. Later I will fix this up to have a configuration
# option that will allow entering the password once and it "caches" the
# unwrapped key for the session, or something. I have to think this 
# over for obvious reasons to do with security :)
import paramiko
import json
import sys
import os

# colours
RED = "\x1b[1;31m"
GREEN = "\x1b[1;32m"
CLEAR = "\x1b[0m"
CYAN = "\x1b[1;36m"
BLUE = "\x1b[1;34m"
YELLOW = "\x1b[1;33m"

# A global variable or two go here...
DEFAULT_CONF_FILE = os.getenv("HOME")+"/.relaycheck.conf" # XXX: this is a filthy hack.
PRIVKEY = os.getenv("HOME")+"/.ssh/relay.key" # XXX: No password support on privkeys yet.
DEBUG = False

def msg_info(msg):
	print "%s{i} %s%s" %(CYAN, msg, CLEAR)

def msg_status(msg):
    print "%s{*} %s%s" %(BLUE, msg, CLEAR)

def msg_success(msg):
    print "%s{+} %s%s" %(GREEN, msg, CLEAR)

def msg_fail(msg):
	print "%s{!} %s%s" %(RED, msg, CLEAR)

def msg_debug(msg):
    if DEBUG == True:
        print "%s{>} %s%s" %(YELLOW, msg, CLEAR)
    else:
        pass

def exec_cmd(host, port, user, command):
	# execute a command, return outputz.
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(PRIVKEY)
    msg_debug("Connecting to %s:%s" %(host, port))
    ssh.connect(host, port=int(port), username=user, pkey=privkey)
    msg_debug("Executing %s" %(command))
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read()
    return output

def check_status_all(configuration):
    for host in configuration['hosts']:
        msg_status("Checking Tor Status on %s" %(host['relayname']))
        success = check_status(host=host['host'], port=host['port'], user=host['user'])
        if success == True:
            msg_success("Tor is running on %s" %(host['relayname']))
        else:
            msg_fail("Tor is NOT running on %s" %(host['relayname']))
    # have some counter here later...

def check_status(host, port, user):
    try:
        output = exec_cmd(host=host, port=port, user=user, command="service tor status")
    except Exception, e:
        msg_fail("Error in command execution. Printing stack trace and aborting...")
        print e
        sys.exit(0)
    if "tor is running" in output:
        return True
    else:
        return False

def restart_relays(configuration):
    for host in configuration['hosts']:
        msg_status("Restarting Tor on %s" %(host['relayname']))
        success = restart_relay(host=host['host'], port=host['port'], user=host['user'])
        if success == True:
            msg_success("Tor restarted successfully on %s" %(host['relayname']))
        else:
            msg_fail("Tor restart failure on %s" %(host['relayname']))
    # have some counter here later...

def restart_relay(host, port, user):
    try:
        output = exec_cmd(host=host, port=port, user=user, command="kill -HUP $(pidof tor) && ps aux | grep tor")
    except Exception, e:
        msg_fail("Error in command execution. Printing stack trace and aborting...")
        print e
        sys.exit(0)
    if "/usr/bin/tor" in output:
        return True
    else:
        return False

def main(args):
    if len(args) < 2:
        sys.exit("use: %s <status | restart> (optional config file)" %(args[0]))
    if len(args) > 2:
        msg_info("Using Configuration File: %s" %(args[2]))
        try:
            configuration = json.loads(open(args[2], "rb").read())
        except Exception, e:
            msg_fail("Error in configuration loading. Printing stack trace and aborting...")
            print e
            sys.exit(0)
    elif len(args) == 2:
        msg_info("Using Configuration File: %s" %(DEFAULT_CONF_FILE))
        try:
            configuration = json.loads(open(DEFAULT_CONF_FILE, "rb").read())
        except Exception, e:
            msg_fail("Error in configuration loading. Printing stack trace and aborting...")
            print e
            sys.exit(0)
    if args[1] == "status":
        check_status_all(configuration=configuration)
    elif args[1] == "restart":
        restart_relays(configuration=configuration)
    else:
        msg_fail("WTF? RTFM!")
        sys.exit(0)

if __name__ == "__main__":
    main(args=sys.argv)
#_EOF skyhighatrist (2015)
