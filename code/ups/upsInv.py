#!usr/bin/env python
from pysnmp.entity.rfc3413.oneliner import cmdgen
import socket
import re
import subprocess
from devices.models import UPS

## Do an snmpget using cmdgen from PySNMP to get data about each UPS.
## For APCs, return [serialno, model, mac addr, name].
## For Lieberts, return [serialno, model, mac addr, manufacture date].
def snmpget(ip, brand, APC_OIDs, Liebert_OIDs):
    cmdGen = cmdgen.CommandGenerator()

    if brand == "APC":
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('spa'),
            cmdgen.UdpTransportTarget((ip, 161)),
            APC_OIDs[0], APC_OIDs[1], APC_OIDs[2], APC_OIDs[3]
            ## serial, model, mac, name
        )
    else:
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('spa'),
            cmdgen.UdpTransportTarget((ip, 161)),
            Liebert_OIDs[0], Liebert_OIDs[1], Liebert_OIDs[2], Liebert_OIDs[3]
            ## serial, model, mac, manufacture date
        )

    vals = list()

    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?'
                )
            )
        else:
            for name, val in varBinds:
                vals.append(val.prettyPrint())
    vals[2] = vals[2].lstrip('0x').upper()
    return vals

## Pull ip addresses from file, add them to the database.
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

def checkValidIP(ip):
    proc = subprocess.Popen(["ping " + ip + " -w 1"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    packetsBack = re.findall(r"(\d) received", out)[0]
    return packetsBack > '0'

## For each IP in the ups table, update the entry with the serialno,
## model, mac addr, name, and mf date (for Liebert UPSes).
def updateUPS(APC_OIDs, Lie_OIDs):
    UPSs = UPS.objects.all()
    for ups in UPSs:
        try:
            data = snmpget(ups.ip, ups.brand, APC_OIDs, Lie_OIDs)
            ups.serialno = data[0]
            ups.model = data[1]
            ups.mac = data[2]
            if ups.brand == "APC":
                ups.name = data[3]
            else:
                ups.name = socket.getfqdn(ups.ip).rstrip(".centre.edu")
                ups.mfdate = data[3]
            ups.save()
        except:
            print "Could not update", ups.ip


if __name__ == "__main__":
    # liebert_path = "/local_centre/network_inventory/code/ups/liebert_ip"
    # apc_path = "/local_centre/network_inventory/code/ups/apc_ip"
    # importIPs(liebert_path, "Liebert")
    # importIPs(apc_path, "APC")
    updateUPS()  ## update the ups table in the database


