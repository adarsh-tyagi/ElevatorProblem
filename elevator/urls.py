from django.urls import path
from . import views

app_name = 'elevator'

urlpatterns = [
    path('', view=views.home, name='home'),
    path('create-elevator-system', view=views.createElevatorSystem, name='CreateElevatorSystem'),
    path('fetch-requests', view=views.fetchElevatorRequests, name='FetchElevatorRequests'),
    path('next-destination', view=views.fetchNextDestination, name='FetchNextDestination'),
    path('direction', view=views.fetchElevatorDirection, name='FetchElevatorDirection'),
    path('add-request', view=views.saveElevatorRequests, name='AddElevatorRequest'),
    path('change-status', view=views.changeElevatorStatus, name='ChangeElevatorStatus'),
    path('door', view=views.closeOrOpenDoor, name='CloseOpenDoor'),
]