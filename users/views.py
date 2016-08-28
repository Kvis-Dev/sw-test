from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from db import Database
from users import forms


def index(request):
    db = Database()
    users = db.select('user')
    paginator = Paginator(users, 25)  # Show 25 contacts per page

    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'users/index.html', {
        'users': users
    })


def view(request, id=0):

    return render(request, 'users/view.html')


def update(request, id=0):

    return render(request, 'users/update.html')


def create(request):
    form = forms.User(request.POST if request.method == 'POST' else None)

    if form.is_valid():
        pass
    else:
        pass

    return render(request, 'users/create.html', {
        'form': form
    })


def delete(request):

    return redirect('/')
