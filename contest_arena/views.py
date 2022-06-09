from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from .models import *
from user.models import *
from .forms import *


def home(request):
    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
    }
    if request.user.is_authenticated:
        to_frontend["user_level"] = request.user.participant.curr_level

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


def load_next_puzzle(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')

    # if request.method == 'GET':
    if pk < request.user.participant.curr_level:
        return HttpResponse("You have already solved this puzzle!")
    elif pk > request.user.participant.curr_level:
        return HttpResponse("Hehe hacker man , no good")

    form = PuzzleAnsForm()
    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
        "msg": "",
        "puzzle": None,
        "form": form,
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
        puzzle = Puzzle.objects.filter(Q(level=request.user.participant.curr_level + 1) & Q(visible=True))
        print(puzzle)
        if not puzzle:
            to_frontend['msg'] = "You have completed all currently available levels. Please wait for more"
        else:
            to_frontend['puzzle'] = puzzle.first()

    if request.method == "POST":
        # if the submitted answer is correct, then increase the level of participant
        # show success message
        # else show error message
        form = PuzzleAnsForm(request.POST)
        if form.is_valid():
            ans = form.cleaned_data['ans']
            if ans.lower() == to_frontend['puzzle'].ans.lower():
                # increase level
                request.user.participant.curr_level += 1
                # update position
                # request.user.participant.position = Participant.objects.filter(Q)
                request.user.participant.save()
                to_frontend['msg'] = "Correct answer! You have advanced to the next level"
                return redirect('puzzle', pk=request.user.participant.curr_level)
            else:
                to_frontend['msg'] = "Wrong answer! Please try again"

    return render(request, 'contest_arena/puzzle.html', to_frontend)
