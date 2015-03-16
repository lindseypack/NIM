#!usr/bin/env python
""" UpdateDevices.py

This program controls several other Python scripts that each update the inventory
information for a network device. Currently supported devices are access points,
switches, APC or Liebert UPSes, and phones using VOIP.

Uses a configuration file for information about device logins, OIDs, IP addresses,
and so on.

Usage: UpdateDevices.py [-h] [-a] [-e] [-s] [-u] [-p]

Optional arguments:
  -h, --help         show a help message and exit
  -a, --accesspoint  update access points
  -e, --apstatus     update access point status and send notification email
  -s, --switch       update switches
  -u, --ups          update UPSes
  -p, --phone        update phones

Running with no arguments will attempt to update all devices.
"""

import sys
import os
import re
import argparse
import logging
import datetime
import deviceconfig as config

path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
logPath = os.path.join(path, "log")
logging.basicConfig(filename=logPath)

def updateAP():
    """ This function reads necessary information from a config file, then
    calls the updateAccessPoints function in apInv.py.
    """
    try:
        from ap import apInv
        print "Updating access points..."
        apInv.updateAccessPoints(path, config.AP_OIDs, config.AP_ControllerIPs)
    except:
        msg = "========================================================\n"\
            + str(datetime.datetime.today()) + "\n"\
            + "Could not update access points:\n\n"
        logging.exception(msg)
        print "Could not update access points. See", logPath, "for details."

def updateAPStatus():
    """ This function reads necessary information from a config file, then
    calls the updateStatus function in apInv.py.
    """
    try:
        from ap import apInv
        print "Updating access point status..."
        apInv.updateStatus(config.AP_ControllerIPs, config.AP_Status_OID,
                           config.AP_Email)
    except:
        msg = "========================================================\n"\
            + str(datetime.datetime.today()) + "\n"\
            + "Could not update access points:\n\n"
        logging.exception(msg)
        print "Could not update access point status. See", logPath, "for details."

def updateSwitch(switch_IPs = []):
    """ This function reads necessary information from a config file, then
    calls the updateSwitches function in switchInv.py.
    """
    try:
        from switch import switchInv
        print "Updating switches..."
        switchInv.updateSwitches(config.Switch_Login, config.Switch_IPs)
    except:
        msg = "========================================================\n"\
            + str(datetime.datetime.today()) + "\n"\
            + "Could not update switches:\n\n"
        logging.exception(msg)
        print "Could not update switches. See", logPath, "for details."

def updateUPS():
    """ This function reads necessary information from a config file, then
    calls the updateUPS function in upsInv.py.
    """
    try:
        from ups import upsInv
        print "Updating UPSes..."
        upsInv.updateUPS(config.UPS_OIDs)
    except:
        msg = "========================================================\n"\
            + str(datetime.datetime.today()) + "\n"\
            + "Could not update UPSes:\n\n"
        logging.exception(msg)
        print "Could not update UPSes. See", logPath, "for details."

def updatePhone():
    """ This function reads necessary information from a config file, then
    calls the updatePhones function in phoneInv.py.
    """
    try:
        from phone import phoneInv
        print "Updating phones..."
        phoneInv.updatePhones(path, config.Phone_Login)
    except:
        msg = "========================================================\n"\
            + str(datetime.datetime.today()) + "\n"\
            + "Could not update phones:\n\n"
        logging.exception(msg)
        print "Could not update phones. See", logPath, "for details."


if __name__ == "__main__":
    import django
    sys.path.append(os.path.abspath(path))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "network_inventory.settings")
    django.setup()

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--accesspoint", help="update access points", action="store_true")
    parser.add_argument("-e", "--apstatus", help="check AP status and send notification email", action="store_true")
    parser.add_argument("-s", "--switch", help="update switches", action="store_true")
    parser.add_argument("-u", "--ups", help="update UPSes", action="store_true")
    parser.add_argument("-p", "--phone", help="update phones", action="store_true")
    args = parser.parse_args()

    if args.accesspoint:
        updateAP()
        updateAPStatus()
    if args.apstatus:
        updateAPStatus()
    if args.switch:
        updateSwitch()
    if args.ups:
        updateUPS()
    if args.phone:
        updatePhone()

    if not args.apstatus and not args.accesspoint and not args.switch \
            and not args.ups and not args.phone:
        updateAP()
        updateAPStatus()
        updateSwitch()
        updateUPS()
        updatePhone()
