NIM
===

NIM is a small network inventory management tool written in Python, using Django. NIM can automatically track inventory information such as IP address, serial number, model number, etc. for access points, switches, UPSes, and phones. This information can be viewed in a friendly format through a Django administrator interface.

Features
========
- Track inventory information for access points, switches, UPSes, and phones.
- Web interface for viewing and editing stored inventory data. 

Installation
============

- First, make sure all of NIM's requirements are installed. NIM requires Python 2.7, MySQL, Django, Django extensions, PySNMP, snmpwalk, Exscript, and PyCURL, and MySQLdb.
- Clone the NIM repository.
- In MySQL, make a database called "network_inventory". 
- Using NIM/config_template, create NIM/config with the settings needed for your setup.
- Run NIM/code/UpdateDevices.py
- Run the command "manage.py runserver" to put Django's administrator web interface on localhost, or use "manage.py runserver ip:port".
- Navigate to the administrator interface in a web browser.
