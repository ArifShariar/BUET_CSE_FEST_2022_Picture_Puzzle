from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from user.models import *

# Create your views here.


def register(request):
    return HttpResponse("hello world from register page")


def participant_login(request):
    print("here")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome back ' + username + '!')
            participant_info = Participant(user=user)

            level = participant_info.curr_level + 1
            # return redirect('puzzle:show_puzzle', level)
            return redirect('logout')

    return render(request, 'contest_arena/login_page.html')


def participant_logout(request):
    return HttpResponse("hello world from logout page")



