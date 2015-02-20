from django.db import models

class Switch(models.Model):
    serialno = models.CharField("Serial No", max_length=50, default='', blank=True)
    ip = models.GenericIPAddressField("IP")
    name = models.CharField("Name", max_length=50, default='', blank=True)
    mac = models.CharField("MAC", max_length=12, default='', blank=True)
    model = models.CharField("Model", max_length=50, default='', blank=True)
    softwarever = models.CharField("Software Version", max_length=20, default='', blank=True)
    uptime = models.CharField("Uptime", max_length=50, default='', blank=True)
    stack = models.IntegerField("Stack", default=0, blank=True)
    purchaseyr = models.CharField("Purchase Year", max_length=4, default='', blank=True)
    purchaseorder = models.CharField("Purchase Order", max_length=50, default='', blank=True)
    uplink1 = models.TextField("Uplink 1", default='', blank=True)
    uplink2 = models.TextField("Uplink 2", default='', blank=True)
    uplink3 = models.TextField("Uplink 3", default='', blank=True)
    uplink4 = models.TextField("Uplink 4", default='', blank=True)
    notes = models.TextField("Notes", default='', blank=True)
    status = models.CharField("Status", max_length=128, default='active', blank=True)
    lastupdate = models.DateTimeField("Last Update", auto_now=True)

    class Meta:
        verbose_name = "Switch"
        verbose_name_plural = "Switches"

    def __str__(self):
        return self.name

class Phone(models.Model):
    name = models.CharField("Name", max_length=32, primary_key=True)
    ip = models.GenericIPAddressField("IP")
    mac = models.CharField("MAC", max_length=12, default='')
    did = models.CharField("DID", max_length=10, default='')
    model = models.CharField("Model", max_length=32, default='')
    serialno = models.CharField("Serial No", max_length=50, default='')
    status = models.CharField("Status", max_length=50, default='')
    purchaseyr = models.CharField("Purchase Year", max_length=4, default='')
    description = models.CharField("Description", max_length=200, default='')
    notes = models.TextField("Notes", default='', blank=True)
    lastupdate = models.DateTimeField("Last Update", auto_now=True)

    class Meta:
        verbose_name = "Phone"

    def __str__(self):
        return self.name

class AP(models.Model):
    serialno = models.CharField("Serial No", max_length=50, primary_key=True)
    ip = models.GenericIPAddressField("IP")
    mac = models.CharField("MAC", max_length=12, default='')
    name = models.CharField("Name", max_length=50, default='')
    checkstatus = models.BooleanField("Check Status?", default=True)
    laststatus = models.CharField("Last Status", max_length=32, default='up')
    notes = models.TextField("Notes", default='', blank=True)
    autoupdate = models.BooleanField("Autoupdate?", default=True)
    lastupdate = models.DateTimeField("Last Update", auto_now=True)

    class Meta:
        verbose_name = "Access Point"
        ordering = ['name']

    def __str__(self):
        return self.name

class UPS(models.Model):
    ip = models.GenericIPAddressField("IP", primary_key=True)
    name = models.CharField("Name", max_length=50, default='', blank=True)
    mac = models.CharField("MAC", max_length=12, default='', blank=True)
    model = models.CharField("Model", max_length=32, default='', blank=True)
    serialno = models.CharField("Serial No", max_length=50, default='', blank=True)
    mfdate = models.CharField("Manufacture Date", max_length=10, default='', blank=True)
    brand = models.CharField("Brand", max_length=50, default='', blank=True, choices=[('Liebert','Liebert'),('APC','APC')])
    notes = models.TextField("Notes", default='', blank=True)
    autoupdate = models.BooleanField("Autoupdate?", default=True)
    lastupdate = models.DateTimeField("Last Update", auto_now=True)

    class Meta:
        verbose_name = "UPS"
        verbose_name_plural = "UPSes"

    def __str__(self):
        return self.name

