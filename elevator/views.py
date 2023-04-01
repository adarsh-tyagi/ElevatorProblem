from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from .lib import Elevator, ElevatorSystem

# Create your views here.
elevatorSystem = None

@api_view(['GET'])
def home(request):
    if request.method == 'GET':
        allApiInfo = [
            {'task': 'Create Elevator System', 'api endpoint': 'api/create-elevator-system', 'description': 'To create the new elevator system with given number of lifts, min and max floors possible, requests queues for each lift is there is any and initial floor positions for all lifts (by default all will be at 0th floor).'},
            {'task': 'Fetch Requests', 'api endpoint': 'api/fetch-requests', 'description': 'Fetch all the requests queue for a given elevator id if elevator is present and operational.'},
            {'task': 'Next Destination', 'api endpoint': 'api/next-destination', 'description': 'Fetch the next destination for a given elevator if elevator is present, operational and there is next destination.'},
            {'task': 'Fetch Direction', 'api endpoint': 'api/direction', 'description': 'Fetch the current direction for a given elevator is it is present, operational and currently moving.'},
            {'task': 'Add Elevator Request', 'api endpoint': 'api/add-request', 'description': 'Add the given floor request for a given elevatoer if it is present and operational.'},
            {'task': 'Change Status', 'api endpoint': 'api/change-status', 'description': 'Change the status of a given elevator to not working if it is present and working or vice-versa.'},
            {'task': 'Close/Open Door', 'api endpoint': 'api/door', 'description': 'Close or open the door of a given elevator if it is present, operational and not in motion.'}
        ]
        return JsonResponse({'message': "This is the home page for Elevator project APIs.", 'APIs': allApiInfo})

@api_view(['POST'])
def createElevatorSystem(request):
    if request.method == 'POST':
        numLifts = int(request.POST.get('numLifts', 5))
        maxFloor = int(request.POST.get('maxFloor', 5))
        requestQueue = request.POST.get('requestQueue', [[]]*numLifts)
        liftPositions = request.POST.get('liftPositions', [])

        minFloor = 0
        global elevatorSystem
        elevatorSystem = ElevatorSystem(numberOfLifts=numLifts, minFloor=minFloor, maxFloor=maxFloor, requestQueueForEach=requestQueue, liftPositions=liftPositions)
        return JsonResponse({'message': f"Elevator system with {numLifts} number of lifts is initialized "})

@api_view(['GET'])
def fetchElevatorRequests(request):
    if request.method == 'GET':
        elevatorId = request.GET.get('id', None)
        if not elevatorId or int(elevatorId) > len(elevatorSystem.elevators):
            return JsonResponse({'message': 'Please give the valid elevator id to fetch its requests'})
        if not elevatorSystem:
            return JsonResponse({'message': 'No elevator system exists currently'})
        
        currentElevator = elevatorSystem.elevators[int(elevatorId)]
        if currentElevator.isWorking:
            currentElevatorRequests = currentElevator.services
            if len(currentElevatorRequests) > 0:
                return JsonResponse({'message': f'Here are the requests processing by elevator {elevatorId} : {currentElevatorRequests}' })
            return JsonResponse({'message': f'There are no request services for elevator id {elevatorId}'})
        return JsonResponse({'message': f'Sorry!, Elevator id {elevatorId} is not operational'})
    
@api_view(['GET'])
def fetchNextDestination(request):
    if request.method == 'GET':
        elevatorId = request.GET.get('id', None)
        if not elevatorId or int(elevatorId) > len(elevatorSystem.elevators):
            return JsonResponse({'message': 'Please give the valid elevator id to fetch its next destination'})
        if not elevatorSystem:
            return JsonResponse({'message': 'No elevator system exists currently'})

        currentElevator = elevatorSystem.elevators[int(elevatorId)]
        if currentElevator.isWorking:
            if len(currentElevator.services) > 0:
                currentElevatorNextDestination = currentElevator.services[0]
                return JsonResponse({'message': f'Elevator {elevatorId} next destination is floor number {currentElevatorNextDestination}'})
            return JsonResponse({'message': f'There is no destination in queue for elevator id {elevatorId}'})
        return JsonResponse({'message': f'Sorry!, Elevator id {elevatorId} is not operational'})
    
@api_view(['GET'])
def fetchElevatorDirection(request):
    if request.method == 'GET':
        elevatorId = request.GET.get('id', None)
        if not elevatorId or int(elevatorId) > len(elevatorSystem.elevators):
            return JsonResponse({'message': 'Please give the valid elevator id to fetch its direction'})
        if not elevatorSystem:
            return JsonResponse({'message': 'No elevator system exists currently'})

        currentElevator = elevatorSystem.elevators[int(elevatorId)]
        if currentElevator.isWorking:
            if currentElevator.isMoving:
                currentElevatorDirection = 'up' if currentElevator.direction == 1 else 'down'
                return JsonResponse({'message': f'Elevator {elevatorId} is moving {currentElevatorDirection}wards'})
            return JsonResponse({'message': f'Elevator id {elevatorId} is not moving currently'})
        return JsonResponse({'message': f'Sorry!, Elevator id {elevatorId} is not operational'})

@api_view(['POST'])
def saveElevatorRequests(request):
    if request.method == 'POST':
        elevatorId = request.POST.get('id', None)
        floorNumber = request.POST.get('floor', None)
        if not elevatorId or int(elevatorId) > len(elevatorSystem.elevators) or not floorNumber or int(floorNumber) > elevatorSystem.maxFloor:
            return JsonResponse({'message': 'Please give the valid elevator id and floor number'})
        if not elevatorSystem:
            return JsonResponse({'message': 'No elevator system exists currently'})

        currentElevator = elevatorSystem.elevators[int(elevatorId)]
        currentElevator.services.append(floorNumber)
        return JsonResponse({'message': f'Elevator id {elevatorId} requests are updated. New requests are: {currentElevator.services}'})

@api_view(['POST'])
def changeElevatorStatus(request):
    if request.method == 'POST':
        elevatorId = request.POST.get('id', None)
        status = request.POST.get('status', None)
        if not elevatorId or int(elevatorId) > len(elevatorSystem.elevators) or not status:
            return JsonResponse({'message': 'Please give the valid elevator id and status both to change its status'})
        if not elevatorSystem:
            return JsonResponse({'message': 'No elevator system exists currently'})

        currentElevator = elevatorSystem.elevators[int(elevatorId)]
        if status in ('not working', 'maintenance'):
            curr_status = False
        else:
            curr_status = True
        currentElevator.isWorking = curr_status
        return JsonResponse({'message': f'Status of Elevator id {elevatorId} is updated.'})


@api_view(['POST'])
def closeOrOpenDoor(request):
    if request.method == 'POST':
        elevatorId = request.POST.get('id', None)
        if not elevatorId or int(elevatorId) > len(elevatorSystem.elevators):
            return JsonResponse({'message': 'Please give the valid elevator id to change status of door'})
        if not elevatorSystem:
            return JsonResponse({'message': 'No elevator system exists currently'})

        currentElevator = elevatorSystem.elevators[int(elevatorId)]
        if currentElevator.isWorking:
            if not currentElevator.isMoving:
                currentElevator.isDoorOpen = not currentElevator.isDoorOpen
                doorStatus = 'opening' if currentElevator.isDoorOpen else 'closing'
                return JsonResponse({'message': f'Doors of elevator id {elevatorId} are {doorStatus}'})
            return JsonResponse({'message': f'Elevator id {elevatorId} is moving right now. Can not change the door status'})
        return JsonResponse({'message': f'Sorry!, Elevator id {elevatorId} is not operational'})
