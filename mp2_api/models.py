from django.db import models
# import hashlib
# Create your models here.
class Drone(models.Model):
    """Database model for drones """

    drone_id = models.CharField(max_length = 100, primary_key = True)
    registered_date = models.DateField(auto_now_add=True)
    lat = models.DecimalField(default = 0, max_digits=9, decimal_places=6)
    log = models.DecimalField(default = 0, max_digits=9, decimal_places=6)
    battery_level = models.IntegerField()
    last_accessed = models.DateTimeField(auto_now=True)
    users_connected = models.IntegerField(default = 0)
    state = models.IntegerField(default = 0)
    warning_bit = models.BooleanField(default = False)
    def __str__(self):
        return "Drone : " +str(self.drone_id) + "Registered Date : " + str(self.registered_date) + \
        "GPS Location : " + str([self.lat, self.log]) + "Battery Level : " + str(self.battery_level) + \
        "Last Accessed : " + str(self.last_accessed) + "Users Connected : " + str(self.users_connected) + \
        "State : " + str(self.state) + "Warning : " + str(self.warning_bit)
    class Meta :
        verbose_name_plural = "Drones"

class Client(models.Model):
    """Database model for clients """

    client_id = models.CharField(max_length = 100, primary_key = True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null = True)
    ip_address = models.GenericIPAddressField()
    drone = models.ForeignKey(Drone, on_delete = models.CASCADE, default = 0)
    def __str__(self):
        return "Client Id : " + str(self.client_id) + "Login Time : " + str(self.login_time) + \
        "Logout Time : " + str(self.logout_time) + "IP Address : " + str(self.ip_address)
    class Meta :
        verbose_name_plural = "Clients"
