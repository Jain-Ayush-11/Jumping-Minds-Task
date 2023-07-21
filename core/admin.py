from django.contrib import admin
from . import models

class CustomModelAdmin(admin.ModelAdmin):
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)

class ElevatorSystemAdmin(CustomModelAdmin):
    pass

class ElevatorAdmin(CustomModelAdmin):
    pass

class UserRequestAdmin(CustomModelAdmin):
    pass

# Register your models here.
admin.site.register(models.ElevatorSystem, ElevatorSystemAdmin)
admin.site.register(models.Elevator, ElevatorAdmin)
admin.site.register(models.UserRequest, UserRequestAdmin)
