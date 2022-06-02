from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def register(request):
    return HttpResponse("hello world from register page")


def login(request):
    return HttpResponse("hello world from login page")


def logout(request):
    return HttpResponse("hello world from logout page")
