class Elevator:
    '''
        Class for creating a single elevator/lift
        liftId: Id of current lift object
        isSelected: is current lift is already selected by clicking outside button by user or not
        direction: is moving up (1) or down (-1)
        isMoving: is current lift in motion currently or not
        isDoorOpen: are the doors of current lift open or not
        isWorking: is current lift operational or not
        onFloor: floor number on which current lift is right now
        services: list of request queues (floor numbers clicked by user)
    '''
    def __init__(self, liftId, onFloor = 0):
        self.liftId = liftId
        self.isSelected = False
        self.direction = 1
        self.isMoving = False
        self.isDoorOpen = False
        self.isWorking = True
        self.onFloor = onFloor
        self.services = []
    
    # fetches the current status of lift
    def currentStatus(self):
        if self.isWorking:
            if self.isMoving:
                direction = 'up' if self.direction == 1 else 'down'
                message = f"Lift {self.liftId} is on floor number {self.onFloor}. Lift {self.liftId} is moving {direction}wards."
            else:
                message = f"Lift {self.liftId} is stopped."
            print(message)
        else:
            print(f"{self.liftId} is not working")
    
    # changes the door status to True (open)
    def openDoor(self):
        self.isDoorOpen = True
        print(f"Lift {self.liftId}: Door is opening")
    
    # changes the door status to False (close)
    def closeDoor(self):
        self.isDoorOpen = False
        print(f"Lift {self.liftId}: Door is closing")
    
    # reset the lift values (after processing all requests)
    def resetLift(self):
        self.direction = 1
        self.isMoving = False
        self.isDoorOpen = False
        self.services = []
    
    # split the services list into direction wise lists up and down and return those lists
    def getDirectionWiseServices(self):
        self.services = sorted(self.services)
        upDirectionServices = []
        downDirectionServices = []
        for i in self.services:
            if i < self.onFloor:
                downDirectionServices.append(i)
            else:
                upDirectionServices.append(i)
        
        downDirectionServices = downDirectionServices[::-1]
        return upDirectionServices, downDirectionServices

    # process the up and down lists after processing the first value of services list
    def requestsProcessing(self):
        print(f"{self.liftId} is processing these floors: {self.services}")
        if self.services[0] != self.onFloor:
            if self.services[0] < self.onFloor:
                self.direction = -1
            else:
                self.direction = 1
            self.currentStatus()
            self.executeRequest(self.services[0:1])
        else:
            self.currentStatus()
            self.openDoor()
            self.closeDoor()
        
        self.services = self.services[1:]
        upDirectionServices, downDirectionServices = self.getDirectionWiseServices()
        if len(upDirectionServices) == 0:
            self.direction = -1
        elif len(downDirectionServices) == 0:
            self.direction = 1
        else:
            upsideEffort = abs(upDirectionServices[0] - self.onFloor)
            downsideEffort = abs(downDirectionServices[0] - self.onFloor)
            if upsideEffort <= downsideEffort:
                self.direction = -1
            else:
                self.direction = 1
        
            for i in range(2):
                if self.direction == 1:
                    self.executeRequest(upDirectionServices)
                else:
                    self.executeRequest(downDirectionServices)
                
                self.direction = -self.direction
                print("-"*30)
        
        self.resetLift()
    
    # move the lift one floor up or down at a time
    def move(self):
        if self.isWorking:
            self.onFloor += self.direction
        else:
            print(f"Lift {self.liftId} is not operational")
    
    # execute function called when processing the service list i.e. up or down at a time
    def executeRequest(self, requestList):
        while True:
            self.isMoving = True
            if self.onFloor in requestList:
                while requestList.count(self.onFloor) > 0:
                    requestList.remove(self.onFloor)
                self.isMoving = False
                self.openDoor()
                self.closeDoor()

            if len(requestList) == 0:
                break

            self.currentStatus()
            self.move()



class ElevatorSystem:
    '''
        Class for creting the new elevator system:
        numberOfLifts: number of lifts needed to be in a system (default = 5)
        requestQueueForEach: floors number list for each elevator to be processed 
        minFloor: minimum number of floor possible i.e. 0 in this system
        maxFloor: maximum number of floor possible (default=5)
        liftPositions: initial position of each lift in the system (if empty then all lifts will be at 0th floor)
    '''

    def __init__(self, requestQueueForEach, numberOfLifts=5 , minFloor=0, maxFloor=5, liftPositions=[]):
        self.numberOfLifts = numberOfLifts
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.elevators = []
        self.requestQueueForEach = requestQueueForEach
        
        # if not initial lift position, then make them place at 0th floor
        if len(liftPositions) <= 0:
            liftPositions = [0]*numberOfLifts
        
        # creating elevator objects list
        for i in range(numberOfLifts):
            newElevator = Elevator(i, liftPositions[i])
            self.elevators.append(newElevator)
    
    # processing the active floors request list , active floors are the ones where buttons are clicked by users
    def processRequest(self, activeFloors):
        activeFloors = list(set(activeFloors))
        activeFloors.sort()

        print(f"Assigning lifts to active floors: {activeFloors}")
        
        for queueCounter, floor in enumerate(activeFloors):
            # if floor number is valid (less than maxfloor)
            if floor <= self.maxFloor:
                distance = []
                # checking for elevator which is not free and closest to floor
                for elevator in self.elevators:
                    if not elevator.isSelected:
                        distance.append(abs(elevator.onFloor - floor))
                    else:
                        distance.append(9999)
                
                queueCounter = queueCounter%len(self.requestQueueForEach)
                selectedLift = distance.index(min(distance))
                selectedElevator = self.elevators[selectedLift]
                selectedElevator.services = [floor] + self.requestQueueForEach[queueCounter]
                selectedElevator.direction = 1 if selectedElevator.onFloor <= floor else -1
                selectedElevator.isSelected = True
        
        # processing the each elevators services list (floor numbers list)
        for elevator in self.elevators:
            if elevator.isSelected:
                print("*"*50)
                print(f"Lift Number: {elevator.liftId}")
                print(elevator.requestsProcessing())
