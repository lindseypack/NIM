from django.contrib import admin
from devices.models import AP, UPS, Switch, Phone
import sys
import os
sys.path.append(os.path.abspath("/local_centre/NIM/code"))

import UpdateDevices

admin.site.disable_action('delete_selected')

def toggle_autoupdate(modeladmin, request, queryset):
    for obj in queryset:
        obj.autoupdate = not obj.autoupdate
        obj.save()
toggle_autoupdate.short_description = "Toggle auto-update"

class APAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'serialno', 'ip', 'mac', 'laststatus')
    fields = ['name', 'serialno', 'ip', 'mac', 'laststatus','checkstatus', 'autoupdate', 'notes']
    list_display = ('name', 'serialno', 'ip', 'mac', 'laststatus', 'lastupdate','checkstatus', 'autoupdate')
    search_fields = ['name', 'serialno', 'ip', 'mac']
    actions = ['toggle_autoupdate', 'toggle_checkstatus']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def toggle_checkstatus(modeladmin, request, queryset):
        for obj in queryset:
            obj.checkstatus = not obj.checkstatus
            obj.save()
    toggle_checkstatus.short_description = "Toggle checkstatus"


class SwitchAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'serialno', 'softwarever', 'mac', 'uptime', 'stack', 'status')
    fields = ['name', 'serialno', 'ip', 'softwarever', 'mac', 'uptime', 'stack', 'purchaseyr', 'status', 'autoupdate', 'notes']
    list_display = ['name', 'serialno', 'ip', 'softwarever', 'mac', 'uptime', 'stack', 'status', 'autoupdate', 'lastupdate']
    search_fields = ['name', 'serialno', 'softwarever', 'ip', 'mac', 'purchaseyr']
    actions = ['toggle_autoupdate', 'delete_selected']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        try:
            UpdateDevices.updateSwitch([obj.ip])
        except:
            pass


class PhoneAdmin(admin.ModelAdmin):
    fields = ['name', 'ip', 'mac', 'did', 'model', 'serialno', 'status', 'purchaseyr', 'description', 'notes']
    list_display = ['name', 'ip', 'mac', 'did', 'model', 'serialno', 'status', 'lastupdate']
    search_fields = ['name', 'ip', 'mac', 'did', 'model', 'serialno', 'status']
    actions = []


class UPSAdmin(admin.ModelAdmin):
    fields = ['name', 'ip', 'mac', 'brand', 'model', 'serialno', 'mfdate',
              'notes', 'autoupdate']
    list_display = ['name', 'ip', 'mac', 'brand', 'model', 'serialno', 'autoupdate', 'lastupdate']
    search_fields = ['name', 'ip', 'mac', 'brand', 'model', 'serialno', 'mfdate']
    actions = ['toggle_autoupdate','delete_selected']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        try:
            UpdateDevices.updateUPS()
        except:
            pass

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name', 'mac', 'model', 'serialno', 'brand']
        else:
            return ['name', 'mac', 'model', 'serialno']

admin.site.register(AP, APAdmin)
admin.site.register(UPS, UPSAdmin)
admin.site.register(Switch, SwitchAdmin)
admin.site.register(Phone, PhoneAdmin)

