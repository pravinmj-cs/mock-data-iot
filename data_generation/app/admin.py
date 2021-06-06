from django.contrib import admin
from app.models import AppUser, UserDevice, DeviceData

class AppUserAdmin(admin.ModelAdmin):
    list_display = ["name"]

class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ["app_user", "device_name"]

class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ["user_device", "datetime", "temperature", "humidity"]

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(DeviceData, DeviceDataAdmin)