from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from user.models import *

from django.contrib import messages

from django.shortcuts import render, redirect
from .forms import *


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


def participant_register(request):
    if request.user.is_authenticated:
        return redirect('logout')

    u_form = UserForm()
    p_form = ParticipantForm()

    if request.method == "POST":
        u_form = UserForm(request.POST)
        p_form = ParticipantForm(request.POST)

        if u_form.is_valid() and p_form.is_valid():
            user_created = u_form.save()
            print("User created")
            p_form = p_form.save(commit=False)
            p_form.user = user_created
            print("Participant created")
            return redirect('login')
        else:
            print("Failed to create user")

    return render(request, 'auth/register.html', {'u_form': u_form, 'p_form': p_form})


def participant_logout(request):
    return HttpResponse("hello world from logout page")
