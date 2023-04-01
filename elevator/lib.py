class Elevator:
    def __init__(self, liftId, onFloor = 0):
        self.liftId = liftId
        self.isSelected = False
        self.direction = 1
        self.isMoving = False
        self.isDoorOpen = False
        self.isWorking = True
        self.onFloor = onFloor
        self.services = []
    
    def currentStatus(self):
        if self.isWorking:
            if self.isMoving:
                direction = 'up' if self.direction == 1 else 'down'
                message = f"{self.liftId} is moving {direction}wards."
            else:
                message = f"{self.liftId} is not moving."
            message += f" Lift is on floor number {self.onFloor}"
            print(message)
        else:
            print(f"{self.liftId} is not working")
    
    def openDoor(self):
        self.isDoorOpen = True
        print(f"Lift {self.liftId}: Door is opening")
    
    def closeDoor(self):
        self.isDoorOpen = False
        print(f"Lift {self.liftId}: Door is closing")
    
    def resetLift(self):
        self.direction = 1
        self.isMoving = False
        self.isDoorOpen = False
        self.services = []
    
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

    def requestsProcessing(self):
        print(f"{self.liftId} is processing: {self.services}")
        if self.services[0] != self.onFloor:
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
        
        self.resetLift()
    
    def move(self):
        if self.isWorking:
            self.onFloor += self.direction
        else:
            print(f"Lift {self.liftId} is not operational")
    
    def executeRequest(self, requestList):
        while True:
            self.isMoving = True
            if self.onFloor in requestList:
                while requestList.count(self.onFloor) > 0:
                    requestList.remove(self.onFloor)
            
            self.isMoving = False
            self.currentStatus()
            self.openDoor()
            self.closeDoor()

            if len(requestList) == 0:
                break

            self.currentStatus()
            self.move()



class ElevatorSystem:
    def __init__(self, numberOfLifts, requestQueueForEach, minFloor = 0, maxFloor = 4, liftPositions = []):
        self.numberOfLifts = numberOfLifts
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.elevators = []
        self.requestQueueForEach = requestQueueForEach

        if len(liftPositions) <= 0:
            liftPositions = [0]*numberOfLifts
        
        for i in range(numberOfLifts):
            newElevator = Elevator(i, liftPositions[i])
            self.elevators.append(newElevator)
    
    def processRequest(self, activeFloors):
        activeFloors = list(set(activeFloors))
        activeFloors.sort()

        print(f"Assigning lifts to active floors: {activeFloors}")
        
        for queueCounter, floor in enumerate(activeFloors):
            distance = []
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
        

        for elevator in self.elevators:
            if elevator.isSelected:
                print("********************************")
                print(f"Lift Number: {elevator.lifeId}")
                print(elevator.executeRequest())