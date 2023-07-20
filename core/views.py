from rest_framework import viewsets, status
from .models import Elevator, UserRequest
from .serializers import ElevatorSerializer, UserRequestSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=False, methods=['post'])
    def initialize(self, request):
        num_elevators = request.data.get('num_elevators')
        if num_elevators is None or not isinstance(num_elevators, int) or num_elevators <= 0:
            return Response({'error': 'Invalid number of elevators. Please provide a positive integer.'}, status=400)

        for i in range(num_elevators):
            Elevator.objects.create()

        return Response({'message': f'{num_elevators} elevators have been initialized.'}, status=201)

    @action(detail=False, methods=['get'])
    def get_current_floor(self, request, *args, **kwargs):
        try:
            elevator = self.get_object()
            current_floor = elevator.current_floor
            return Response({'current_floor': current_floor}, status=status.HTTP_200_OK)

        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def is_moving_up(self, request, pk=None):
        elevator = self.get_object()
        return Response({'is_moving_up': elevator.is_moving_up})

    @action(detail=True, methods=['post'])
    def mark_maintenance(self, request, pk=None):
        try:
            elevator = self.get_object()
            is_maintenance = request.data.get('is_maintenance')

            if is_maintenance is None:
                return Response({'error': 'is_maintenance parameter is missing.'}, status=400)

            # Update the maintenance status of the elevator
            elevator.is_operational = not is_maintenance
            elevator.save()

            serializer = ElevatorSerializer(elevator)
            return Response(serializer.data, status=200)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=404)

    @action(detail=True, methods=['post'])
    def open_door(self, request, pk=None):
        try:
            elevator = self.get_object()
            elevator.is_door_open = True
            elevator.save()

            serializer = ElevatorSerializer(elevator)
            return Response(serializer.data, status=200)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=404)

    @action(detail=True, methods=['post'])
    def close_door(self, request, pk=None):
        try:
            elevator = self.get_object()
            elevator.is_door_open = False
            elevator.save()

            serializer = ElevatorSerializer(elevator)
            return Response(serializer.data, status=200)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=404)

   
class UserRequestViewSet(viewsets.ModelViewSet):
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer

