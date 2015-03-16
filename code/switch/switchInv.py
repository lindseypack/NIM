#!usr/bin/env/python
import re
import socket
import sys
import os
import subprocess
from Exscript import Account, Host
from Exscript.util.interact import read_login
from Exscript.protocols import SSH2, Telnet
from devices.models import Switch

## This file is used to update the switch inventory data. Use the
## updateSwitches function to run the update.

## use this to import a bunch of IPs into the database from a file
def importIPs(IPFile):
    with open(IPFile) as f:
        IPs = [ip.strip() for ip in f]
        for ip in IPs:
            if testActive(ip):
                switch = Switch(ip = ip)
                switch.save()
            else:
                print ip, "is not active"

## Test if an IP address actually exists
def testActive(ip):
    proc = subprocess.Popen(["ping " + ip + " -w 1"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    packetsBack = re.findall(r"(\d) received", out)[0]
    return packetsBack > '0'

## Function to map IP address to host name. Returns dictionary.
def lookup(IPs):
    addrBook = dict()
    for addr in IPs:
        try:
            addrBook[addr] = socket.gethostbyaddr(addr)[0].rstrip('.centre.edu').lower()
        except socket.herror:
            print "dns lookup failed on", addr
    return addrBook

def showVer(ip, login):
    acct = Account(login[0], login[1])
    conn = SSH2()
    conn.connect(ip)
    conn.set_driver('ios')
    conn.authenticate(acct)  # Authenticate on the remote host
    conn.execute('terminal length 0')   # Set terminal length
    conn.execute('show ver')
    response = repr(conn.response)
    conn.send('exit\r')     # Send the "exit" command
    conn.close()
    return response

## use ssh or telnet to run the "show ver" command on every switch.
## return the data as a dictionary: {'ip':'show ver result', ...}
def getShowVerData(IPs, login):
    acct = Account(login[0], login[1])
    showver = dict()
    for i in range(4):
        failed = []
        for ip in IPs:
            try:
                showver[ip] = showVer(ip, login)
            except:
                failed.append(ip)
        IPs = failed
    return showver

## extract useful info from the showver data using regular expressions.
## return a list of switches: [(serialno, ip, name, mac, model, swVer, uptime, stack, purchaseyr), ...]
## and a list of ip addresses that failed the REs.
def parseShowVer(showver):
    addrBook = lookup(showver)  ## use to get names for each switch
    switches = list()
    failed = list()  ## need to know if regexes fail for a given switch - this shouldn't happen

    ## REs
    serialRE = re.compile(r'System serial number\s*: (.+?)\\r\\n')
    macRE = re.compile(r'Base ethernet MAC Address\s*: (.+?)\\r\\n')
    modelRE = re.compile(r'Model number\s*: (.+?)\\r\\n')
    swVerRE = re.compile(r'Version (.+?), RELEASE SOFTWARE')
    upRE = re.compile(r'uptime is (.+?)\\r\\n')
    masterRE = re.compile(r'\*    (\d)')    ## for stacks, use to tell which switch is the master

    for ip in showver:
        name = addrBook[ip]
        data = showver[ip]
        try:
            if name.find('stack') >= 0:  ## stack
                ## count how many switches
                start = data.find('Switch Ports Model              SW Version            SW Image')
                end = data.find('Switch 0')
                stackSize = data[start:end].count('\\r\\n') - 4

                master = masterRE.findall(data)[0] ## which is the master switch
                for i in range(1, stackSize + 1):
                    model = re.findall(r'SW Image.+?' + str(i) + '\s+\d+\s+(.+?)\s', data)[0]
                    swVer = re.findall(r'SW Image.+?' + str(i) + '\s+\d+\s+.+?\s+(.+?)\s', data)[0]

                    if (str(i) == master):
                        uptime = upRE.findall(data)[0]
                        mac = macRE.findall(data)[0]
                        serial = serialRE.findall(data)[0]
                    else:
                        uptime = re.findall(r'Switch 0' + str(i) + r'.+?Switch Uptime\s*: (.+?)\\r\\n', data)[0]
                        mac = re.findall(r'Switch 0' + str(i) + r'.+?Base ethernet MAC Address\s*: (.+?)\\r\\n', data)[0]
                        serial = re.findall(r'Switch 0' + str(i) + r'.+?System serial number\s*: (.+?)\\r\\n', data)[0]
                    purchaseyr = int(serial[3:5]) + 1996
                    switches.append({
                        "serial": serial,
                        "ip": ip,
                        "name": name.rstrip('.centre.edu'),
                        "mac": mac.replace(":", "").lower(),
                        "model": model,
                        "swver": swVer,
                        "uptime": uptime,
                        "stack": i,
                        "purchaseyr": purchaseyr,
                    })

            else:  ## switch
                swVer = swVerRE.findall(data)[0].strip()
                uptime = upRE.findall(data)[0].strip()
                mac = macRE.findall(data)[0].strip()
                model = modelRE.findall(data)[0].strip()
                serial = serialRE.findall(data)[0].strip()
                purchaseyr = int(serial[3:5]) + 1996
                # switches.append((serial, ip, name.rstrip('.centre.edu'),
                #     mac.replace(":", ""), model, swVer, uptime, 0, purchaseyr))
                switches.append({
                    "serial": serial,
                    "ip": ip,
                    "name": name.rstrip('.centre.edu'),
                    "mac": mac.replace(":", "").lower(),
                    "model": model,
                    "swver": swVer,
                    "uptime": uptime,
                    "stack": 0,
                    "purchaseyr": purchaseyr,
                })
        except:
            failed.append(ip)

    return switches, failed

## if a switch x has been replaced with y, y will have the same IP x has in the
## database. So if a switch from showver has the same IP as a different switch
## in the db, the switch in the db has been replaced and its info should be
## updated to reflect this.
def checkReplaced(switches):
    newSwitches = [switch["serial"] for switch in switches]  ## serialno, ip
    oldSwitchObjs = Switch.objects.exclude(ip='0.0.0.0').exclude(autoupdate=False)
    oldSwitches = [switch.serialno.encode('ascii', 'ignore') for switch in oldSwitchObjs]
    replaced =  list()
    for old in oldSwitches:
        if (old != "") and (old not in newSwitches):
            replaced.append(old)
    return replaced

## extract specific info from showver data for each IP address in the table
def updateSwitches(switchlogin, IPs = []):
    # importIPs('/local_centre/NIM/code/switch/switch_ip')

    if (IPs == []):
        ## get IPs from db
        switchObjs = Switch.objects.exclude(ip='0.0.0.0').exclude(autoupdate=False)
        IPs = [switch.ip for switch in switchObjs]

    ## get & parse info about each switch
    showver = getShowVerData(IPs, switchlogin)
    switches, failed = parseShowVer(showver)

    if len(failed) > 0:
        print "Could not parse show ver data for these switches: ", failed

    if len(IPs) > 1:
        replaced = checkReplaced(switches)  # list of serials

        for r in replaced:
            switch = Switch.objects.get(serialno=r)
            switch.ip = '0.0.0.0'
            switch.status = 'inactive'
            switch.uptime = ''
            switch.save()

    for s in switches:
        switch = Switch()
        try:
            switch = Switch.objects.get(serialno = s["serial"])
        except:
            try:
                switch = Switch.objects.get(ip = s["ip"])
                switch.serialno = s["serial"]
            except:
                switch.serialno = s["serial"]

        switch.ip = s["ip"]
        switch.name = s["name"]
        switch.mac = s["mac"]
        switch.model = s["model"]
        switch.softwarever = s["swver"]
        switch.uptime = s["uptime"]
        switch.stack = s["stack"]
        switch.purchaseyr = s["purchaseyr"]
        switch.status = 'active'
        switch.save()
