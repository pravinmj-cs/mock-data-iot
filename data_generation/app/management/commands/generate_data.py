from faker import Faker
from datetime import datetime
from time import sleep, gmtime, strftime
from django.core.management.base import BaseCommand
from django.db import connection
from app.models import AppUser, UserDevice, DeviceData

faker = Faker()

class Command(BaseCommand):
    help = "Generates mock data for user, device"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            "################################# User and Device Data Generation Input Sample #################################"
        )
        self.stdout.write("Enter the number of users: 5")
        self.stdout.write("Enter the number of devices to be generated for each user: 5")
        self.stdout.write("Enter the interval type: year")
        self.stdout.write("Enter the interval length: 5")
        self.stdout.write("Enter the interval period: hour")
        self.stdout.write("Enter the interval duration: 1")
        self.stdout.write("\n")
        self.stdout.write(
            "For the above sample input data, 5 users will be generated, Each user will have 5 devices"
        )
        self.stdout.write(
            "Data will be generated for every hour for 5 years.starting from 5 years before the current year."
        )
        self.stdout.write(
            "################################# Input Sample #################################"
        )
        self.stdout.write("\n")


        self.stdout.write("\n")
        try:
            no_of_users = int(input("Enter the number of users: "))
            no_of_devices_per_user = int(
                input("Enter the number of devices per user to be generated for each user: ")
            )
            # data generation for day, month or year
            self.stdout.write("\n")
            self.stdout.write("***** Interval type can be only 'day', 'month', or 'year' *****")
            interval_type = str(input("Enter the interval type: "))
            interval_type = "year"
            if interval_type not in ["day", "month", "year"]:
                self.stdout.write("Enter value only of 'day' or 'month' or 'year'!!! ")
            # How many length based on above interval_type
            interval_length = int(input("Enter the interval length(only numeric): "))
            # Interval Period - hour, minute, day
            self.stdout.write("\n")
            self.stdout.write("***** Interval period can be only 'hour', 'minute', or 'day' *****")
            interval_period = str(input("Enter interval period: "))
            interval_period = 'hour'
            if interval_period not in ["hour", "minute", "day"]:
                self.stdout.write("Enter value only of 'hour' or 'minute' or 'day'!!! ")
            # duration between each data- based on above interval period
            interval_duration = input("Enter interval duration(only numeric): ")
        except ValueError:
            self.stdout.write("Enter only numbers !!! ")
            sys.exit()

        # if interval_type is year and interval_length is 2 -data will be generated for 2 years
        series_interval_length = f"{interval_length} {interval_type}"
        # if interval_period is hour and interval_duration is 3 -data will be generated for every 3 hours
        series_interval_duration = f"{interval_duration} {interval_period}"

        start_time = datetime.now()
        user_list = [faker.name() for i in range(1, no_of_users + 1)]
        user_instances = []
        for i in range(len(user_list)):
            user_obj = AppUser(name=user_list[i]) 
            user_instances.append(user_obj)
        AppUser.objects.bulk_create(user_instances)

        self.stdout.write("\n")
        self.stdout.write("App Users created....")
        sleep(1)
        device_index = 0
        device_instances = []
        for i in range(len(user_list)):
            for j in range(1, no_of_devices_per_user + 1):
                device_obj = UserDevice(app_user=user_instances[i], device_name=f"UID{device_index}")
                device_index += 1
                device_instances.append(device_obj)

        UserDevice.objects.bulk_create(device_instances)

        device_list = UserDevice.objects.all().values("id", "device_name")
        for device in device_list:
            # self.stdout.write(f"Inserting Data for Device - {device['device_name']}")
            query = """
                        INSERT INTO device_data (datetime, user_device_id, temperature, humidity)
                        SELECT
                        datetime,
                        user_device_id,
                        random()*100 AS temperature,
                        random()*100 AS humidity    
                        FROM generate_series(now() - interval '%s', now(), interval '%s') AS g1(datetime),
                        generate_series(%s,%s) AS g2(user_device_id)
                    """ % (
                series_interval_length,
                series_interval_duration,
                device["id"],
                device["id"],
            )
            cur = connection.cursor()
            cur.execute(query)
        end_time = datetime.now()
        mean_time = end_time - start_time
        time_taken_seconds = mean_time.seconds
        self.stdout.write("**** Task Completed ****")
        total_minutes = strftime("%H:%M:%S", gmtime(time_taken_seconds))
        self.stdout.write(f"Completed in {total_minutes}")

        self.stdout.write("**** Generated Records ****")
        self.stdout.write(f"Total User: {AppUser.objects.all().count()}")
        self.stdout.write(f"Total Devices: {UserDevice.objects.all().count()}")
        self.stdout.write(f"Total Device Data: {DeviceData.objects.all().count()}")

        AppUser.objects.all().delete()
        UserDevice.objects.all().delete()
        DeviceData.objects.all().delete()