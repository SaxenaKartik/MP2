from django.db import models

# Create your models here.
class Drone(models.Model):
    """Database model for drones """
    drone_id = models.AutoField(primary_key = True)
    registered_date = models.DateField(auto_now_add=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    log = models.DecimalField(max_digits=9, decimal_places=6)
    battery_level = models.IntegerField()
    last_accessed = models.DateTimeField(auto_now=True)
    users_connected = models.IntegerField()
    status = models.IntegerField()
    warning_bit = models.BooleanField(default = False)
    def __str__(self):
        return "Drone : " +str(self.drone_id) + "Registered Date : " + str(self.registered_date) + \
        "GPS Location : " + str([self.lat, self.log]) + "Battery Level : " + str(self.battery_level) + \
        "Last Accessed : " + str(self.last_accessed) + "Users Connected : " + str(self.users_connected) + \
        "Status : " + str(self.status) + "Warning : " + str(self.warning_bit)
    class Meta :
        verbose_name_plural = "Drones"

class Client(models.Model):
    """Database model for clients """
    client_id = models.IntegerField()
    login_time = models.DateTimeField(auto_now=True)
    logout_time = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()
    def __str__(self):
        return "Client Id : " + str(self.client_id) + "Login Time : " + str(self.login_time) + \
        "Logout Time : " + str(self.logout_time) + "IP Address : " + str(self.ip_address)
    class Meta :
        verbose_name_plural = "Clients"
