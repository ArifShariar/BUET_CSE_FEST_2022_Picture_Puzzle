from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html')


def view_rank_list_page(request):
    return render(request, 'rank_list/rank_list.html')
