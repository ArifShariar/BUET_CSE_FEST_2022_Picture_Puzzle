import datetime
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

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

    return render(request, 'contest_arena/home.html', to_frontend)


@login_required(login_url='login')
def view_leaderboard_page(request):

    participants = User.objects.filter(is_staff=False, participant__last_successful_submission_time__isnull=False).order_by('-participant__curr_level', 'participant__last_successful_submission_time')

    rank_list = []
    for p in participants:
        # batch
        p.participant.student_ID = p.participant.student_ID[0:2]
        rank_list.append(p)
        print(p.participant.curr_level, p.username, p.participant.student_ID)

    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
        "rank_list": rank_list,
        "user_level": request.user.participant.curr_level,
    }

    return render(request, 'contest_arena/leaderboard.html', to_frontend)


@login_required(login_url='login')
def hack(request):
    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
    }

    if HackerManImage.objects.count() == 0:
        # temporary fix
        return render(request, 'contest_arena/hacker.html', to_frontend)

    # if the user is alumni
    if request.user.participant.acc_type == 1:
        image = HackerManImage.objects.get(id=random.randint(1, HackerManImage.objects.count()))
        to_frontend["random_image"] = image
        random_quote = AlumniHackermanQuote.objects.get(id=random.randint(1, AlumniHackermanQuote.objects.count()))
        to_frontend["random_quote"] = random_quote
    else:
        image = HackerManImage.objects.get(id=random.randint(1, HackerManImage.objects.count()))
        to_frontend["random_image"] = image
        random_quote = CurrentStudentHackerQuote.objects.get(
            id=random.randint(1, CurrentStudentHackerQuote.objects.count()))
        to_frontend["random_quote"] = random_quote

    return render(request, 'contest_arena/hacker.html', to_frontend)


@login_required(login_url='login')
def banned(request):
    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
        "puzzle": None,
        "msg": "You are banned from the contest. Please contact the contest administrator for more information."
    }
    return render(request, 'contest_arena/banned.html', to_frontend)


@login_required(login_url='login')
def load_next_puzzle(request, pk):
    if pk < request.user.participant.curr_level:
        return HttpResponse("You have already solved this puzzle!")
    elif pk > request.user.participant.curr_level and settings.SHOW_HACK:
        return redirect('hackerman')
    elif pk > request.user.participant.curr_level and not settings.SHOW_HACK:
        return HttpResponseNotFound("You can't solve this now!")

    elif request.user.participant.disabled:
        return redirect('banned')

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
                request.user.participant.last_successful_submission_time = datetime.datetime.now()
                request.user.participant.save()
                to_frontend['msg'] = "Correct answer! You have advanced to the next level"
                return redirect('puzzle', pk=request.user.participant.curr_level)
            else:
                to_frontend['msg'] = "Wrong answer! Please try again"

    return render(request, 'contest_arena/puzzle.html', to_frontend)
