#!usr/bin/env python
import pycurl
import re
from StringIO import StringIO
import urllib
from timeout import timeout
import sys
import os
from devices.models import Phone

## This file is used to update the phone inventory data. Use
## the updatePhones function to run the update.

## use PyCURL to retrieve xml data, then parse this to get the name and
## model of each phone.
## return list of phones: [[name,model],...].
def getNameModel(path, login):
    url = "https://10.90.1.30:8443/axl/"
    binaryptr = open(path + '/code/phone/phones.xml','rb').read()
    head = ['Content-type:text/xml;', 'SOAPAction: CUCM:DB ver=8.5']

    storage = StringIO()
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(c.POSTFIELDS,binaryptr)
    c.setopt(c.HTTPHEADER,head)
    c.setopt(c.URL, url)
    c.setopt(c.USERPWD, login)
    c.setopt(c.VERBOSE, 0)
    c.setopt(c.WRITEFUNCTION, storage.write)
    c.perform()
    c.close()
    xml = storage.getvalue()
    storage.close()

    phones = list()
    phoneXML = re.findall(r"(<phone.+?</phone>)", xml)
    modelRE = re.compile(r"<model>(.+?)</model>")
    nameRE = re.compile(r"<name>(.+?)</name>")
    for phone in phoneXML:
        model = modelRE.findall(phone)[0]
        name = nameRE.findall(phone)[0]
        phones.append([name.upper(), model])
    return phones

## use an xml file containing a list of phone names
## to get the IP addr, name, status, description, timestamp?
## for each of those phones
def risData(ris, login):
    phones = list()
    while (len(phones) == 0):
    ## sometimes this doesn't find anything, keep trying
        url = "https://10.90.1.30:8443/realtimeservice/services/RisPort"
        head = ['Content-type:text/xml;', 'SOAPAction: http://schemas.cisco.com/ast/soap/action/#RisPort#SelectCmDevice']
        storage = StringIO()
        c = pycurl.Curl()
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(c.POSTFIELDS,ris)
        c.setopt(c.HTTPHEADER,head)
        c.setopt(c.URL, url)
        c.setopt(c.USERPWD, login)
        c.setopt(c.VERBOSE, 0)
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        xml = storage.getvalue()
        storage.close()

        items = re.findall(r"<item(.+?)</item>", xml)
        itemRE = re.compile(r"<item(.+</TimeStamp>)")
        ipRE = re.compile(r"(\d+\.\d+\.\d+\.\d+)</IpAddress>")
        statusRE = re.compile(r"<Status.+?>(.+?)</Status>")
        descRE = re.compile(r"<Description.+?>(.+?)</Description>")
        nameRE = re.compile(r"<Name.+?>(.+?)</Name>")
        timeStampRE = re.compile(r"<TimeStamp.+?>(.+?)</TimeStamp>")
        didRE = re.compile(r"<DirNumber.+?>(\d\d\d\d).+?</DirNumber>")

        for item in items:
            try:
            ## weird xml format - sometimes have <item>....<item>...</item>
            ## instead of always <item>...</item>
            ## so get rid of the leading <item>... if necessary
                item = itemRE.findall(item)[0]
            except:
                pass
            try:
                name = nameRE.findall(item)[0]
                ip = ipRE.findall(item)[0]
                status = statusRE.findall(item)[0]
                description = descRE.findall(item)[0]
                timeStamp = timeStampRE.findall(item)[0]
                try:
                    did = didRE.findall(item)[0]
                except:
                    did = "----"
                phones.append([name.upper(), ip, status, description, timeStamp, did])

            except:
                pass
    return phones

## take a list of phones and return a list of phones with distinct names.
## keep registered over unregistered.
## if both reg or both unreg, keep one with latest timestamp.
## phones in format [[name,ip,status,descr,timestamp],...].
## does not preserve original list.
def distinct(phones):
    distinctNames = set()
    for p in phones:
        distinctNames.add(p[0])

    distinctPhones = list()
    for i in range(len(phones)):
        matched = 0
        for j in range(i+1, len(phones)):
            if phones[i][0] == phones[j][0]: ## same name
                matched = 1
                if phones[i][0].upper() == "REGISTERED" \
                        and phones[j][0].upper() == "UNREGISTERED":
                    phones[j] = phones[i]
                elif phones[i][0].upper() == "UNREGISTERED" \
                        and phones[j][0].upper() == "REGISTERED":
                    pass
                else:
                    if int(phones[i][4]) > int(phones[j][4]):
                        phones[j] = phones[i]
        if matched == 0:
            distinctPhones.append(phones[i])

    assert len(distinctPhones) == len(distinctNames)
    return distinctPhones

## use a phone's ip to get its serial no.
## timeout because some phones require a login - when this
## happens the login request is written to stdout, need to
## fix that.
@timeout(1)
def serialNo(ip):
    page = urllib.urlopen("http://" + ip).read()
    serialno = re.findall(r"Serial Number.+?>(\w+?)\s?<", page, re.DOTALL)[0]
    return serialno

## Collect useful information about phones.
def phoneInfo(path, login):
    templateBegin = ""
    with open(path + "/code/phone/ris_production_template.xml", 'r') as f:
        templateBegin += f.read()
    templateEnd = "\n</Item></multiRef></soapenv:Body></soapenv:Envelope>"

    phonesNameModel = getNameModel(path, login)
    n = len(phonesNameModel)
    phones = list()
    ## ris data can only take up to 100 phones, so split phones into groups.
    for i in range(n/99 + 1):
        group = list()
        for k in range(99):
            if i*99 + k >= n:
                break
            group.append(phonesNameModel[i*99 + k][0])
        ris = templateBegin
        for phone in group:
            ris = ris + phone + ","
        ris = ris.strip(",") + templateEnd
        phones[len(phones):] = risData(ris, login)
    # format of phones is [[name,ip,status,descr,timestamp,did],...]
    phones = distinct(phones)

    for phone in phones:
        for phoneNM in phonesNameModel:
            if phone[0] == phoneNM[0]:
                phone.append(phoneNM[1])
                break
    # format of phones is [[name,ip,status,descr,timestamp,did,model],...]
    for phone in phones:
        try:
            phone.append(serialNo(phone[1]))
        except:
            phone.append(None)

    # format of phones is [[name,ip,status,descr,timestamp,did,model,serialno],...]

    return phones


## Get information about the phones, then update the phone database with Django.
def updatePhones(path, login):
    phones = phoneInfo(path, login)

    oldPhones = Phone.objects.all()

    ## set status = inactive for phones in the db that can't be reached now
    foundNames = [phone[0] for phone in phones]
    for old in oldPhones:
        if old not in foundNames:
            old.status = "Inactive"
            old.save()

    for phone in phones:
        try:
            pObj = oldPhones.get(name = phone[0])
        except:
            pObj = Phone()
            pObj.name = phone[0]
        pObj.mac = phone[0][3:]
        pObj.ip = phone[1]
        pObj.status = phone[2]
        pObj.description = phone[3].replace("'","")
        pObj.model = phone[6]
        pObj.did = phone[5]
        if phone[7] != None:
            pObj.serialno = phone[7]
        pObj.save()
