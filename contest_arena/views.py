import glob
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user.models import *
from .forms import *
from CSE_FEST_2022_Picture_Puzzle.settings import MEDIA_ROOT


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


@login_required(login_url='login')
def view_rank_list_page(request):
    # if not request.user.is_authenticated:
    #     return redirect('home')

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


def hack(request):
    # TODO: in my opinion, this is not the way to do it, we can create a model in the database to store the
    #       quotes and the images, and then we can use the model to get the quotes and images randomly
    #       from the database. Moreover, storing images in files MANUALLY not loading it

    to_frontend = {
        "user_active": request.user.is_authenticated,
        "user": request.user,
    }
    senior_hacker_quote = [
        'ভাই আমার গার্লফ্রেন্ডের ফেইসবুক একাউন্টটা হ্যাক করে দিবা ?',
        'স্যারা ভাই স্যারা.......... পুরা হ্যাকার',
        'ও বাই ও বাই.......... স্যারা',
        'স্যারা ভাই স্যারা.......... পুরা হ্যাকার',
        'ping cute-hamster.com',
        'Ever wonder Freddie Mercury was also a black hat hacker like you'
    ]
    hacker_man_images = []

    hacker_man_image_dir = MEDIA_ROOT + '\hackerman\\'
    print(hacker_man_image_dir)
    for filename in glob.iglob(hacker_man_image_dir + "**/*.jpg", recursive=True):
        hacker_man_images.append(filename)

    random_quote = senior_hacker_quote[random.randint(0, len(senior_hacker_quote) - 1)]
    random_img = hacker_man_images[random.randint(0, len(hacker_man_images) - 1)]

    to_frontend["random_quote"] = random_quote
    to_frontend["random_img"] = random_img

    return render(request, 'contest_arena/hacker.html', to_frontend)


@login_required(login_url='login')
def load_next_puzzle(request, pk):
    if pk < request.user.participant.curr_level:
        return HttpResponse("You have already solved this puzzle!")
    elif pk > request.user.participant.curr_level:
        return redirect('hackerman')

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
