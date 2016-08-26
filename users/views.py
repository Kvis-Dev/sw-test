from django.shortcuts import render, redirect

# Create your views here.


def index(request):

    return render(request, 'users/index.html')


def view(request, id=0):

    return render(request, 'users/view.html')


def update(request, id=0):

    return render(request, 'users/update.html')


def create(request):

    return render(request, 'users/create.html')


def delete(request):

    return redirect('/')
