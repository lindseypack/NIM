import sys
import os
import re
import argparse

def updateAP():
    from ap import apInv
    print "Updating access points..."

    with open("config") as f:
        config = f.read()
        path = re.findall(r'path = (.+?)\n', config)[0]
        ap_mac = re.findall(r'AP_MAC_OID = (.+?)\n', config)[0]
        ap_name = re.findall(r'AP_Name_OID = (.+?)\n', config)[0]
        ap_ip = re.findall(r'AP_IP_OID = (.+?)\n', config)[0]
        ap_serial = re.findall(r'AP_Serial_OID = (.+?)\n', config)[0]
        ap_model = re.findall(r'AP_Model_OID = (.+?)\n', config)[0]
        ap_status = re.findall(r'AP_Status_OID = (.+?)\n', config)[0]
        ap_controllers = re.findall(r'AP_ControllerIPs = \[(.+?)\]', config)[0].split(",")

    apInv.updateAccessPoints(path, ap_oids, ap_controllers)

def updateSwitch():
    from switch import switchInv
    print "Updating switches..."

    with open("config") as f:
        config = f.read()
        switch_login = re.findall(r'Switch_Login = \[(.+?)\]', config)[0].split(",")
        switch_IPs = re.findall(r'Switch_IPs = \[(.+?)\]', config)[0].split(",")

    switchInv.updateSwitches(switch_login, switch_IPs)

def updateUPS():
    from ups import upsInv
    print "Updating UPSes..."

    with open("config") as f:
        config = f.read()
        apc_serial = re.findall(r'APC_Serial_OID = (.+?)\n', config)[0]
        apc_model = re.findall(r'APC_Model_OID = (.+?)\n', config)[0]
        apc_mac = re.findall(r'APC_MAC_OID = (.+?)\n', config)[0]
        apc_name = re.findall(r'APC_Name_OID = (.+?)\n', config)[0]
        apc_oids = [apc_serial, apc_model, apc_mac, apc_name]
        lie_serial = re.findall(r'Liebert_Serial_OID = (.+?)\n', config)[0]
        lie_model = re.findall(r'Liebert_Model_OID = (.+?)\n', config)[0]
        lie_mac = re.findall(r'Liebert_MAC_OID = (.+?)\n', config)[0]
        lie_mfdate = re.findall(r'Liebert_MfDate_OID = (.+?)\n', config)[0]
        liebert_oids = [lie_serial, lie_model, lie_mac, lie_mfdate]

    upsInv.updateUPS(apc_oids, liebert_oids)

def updatePhone():
    from phone import phoneInv
    print "Updating phones..."

    with open("config") as f:
        config = f.read()
        path = re.findall(r'path = (.+?)\n', config)[0]
        phone_login = re.findall(r'Phone_Login = (.+?)\n', config)[0]

    phoneInv.updatePhones(path, phone_login)


if __name__ == "__main__":
    with open("config") as f:
        config = f.read()
        path = re.findall(r'path = (.+?)\n', config)[0]
    try:
        sys.modules['django']
        sys.path.append(os.path.abspath(path))
    except:
        import django
        sys.path.append(os.path.abspath(path))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "network_inventory.settings")
        django.setup()

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--accesspoint", help="Update UPSes.", action="store_true")
    parser.add_argument("-s", "--switch", help="Update UPSes.", action="store_true")
    parser.add_argument("-u", "--ups", help="Update UPSes.", action="store_true")
    parser.add_argument("-p", "--phone", help="Update UPSes.", action="store_true")
    args = parser.parse_args()
    if args.accesspoint:
        updateAP()
    if args.switch:
        updateSwitch()
    if args.ups:
        updateUPS()
    if args.phone:
        updatePhone()

    if not args.accesspoint and not args.switch and not args.ups and not args.phone:
        updateAP()
        updateSwitch()
        updateUPS()
        updatePhone()
