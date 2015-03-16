## Name this file "deviceconfig.py" and put in values for your settings.

## Access point OIDs:
AP_OIDs = {
    "mac": "",
    "name": "",
    "ip": "",
    "serial": "",
    "model": "",
}
AP_Status_OID = ""

## Access point controller IPs:
AP_ControllerIPs = [""]

## Email settings for AP status update.
AP_Email = {
    "from": "",
    "to": [""],
    "server": "",
}

## Switch login username and password
Switch_Login = ["",""]

## If you want to test a few switch IPs, put them here
Switch_IPs = []

## UPS OIDs. Adjust brand names and OIDs as necessary.
UPS_OIDs = {
    "APC": {
        "serial": "",
        "model": "",
        "mac": "",
        "name": "",
    },
    "Liebert": {
        "serial": "",
        "model": "",
        "mac": "",
        "mfdate": "",
    },
    "LiebertNX": {
        "serial": "",
        "model": "",
        "mac": "",
    }
}

## phone login
Phone_Login = ""
