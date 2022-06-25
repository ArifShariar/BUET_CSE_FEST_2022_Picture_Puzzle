import datetime
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from user.models import *
from shomobay_shomiti_detector.models import *
from .forms import *
from shomobay_shomiti_detector.views import *


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
    participants = User.objects.filter(is_staff=False,
                                       participant__last_successful_submission_time__isnull=False).order_by(
        '-participant__curr_level', 'participant__last_successful_submission_time')

    rank_list = []
    for p in participants:
        rank_list.append(p)
        print(p.participant.curr_level, p.username, p.participant.student_ID)

    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
        "rank_list": rank_list,
        "user_level": request.user.participant.curr_level,
        "SHOMOBAY_SHOMITI": settings.SHOMOBAY_SHOMITI,
        "THRESHOLD": settings.THRESHOLD,
    }

    print(to_frontend['THRESHOLD'])

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
    if not request.user.participant.disabled:
        redirect('home')

    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
        "puzzle": None,
        "msg": "You are banned from the contest. Please contact the contest administrator for more information."
    }
    return render(request, 'contest_arena/banned.html', to_frontend)


@login_required(login_url='login')
def load_next_puzzle(request, pk):

    if request.user.participant.disabled and settings.SHOMOBAY_SHOMITI:
        return redirect('banned')

    if pk < request.user.participant.curr_level:
        return HttpResponse("You have already solved this puzzle!")
    elif pk > request.user.participant.curr_level:
        if settings.SHOW_HACK:
            return redirect('hackerman')
        else:
            return HttpResponseNotFound("You can't solve this now!")

    form = PuzzleAnsForm()
    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
        "msg": "",
        "puzzle": None,
        "form": form,
        "meme": None,
    }
    # #
    # """------------------------------------------------temporary for testing start------------------------------------------"""
    # try:
    #     to_frontend['meme'] = random.choice(Meme.objects.filter(meme_for=request.user.participant.acc_type - 1,
    #                                                             meme_type=1))
    # except IndexError:
    #     to_frontend['meme'] = None
    # print(to_frontend['meme'])
    #
    # """------------------------------------------------temporary for testing end--------------------------------------------"""

    if settings.CONTEST_STARTED is False:
        to_frontend['msg'] = "Contest has not started yet"
    elif settings.CONTEST_ENDED is True:
        to_frontend['msg'] = "Contest has ended"
    else:
        # getting next puzzle
        puzzle = Puzzle.objects.filter(level=request.user.participant.curr_level, visible=True)
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
            # add submission
            submit = Submission.objects.create(participant=request.user.participant,
                                               level=request.user.participant.curr_level,
                                               time=datetime.datetime.now(datetime.timezone.utc),
                                               ans=ans)

            if ans.strip().lower() == to_frontend['puzzle'].ans.strip().lower():
                submit.status = 1
                submit.save()

                # increase level
                request.user.participant.curr_level += 1
                request.user.participant.last_successful_submission_time = datetime.datetime.now(datetime.timezone.utc)
                request.user.participant.save()

                # shomobay shomiti
                if settings.SHOMOBAY_SHOMITI:
                    HMModel(request.user.participant)

                # getting next puzzle
                puzzle = Puzzle.objects.filter(level=request.user.participant.curr_level, visible=True)
                if not puzzle:
                    to_frontend['msg'] = "You have completed all currently available levels. Please wait for more"
                    to_frontend['puzzle'] = None
                else:
                    to_frontend['puzzle'] = puzzle.first()

                # load meme
                try:
                    to_frontend['meme'] = random.choice(
                        Meme.objects.filter(meme_for=request.user.participant.acc_type,
                                            meme_type=1))
                except IndexError:
                    to_frontend['meme'] = None
            else:
                submit.status = 0
                submit.save()

                to_frontend['msg'] = "Wrong answer! Please try again"

                number_of_unsuccessful_attempts = Submission.objects.filter(participant=request.user.participant,
                                                                            level=request.user.participant.curr_level,
                                                                            status=0).count()
                if number_of_unsuccessful_attempts % settings.MEME_WRONG == 0:
                    # load meme
                    try:
                        to_frontend['meme'] = random.choice(
                            Meme.objects.filter(meme_for=request.user.participant.acc_type,
                                                meme_type=1))
                    except IndexError:
                        to_frontend['meme'] = None
        else:
            redirect('hackerman')

    return render(request, 'contest_arena/puzzle.html', to_frontend)
