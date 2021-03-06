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
    fields = ['name', 'serialno', 'ip', 'mac', 'model', 'laststatus','checkstatus',
        'autoupdate', 'notes']
    list_display = ('name', 'serialno', 'ip', 'mac', 'laststatus', 'lastupdate',
        'checkstatus', 'autoupdate')
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
    readonly_fields = ('name', 'serialno', 'model', 'softwarever', 'mac', 'uptime',
        'stack', 'status')
    fieldsets = (
        (None, {
            'fields': ['name', 'serialno', 'model', 'ip', 'softwarever', 'mac',
            'uptime', 'stack', 'purchaseyr', 'purchaseorder', 'status', 'notes',
            'autoupdate']
        }),
        ('Uplinks', {
            'classes': ('collapse',),
            'fields': ( 'uplink1', 'uplink2', 'uplink3', 'uplink4')
        }),
        )
    list_display = ['ip', 'serialno', 'model', 'name', 'softwarever', 'mac',
        'uptime', 'stack', 'status', 'lastupdate', 'autoupdate']
    list_filter = ['status']
    search_fields = ['name', 'serialno', 'model', 'softwarever', 'ip', 'mac',
        'purchaseyr']
    actions = ['toggle_autoupdate', 'delete_selected']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        try:
            UpdateDevices.updateSwitch([obj.ip])
        except:
            pass

    def toggle_autoupdate(modeladmin, request, queryset):
        for obj in queryset:
            obj.autoupdate = not obj.autoupdate
            obj.save()
        toggle_autoupdate.short_description = "Toggle auto-update"


class PhoneAdmin(admin.ModelAdmin):
    fields = ['name', 'ip', 'mac', 'did', 'model', 'serialno', 'status',
        'purchaseyr', 'description', 'notes']
    list_display = ['name', 'ip', 'mac', 'did', 'model', 'serialno', 'status',
        'lastupdate']
    search_fields = ['name', 'ip', 'mac', 'did', 'model', 'serialno', 'status']
    actions = []


class UPSAdmin(admin.ModelAdmin):
    fields = ['name', 'ip', 'mac', 'brand', 'model', 'serialno', 'mfdate',
        'notes', 'autoupdate']
    list_display = ['name', 'ip', 'mac', 'brand', 'model', 'serialno',
        'autoupdate', 'lastupdate']
    list_filter = ['brand']
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
        return ['name', 'mac', 'model', 'serialno']

admin.site.register(AP, APAdmin)
admin.site.register(UPS, UPSAdmin)
admin.site.register(Switch, SwitchAdmin)
admin.site.register(Phone, PhoneAdmin)

