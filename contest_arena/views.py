from django.db.models import Q
from django.shortcuts import render, redirect
from django.conf import settings
from .models import *
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


def load_next_puzzle(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        to_frontend = {
            "user_active": request.user.is_authenticated,
            "user": request.user,
            "msg": "",
            "puzzle": None,
        }

        print(settings.CONTEST_STARTED)
        print(settings.CONTEST_ENDED)

        if settings.CONTEST_STARTED is False:
            to_frontend['msg'] = "Contest has not started yet"
        elif settings.CONTEST_ENDED is True:
            to_frontend['msg'] = "Contest has ended"
        else:
            # getting next puzzle
            print('current level ', request.user.participant.curr_level)
            puzzle = Puzzle.objects.filter(Q(level=request.user.participant.curr_level+1) & Q(visible=True))
            print(puzzle)
            if not puzzle:
                to_frontend['msg'] = "You have completed all currently available levels. Please wait for more"
            else:
                to_frontend['puzzle'] = puzzle.first()

        return render(request, 'contest_arena/puzzle.html', to_frontend)
