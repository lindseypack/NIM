#!usr/bin/env python
from pysnmp.entity.rfc3413.oneliner import cmdgen
import shlex
import subprocess
import re
import os
import sys
import smtplib
from devices.models import AP

## This file is used to update the access point inventory data. Use the
## updateAccessPoints function to run the update. The function
## updateStatus will only check if the APs are up or down, and send an
## email report on APs that are currently down or that have recovered.

## Do an snmpwalk using cmdgen from PySNMP to get data about each AP.
def snmpwalk(mac, name, IPs, serialno, model, controllers):
    APs = dict()
    cmdGen = cmdgen.CommandGenerator()

    oids = [name, IPs, mac, serialno, model]

    for i in range(len(oids)):
        for controller in controllers:
            errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
                cmdgen.CommunityData('spa'),
                cmdgen.UdpTransportTarget((controller, 161)),
                0, 1000, oids[i]
            )

            if errorIndication:
                print(errorIndication)
            else:
                if errorStatus:
                    print('%s at %s' % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                        )
                    )
                else:
                    for varBindTableRow in varBindTable:
                        for name, val in varBindTableRow:
                            num = str(name)[len(mac):].strip('.')
                            try:
                                if len(APs[num]) == i:
                                    APs[num].append(str(val.prettyPrint()))
                            except:
                                APs[num] = [str(val.prettyPrint())]
    return APs


#takes a string "com" and runs the command, returning a list of AP names
def runCom(com):
    args = shlex.split(com) #separates com into indv. args
    p = subprocess.Popen(args,stdout=subprocess.PIPE) #runs command, saves stdout

    #communicate() returns a tuple (stdout,stderr)
    #but we only want stdout
    stdout = p.communicate()[0]

    #clean the data (remove un-necessary crap)
    stdout = stdout.replace("SNMPv2-SMI::enterprises.","")
    stdout = stdout.replace("Hex-STRING:","")
    stdout = stdout.replace("STRING:","")
    stdout = stdout.replace("IpAddress:","")
    stdout = stdout.replace("\"", "")
    stdout = stdout.replace(" ", "")

    #split stdout into lines
    stdoutLines = stdout.split("\n")
    stdoutLines = stdoutLines[:-1] #removes last empty row

    #parse stdout into list
    names = []
    for line in stdoutLines:
        names.append(line.split("=")[1])

    return names


## Add or update all access points using Django.
def updateAccessPoints(path, AP_OIDs, controller_IPs):
    mac_oid = AP_OIDs[0]
    name_oid = AP_OIDs[1]
    IP_oid = AP_OIDs[2]
    serialno_oid = AP_OIDs[3]
    model_oid = AP_OIDs[4]
    status_oid = AP_OIDs[5]

    AccessPoints = snmpwalk(mac_oid, name_oid, IP_oid, serialno_oid, model_oid, controller_IPs)
    # AccessPoints = [[name, IPs, mac, serialno, model], ...]

    for AccessPoint in AccessPoints:
        serial = AccessPoints[AccessPoint][3]
        if serial != "0":
            name = AccessPoints[AccessPoint][0]
            ip = AccessPoints[AccessPoint][1]
            mac = AccessPoints[AccessPoint][2].lstrip('0').lstrip('x')
            model = AccessPoints[AccessPoint][4]
            try:
                update_AccessPoint = AP(serialno=serial, ip=ip)
                update_AccessPoint.save()
            except:
                pass

            update_AccessPoint = AP.objects.get(serialno=serial, autoupdate=1)
            update_AccessPoint.ip = ip
            update_AccessPoint.mac = mac
            update_AccessPoint.name = name
            update_AccessPoint.model = model

            update_AccessPoint.save()

    updateStatus(controller_IPs, status_oid)


## Get the names of all the access points which are currently up and connected to
## a controller. Compare to the names in the database to find the APs that are down.
def updateStatus(controller_IPs, status_oid, email):
    AP_command = []
    for controller in controller_IPs:
        AP_command.append("snmpwalk -v2c -c spa " + controller + " " + status_oid)

    # Get the names of the APs connected to each controller.
    # Compare to APs stored in the database to determine which are down and
    # which have recovered.
    upAPs = []
    for cmd in AP_command:
        upAPs.extend(runCom(cmd))
    storedAPs = AP.objects.all()
    downAPs = []
    recoveredAPs = []
    for ap in storedAPs:
        if ap.name not in upAPs:
            ap.laststatus = "down"
            if ap.checkstatus == True:
                downAPs.append(ap)
        else:
            if ap.laststatus == "down" and ap.checkstatus == True:
                recoveredAPs.append(ap)
            ap.laststatus = "up"
        ap.save()

    # Send emails about down or recovered access points.
    if len(downAPs) > 0:
        message = '\nThe following access points are not responding:\n'
        subject = 'APs are not responding'
        sendEmail(message, subject, downAPs, email)
    if len(recoveredAPs) > 0:
        message = '\nThe following access points were down but have recovered:\n'
        subject = 'APs have recovered'
        sendEmail(message, subject, recoveredAPs, email)

## Send an email report on access point status.
def sendEmail(messageBody, subject, APs, email):
    for ap in APs:
        messageBody += "\t" + ap.ip + "\t" + ap.name + "\n"
    toHeaderBuild = []
    for to in email["to"]:
        toHeaderBuild.append("<" + to + ">")
    msg = "From: <" + email["from"] + "> \nTo: " + ', '.join(toHeaderBuild) + " \nSubject: " + subject + " \n" + messageBody
    s = smtplib.SMTP(email["server"])
    s.sendmail(email["from"], email["to"], msg)
    s.quit()
