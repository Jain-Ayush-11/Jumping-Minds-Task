from django.db import models

class Elevator(models.Model):
    is_operational = models.BooleanField(default=True)
    current_floor = models.PositiveIntegerField(default=1)
    is_moving_up = models.BooleanField(default=False)
    is_moving_down = models.BooleanField(default=False)
    is_door_open = models.BooleanField(default=False)

class UserRequest(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name='requests')
    from_floor = models.PositiveIntegerField()
    to_floor = models.PositiveIntegerField()
    requested_time = models.DateTimeField(auto_now_add=True)
    priority = models.PositiveIntegerField(default=0)