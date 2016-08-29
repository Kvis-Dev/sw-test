from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseNotFound

from db import Database
from users import forms


def index(request):
    db = Database()

    q = request.GET.get('q')
    if q:
        where = "LOWER(name) LIKE {} ".format(*db.prepare('%{}%'.format(q)))
    else:
        where = 1

    users = db.select('user', where=where)
    paginator = Paginator(users, int(request.COOKIES.get('pager', 10)))  # Show 25 contacts per page

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


def courses(request):
    db = Database()
    courses_list = db.select('courses')

    return render(request, 'courses/list.html', {
        'courses': courses_list
    })


def view(request, id=0):

    return render(request, 'users/view.html')


def update(request, id=0):
    db = Database()
    u = db.select('user', where='id=%d' % int(id))

    if not len(u) == 1:
        return HttpResponseNotFound('Not found')

    user = u[0]

    form = forms.User(request.POST if request.method == 'POST' else None, initial=user)
    form.fields['name'].widget.attrs['readonly'] = True

    if request.is_ajax():
        if form.is_valid():
            db.update('user', {
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'phone_mob': form.cleaned_data['phone_mob'],
                'status': form.cleaned_data['status'],
            }, where='id=%d' % int(id))

            db.query("DELETE FROM user_courses WHERE user_id=%d" % user['id'])

            for cid in request.POST.get('courses', '').split(','):
                if cid:
                    db.insert('user_courses', {
                        'course_id': int(cid),
                        'user_id': int(user['id']),
                    })

            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'errors': form.errors})
    else:
        if request.method == 'POST':
            raise Exception('An error happened, please enable AJAX')

    return render(request, 'users/update.html', {
        'form': form,
        'all_courses': db.select('courses'),
        'courses': db.select('user_courses', where='user_id=%d' % user['id'])
    })


def create(request):
    form = forms.User(request.POST if request.method == 'POST' else None)

    if request.is_ajax():
        if form.is_valid():
            db = Database()
            db.insert('user', {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'phone_mob': form.cleaned_data['phone_mob'],
                'status': form.cleaned_data['status'],
            })

            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'errors': form.errors})
    else:
        if request.method == 'POST':
            raise Exception('An error happened, please enable AJAX')

    return render(request, 'users/create.html', {
        'form': form
    })


def delete(request, id):
    db = Database()
    db.query("DELETE FROM user WHERE id=%d" % int(id))
    db.query("DELETE FROM user_courses WHERE user_id=%d" % int(id))

    return redirect('/')
