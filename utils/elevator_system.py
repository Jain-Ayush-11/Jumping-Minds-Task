from core.models import *

def get_optimal_elevator(self, from_floor, to_floor_list):
    '''
        Returns the most optimal elevator based on the list floor elevator is called from.
        Returns the elevator which will be closest after it fulfills its last request.
    '''
    elevators = Elevator.objects.filter(is_operational=True)

    optimal_elevator = elevators[0]
    closest_distance = abs(elevators[0].last_floor-from_floor)

    for elevator in elevators:
        temp_distance = abs(elevator.last_floor-from_floor)
        if temp_distance<closest_distance:
            optimal_elevator = elevator
            closest_distance = temp_distance

    return optimal_elevator

def calculate_priority(self, elevator, from_floor, to_floor_list):
    '''
        Method to determine the order in which requests will be fulfilled.
        Assigns a priority to each method.
        Higher number implies higher priority, while lower number implies a low priority.
        Hence, request with priority 1 will be the fulfilled last.
    '''
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
