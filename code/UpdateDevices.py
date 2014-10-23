import sys
import os
import re

def config():
    with open("config") as f:
        config = f.read()

        path = re.findall(r'path = (.+?)\n', config)[0]

    ## access point stuff
        ap_mac = re.findall(r'AP_MAC_OID = (.+?)\n', config)[0]
        ap_name = re.findall(r'AP_Name_OID = (.+?)\n', config)[0]
        ap_ip = re.findall(r'AP_IP_OID = (.+?)\n', config)[0]
        ap_serial = re.findall(r'AP_Serial_OID = (.+?)\n', config)[0]
        ap_model = re.findall(r'AP_Model_OID = (.+?)\n', config)[0]
        ap_status = re.findall(r'AP_Status_OID = (.+?)\n', config)[0]
        ap_controllers = re.findall(r'AP_ControllerIPs = \[(.+?)\]', config)[0].split(",")

    ## switch stuff
        switch_login = re.findall(r'Switch_Login = \[(.+?)\]', config)[0].split(",")
        switch_IPs = re.findall(r'Switch_IPs = \[(.+?)\]', config)[0].split(",")

    ## UPS stuff
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

    ## Phone stuff
        phone_login = re.findall(r'Phone_Login = (.+?)\n', config)[0]

        return (path,
            (ap_mac, ap_name, ap_ip, ap_serial, ap_model, ap_status, ap_controllers),
            switch_login, switch_IPs,
            apc_oids, liebert_oids,
            phone_login)


def updateAPs():
    from ap import apInv
    print "Updating access points..."

def updateSwitches():
    from switch import switchInv
    print "Updating switches..."

def updateUPSes():
    from ups import upsInv
    print "Updating UPSes..."

def updatePhones():
    from phone import phoneInv
    print "Updating phones..."


if __name__ == "__main__":
    path, ap_oids, switch_login, switch_IPs, apc_oids, liebert_oids, phone_login = config()

    try:
        sys.modules['django']
        sys.path.append(os.path.abspath(path))
    except:
        import django
        sys.path.append(os.path.abspath(path))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "network_inventory.settings")
        django.setup()

    print "Argument list:", sys.argv
    args = sys.argv
    if "-a" in args or "--ap" in args

    # print "Updating access points..."
    # apInv.updateAccessPoints(path, ap_oids)
    # print "Updating switches..."
    # switchInv.updateSwitches(switch_login, switch_IPs)
    # print "Updating UPSes..."
    # upsInv.updateUPS(apc_oids, liebert_oids)
    # print "Updating phones..."
    # phoneInv.updatePhones(path, phone_login)
