from django.db import models

class ElevatorSystem(models.Model):
    pass

class Elevator(models.Model):
    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)
    is_operational = models.BooleanField(default=True)
    current_floor = models.PositiveIntegerField(default=1)
    next_floor = models.PositiveIntegerField(default=1)
    last_floor = models.PositiveIntegerField(default=1)
    is_moving_up = models.BooleanField(default=False)
    is_moving_down = models.BooleanField(default=False)
    is_door_open = models.BooleanField(default=False)

class UserRequest(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name='requests')
    from_floor = models.PositiveIntegerField()
    is_fulfilled = models.BooleanField(default=False)
    to_floor = models.PositiveIntegerField()
    priority = models.PositiveIntegerField(default=0)
