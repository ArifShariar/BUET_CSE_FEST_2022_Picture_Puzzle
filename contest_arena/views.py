from django.shortcuts import render, redirect
from user.models import *


def home(request):
    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
    }

    print(to_frontend["user_active"])
    print(to_frontend["user"])

    return render(request, 'home/home.html', to_frontend)


def view_rank_list_page(request):
    if not request.user.is_authenticated:
        return redirect('home')

    participants = User.objects.filter(is_staff=False).order_by('participant__position')

    rank_list = []
    for p in participants:
        rank_list.append(p)
        print(p.participant.position, p.username, p.participant.student_ID)

    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
        "rank_list": rank_list,
    }

    return render(request, 'rank_list/rank_list.html', to_frontend)
