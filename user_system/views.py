from django.shortcuts import render
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json
from functools import wraps
from .models import User, Papers, Discussion, Dis_center

# Create your views here.
def experiment(request):
    return JsonResponse({'username': 'Alice', 'password': 'Bob'})



@csrf_exempt
@require_POST
def register(request):

    register_info = json.loads(request.body)
    name = register_info['username']
    password = register_info['password']
        
    if User.objects.filter(username=name).exists():
        return JsonResponse({'code': 1, 'msg': 'The username has been used'})
    else:
        new_account = User()
        new_account.username = name
        new_account.password_hash = password
        new_account.save()
        return JsonResponse({'code': 0, 'msg': 'success'})

@csrf_exempt
@require_POST
def login(request):

    login_info = json.loads(request.body)
    name = login_info['username']
    password = login_info['password']

    if User.objects.filter(username=name).exists():
        user_check = User.objects.get(username=name)
        if user_check.password_hash == password:
            request.session['is_login'] = '1'
            request.session['name'] = name
            return JsonResponse({'code': 0, 'msg': 'success'})
        else:
            return JsonResponse({'code': 1, 'msg': 'The password is wrong'})
    else:
        return JsonResponse({'code': 1, 'msg': 'The username does not exist'})

def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        ret = request.session.get('is_login')

        if ret == '1':
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({'code': 1, 'msg': 'Please login'})
    return inner

@csrf_exempt
@require_GET
@check_login
def get_user_basic(request):
    return JsonResponse({'username': request.session['name']})

@csrf_exempt
@require_GET
@check_login
def get_user_detail(request):
    name = request.session['name']
    cur_user = User.objects.get(username=name)
    if cur_user.public == True:
        return JsonResponse({
            'username': cur_user.username,
            'email': cur_user.email,
            'profile': cur_user.profile,
            'follow': cur_user.like_users,
            'like': cur_user.like_tags,
        })
    else:
        return JsonResponse({
            'username': cur_user.username,
            'email': cur_user.email,
            'profile': 'This is private',
            'follow': 'This is private',
            'like': 'This is private',
        })