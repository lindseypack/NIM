#!usr/bin/env python
from pysnmp.entity.rfc3413.oneliner import cmdgen
import socket
import re
import subprocess
from devices.models import UPS

## This file is used to update the UPS inventory data. Use the updateUPS
## function to run the update.

## Do an snmpget using cmdgen from PySNMP to get data about each UPS.
## For APCs, return [serialno, model, mac addr, name].
## For Lieberts, return [serialno, model, mac addr, manufacture date].
def snmpget(ip, OIDs):
    cmdGen = cmdgen.CommandGenerator()

    data = dict()
    for key in OIDs:
        errorIndication, errorStatus, errorIndication, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('spa'),
            cmdgen.UdpTransportTarget((ip, 161)),
            OIDs[key]
        )
        data[key] = varBinds[0][1].prettyPrint()
    return data

## Pull IP addresses from file, add them to the database.
def importIPs(nd_ip, brand):
    IPs = [ip.strip() for ip in open(nd_ip)]
    for ip in IPs:
        if checkValidIP(ip):
            try:
                ups = UPS.objects.get(ip = ip, brand = brand)
            except:
                ups = UPS(ip = ip, brand = brand)
                ups.save()
    return IPs

## Make sure that an IP is still valid by pinging it.
def checkValidIP(ip):
    proc = subprocess.Popen(["ping " + ip + " -w 1"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    packetsBack = re.findall(r"(\d) received", out)[0]
    return packetsBack > '0'

## For each IP in the ups table, update the entry with the serialno,
## model, mac addr, name, and mf date (for Liebert UPSes).
# def updateUPS(APC_OIDs, Lie_OIDs):
def updateUPS(OIDs):
    UPSs = UPS.objects.all()
    for ups in UPSs:
        try:
            data = snmpget(ups.ip, OIDs[ups.brand])
            ups.serialno = data["serial"]
            ups.model = data["model"]
            ups.mac = data["mac"].lower()[2:]
            try:
                ups.name = data["name"]
            except:
                ups.name = socket.getfqdn(ups.ip).rstrip(".centre.edu")
            try:
                ups.mfdate = data["mfdate"]
            except:
                pass
            ups.save()
        except:
            print "Could not update", ups.ip

if __name__ == "__main__":
    # liebert_path = "/local_centre/network_inventory/code/ups/liebert_ip"
    # apc_path = "/local_centre/network_inventory/code/ups/apc_ip"
    # importIPs(liebert_path, "Liebert")
    # importIPs(apc_path, "APC")
    updateUPS()  ## update the ups table in the database


