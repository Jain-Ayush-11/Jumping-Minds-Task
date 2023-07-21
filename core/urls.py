from django.urls import path, include
from .views import *

urlpatterns = [
    path('elevators/initialize/', ElevatorViewSet.as_view({'post': 'initialize'}), name='initialize'),
    path('elevators/<int:pk>/mark-maintenance/', ElevatorViewSet.as_view({'post': 'mark_maintenance'}), name='mark_maintenance'),
    path('elevators/<int:pk>/door/<int:door>/', ElevatorViewSet.as_view({'post': 'door_status'}), name='door_status'),
    path('elevators/<int:pk>/current-floor/', ElevatorViewSet.as_view({'get': 'get_current_floor'}), name='elevator-current-floor'),
    path('elevators/save-user-request/', ElevatorViewSet.as_view({'post': 'save_user_request'}), name='save_user_request'),
    path('elevators/<int:pk>/fetch-user-requests/', UserRequestViewSet.as_view({'get': 'fetch_user_requests'}), name='fetch_user_requests'),
    path('elevators/<int:pk>/fetch-user-requests/<int:is_fulfilled>/', UserRequestViewSet.as_view({'get': 'fetch_user_requests'}), name='fetch_user_requests'),
    path('elevators/<int:pk>/next-destination/', ElevatorViewSet.as_view({'get': 'next_destination'}), name='next_destination'),
    path('elevators/<int:pk>/direction/', ElevatorViewSet.as_view({'get': 'direction'}), name='elevator-direction'),
    path('elevators/<int:pk>/stop/', ElevatorViewSet.as_view({'post': 'stop_elevator'}), name='elevator-stop'),
]
