# Elevator System

Implemented the business logic for simplified elevator system in Python and created APIs for following features:

- Initialise the elevator system to create ‘n’ elevators in the system
- Fetch all requests for a given elevator
- Fetch the next destination floor for a given elevator
- Fetch if the elevator is moving up or down currently
- Saves user request to the list of requests for a elevator
- Mark a elevator as not working or in maintenance 
- Open/close the door.

## Project Structure
- Inside project directory, created an django app named elevator.
- Inside elevator app, in `urls.py` file mentioned all the api endpoints and their corresponding views methods. 
- All Views methods are present in `views.py` file. 
- In `lib.py` file, the Elevator and ElevatorSystem classes are present with all their required attributes and methods.

## Elevator Design
- ElevatorSystem: Represents the elevator system with fixed numbers of elevators avaialbel, floors allowed and resposible for allocating the active floor number to each closest available lift.
- Elevator: Represents the each elevator object inside the elevator system with attributes like is working/not working, is moving/stop, are doors open/close, direction of motion (up/down), floor number on which lift is present currently and list of floor numbers to be processed.

## API Reference

#### Create Elevator System

```http
  POST /api/create-elevator-system

  Create the elevator system with given number of lifts.
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `numLifts` | `number` | Number of lifts in a system |
| `maxFloor` | `number` | Max number of floors in a system |
| `requestQueue` | `List` | List of floor number for each lift |
| `liftPositions` | `List` | Initial floor positions of each lift |

#### Fetch Requests

```http
  GET /api/fetch-requests

  Fetch all the floor numbers of requests for an elevator.
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `number` | Lift id |

#### Next Destination

```http
  GET /api/next-destination

  Fetch the next destination from the elevator floor number queue.
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `number` | Lift id |

#### Fetch Direction

```http
  GET /api/direction

  Fetch the current moving direction for an elevator.
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `number` | Lift id |

#### Add Elevator Request

```http
  POST /api/add-request

  Enter the new floor request in the queue for an elevator.
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `number` | Lift id |
| `floor`      | `number` | Floor number |

#### Change Status

```http
  POST /api/change-status

  Change the working/operational status of an elevator.
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `number` | Lift id |
| `status`  | `string` | Status string ('not working', 'maintenance', 'working') |

#### Close/Open Door

```http
  POST /api/door

  Close/open the doors of an elevator.
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `number` | Lift id |


