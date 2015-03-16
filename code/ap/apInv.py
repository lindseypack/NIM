#!usr/bin/env python
from pysnmp.entity.rfc3413.oneliner import cmdgen
import shlex
import subprocess
import re
import os
import sys
import smtplib
from devices.models import AP as AccessPoint

## This file is used to update the access point inventory data. Use the
## updateAccessPoints function to run the update. The function
## updateStatus will only check if the APs are up or down, and send an
## email report on APs that are currently down or that have recovered.

## Do an snmpwalk using cmdgen from PySNMP to get data about each AP.
## Takes a dictionary of OIDs and a list of controller IPs.
def snmpwalk(OIDs, controllers):
    APs = dict()
    cmdGen = cmdgen.CommandGenerator()
    for key in OIDs:
        for controller in controllers:
            errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
                cmdgen.CommunityData('spa'),
                cmdgen.UdpTransportTarget((controller, 161)),
                0, 1000, OIDs[key]
            )
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    ## make a unique identifier for each AP
                    num = str(name)[len(OIDs["mac"]):].strip('.')
                    try:
                        if key not in APs[num]:
                            APs[num][key] = str(val.prettyPrint())
                    except:
                        APs[num] = {key: str(val.prettyPrint())}
    return APs

## Add or update all access points using Django.
def updateAccessPoints(path, AP_OIDs, controller_IPs):
    APs = snmpwalk(AP_OIDs, controller_IPs)
    for AP in APs:
        if APs[AP]["serial"] != "0":
            ## make a new AP object if necessary
            try:
                new_AP = AccessPoint(serialno=APs[AP]["serial"], ip=APs[AP]["ip"])
                new_AP.save()
            except:
                pass
            ## Update the AP's data
            update_AP = AccessPoint.objects.get(serialno=APs[AP]["serial"], autoupdate=1)
            update_AP.ip = APs[AP]["ip"]
            update_AP.mac = APs[AP]["mac"].lower()[2:]
            update_AP.name = APs[AP]["name"]
            update_AP.model = APs[AP]["model"]
            update_AP.save()

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
        upAPs.extend(runCommand(cmd))
    storedAPs = AccessPoint.objects.all()
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

#takes a string "com" and runs the command, returning a list of AP names
def runCommand(com):
    args = shlex.split(com) #separates com into indv. args
    p = subprocess.Popen(args, stdout=subprocess.PIPE) #runs command, saves stdout

    #communicate() returns a tuple (stdout,stderr) but we only want stdout
    stdout = p.communicate()[0]

    #clean the data
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
