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

    @action(detail=False, methods=['post'])
    def save_user_request(self, request):
        from_floor = request.data.get('from_floor')
        to_floor_list = request.data.get('to_floor', '')

        if from_floor is None:
            return Response({'error': 'from_floor parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not to_floor_list:
            return Response({'error': 'At least one valid to_floor parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        to_floor_list.sort()
        elevator = self.get_optimal_elevator(from_floor, to_floor_list)
        UserRequest.objects.filter(elevator=elevator, is_fulfilled=False).update(is_fulfilled=True)
        priority_list = self.calculate_priority(elevator, from_floor, to_floor_list)

        highest_priority = priority_list[0][1]
        temp_first_floor = priority_list[0][0]
        least_priority = priority_list[0][1]
        temp_last_floor = priority_list[0][0]

        user_requests = []
        for item in priority_list:
            user_request, _ = UserRequest.objects.get_or_create(
                elevator=elevator,
                from_floor=from_floor,
                to_floor=item[0],
                priority=item[1]
            )
            user_requests.append(user_request)
            if item[1]>highest_priority:
                highest_priority = item[1]
                temp_first_floor = item[0]
            if item[1]<least_priority:
                least_priority = item[1]
                temp_last_floor = item[0]

        if from_floor < temp_first_floor:
            elevator.is_moving_up = True
            elevator.is_moving_down = False
        else:
            elevator.is_moving_up = False
            elevator.is_moving_down = True

        elevator.current_floor = from_floor
        elevator.next_floor = temp_first_floor
        elevator.last_floor = temp_last_floor
        elevator.save()

        serializer = UserRequestSerializer(user_requests, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_optimal_elevator(self, from_floor, to_floor_list):
        elevators = Elevator.objects.filter(is_operational=True)

        if elevators.filter(is_moving_up=False, is_moving_down=False).exists():
            return elevators.filter(is_moving_up=False, is_moving_down=False).first()

        optimal_elevator = elevators[0]
        closest_distance = abs(elevators[0].last_floor-from_floor)

        for elevator in elevators:
            temp_distance = abs(elevator.last_floor-from_floor)
            if temp_distance<closest_distance:
                optimal_elevator = elevator
                closest_distance = temp_distance

        return optimal_elevator

    def calculate_priority(self, elevator, from_floor, to_floor_list):

        temp_list = [(1 if x-from_floor>0 else -1) for x in to_floor_list]
        direction = sum(temp_list)
        priority_list = list()
        highest_priority = len(to_floor_list)
        p = 1
        if direction>0:
            for i in range(len(to_floor_list)):
                if to_floor_list[i]<from_floor:
                    priority_list.append((to_floor_list[i], p))
                    p+=1
                else:
                    priority_list.append((to_floor_list[i], highest_priority))
                    highest_priority-=1
        else:
            for i in range(len(to_floor_list)):
                if to_floor_list[i]>=from_floor:
                    priority_list.append((to_floor_list[i], highest_priority))
                    highest_priority-=1
                else:
                    priority_list.append((to_floor_list[i], p))
                    p+=1
        return priority_list

    @action(detail=True, methods=['get'])
    def next_destination(self, request, pk=None):
        try:
            elevator = self.get_object()
            return Response({'next_destination': elevator.next_floor}, status=status.HTTP_200_OK)

        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def stop_elevator(self, request, pk=None):
        try:
            elevator = self.get_object()
            elevator.is_moving_up = False
            elevator.is_moving_down = False
            elevator.save()

            serializer = ElevatorSerializer(elevator)
            return Response({'message':'Elevator is stopped'}, status=200)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=404)

    @action(detail=True, methods=['get'])
    def direction(self, request, pk=None):
        try:
            elevator = self.get_object()
            if elevator.is_moving_up:
                return Response({'message':'Eleavtor is moving up'})
            elif elevator.is_moving_down:
                return Response({'message':'Eleavtor is moving down'})
            return Response({'message':'Eleavtor is stopped'})
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=404)
   
class UserRequestViewSet(viewsets.ModelViewSet):
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer

    @action(detail=True, methods=['get'])
    def fetch_user_requests(self, request, pk=None, is_fulfilled=None):
        try:
            elevator = Elevator.objects.get(pk=pk)
            if is_fulfilled:
                user_requests = elevator.requests.filter(is_fulfilled=False)
            else:
                user_requests = elevator.requests.all()
            serializer = UserRequestSerializer(user_requests, many=True)
            return Response(serializer.data)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=404)