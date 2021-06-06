from django.db import models

# Create your models here.


class AppUser(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "app_user"
        verbose_name_plural = "App User"


class UserDevice(models.Model):
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=200)

    def __str__(self):
        return self.device_name

    class Meta:
        db_table = "user_device"
        verbose_name_plural = "User Device"


class DeviceData(models.Model):
    user_device = models.ForeignKey(UserDevice, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    humidity = models.DecimalField(max_digits=8, decimal_places=3, default=0)

    def __str__(self):
        return f"{self.datetime} - {self.sensor_uid} - {self.sensor_type} - {self.value}"

    class Meta:
        db_table = "device_data"
        verbose_name_plural = "Device Data"
