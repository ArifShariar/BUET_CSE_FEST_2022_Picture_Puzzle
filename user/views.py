from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *


def participant_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.add_message(request, messages.SUCCESS, 'Welcome back ' + username + '!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'contest_arena/login.html')


def participant_register(request):
    if request.user.is_authenticated:
        return redirect('home')

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
            p_form.batch = p_form.student_ID[0:2]
            p_form.save()
            print("Participant created")

            # keep user logged in
            login(request, user_created)
            return redirect('home')
        else:
            for err in p_form.errors:
                messages.error(request, p_form.errors[err])
            for err in u_form.errors:
                messages.error(request, u_form.errors[err])
            print("Failed to create user")

    return render(request, 'contest_arena/register.html', {'u_form': u_form, 'p_form': p_form})


def participant_logout(request):
    logout(request)
    return redirect('home')
