from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

# Create your views here.

def ElevatorHome(request):
    return HttpResponse("Please use APIs url. Go to API page using this url: http://localhost:8000/api")
