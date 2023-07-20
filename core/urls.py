from django.urls import path, include
from .views import *

urlpatterns = [
    path('elevators/initialize/', ElevatorViewSet.as_view({'post': 'initialize'}), name='initialize'),
    path('elevators/<int:pk>/mark-maintenance/', ElevatorViewSet.as_view({'post': 'mark_maintenance'}), name='mark_maintenance'),
    path('elevators/<int:pk>/open-door/', ElevatorViewSet.as_view({'post': 'open_door'}), name='open_door'),
    path('elevators/<int:pk>/close-door/', ElevatorViewSet.as_view({'post': 'close_door'}), name='close_door'),
    path('elevators/<int:pk>/current-floor/', ElevatorViewSet.as_view({'get': 'get_current_floor'}), name='elevator-current-floor'),    
]