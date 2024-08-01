from django.db import models

class ParkingLocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class KeyHanger(models.Model):
    id = models.BigAutoField(primary_key=True)
    hanger_number = models.IntegerField(unique=True)  # Ensuring hanger numbers are unique
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Key Hanger {self.hanger_number}"

class Driver(models.Model):
    name = models.CharField(max_length=255)
    truck_rego_number = models.CharField(max_length=20)
    key_hanger_number = models.ForeignKey(KeyHanger, on_delete=models.CASCADE, blank=True, null=True)
    parking_location = models.ForeignKey(ParkingLocation, on_delete=models.CASCADE, blank=True, null=True)
    rear_wheel_chocked = models.BooleanField(default=False)
    key_removed_from_ignition = models.BooleanField(default=False)
    arrival_time = models.DateTimeField(blank=True, null=True)
    departure_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
