NIM
===

NIM is a small network inventory management tool written in Python, using Django. NIM can automatically track inventory information such as IP address, serial number, model number, etc. for access points, switches, UPSes, and phones. This information can be viewed in a friendly format through a Django administrator interface.

Installation
============

- First, make sure all of NIM's requirements are installed. NIM requires Python 2.x, MYSQL, Django, PySNMP, Exscript, and PyCURL.
- Clone the NIM repository.
- Run NIM/code/UpdateDevices.py
- Run the command "manage.py runserver" to put Django's administrator web interface on localhost, or use "manage.py runserver ip:port".
- Navigate to the administrator interface in a web browser.
