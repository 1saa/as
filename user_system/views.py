from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json
from functools import wraps
from .models import User

# Create your views here.
def experiment(request):
    return cors_Jsresponse({'username': 'Alice', 'password': 'Bob'})

def response_options():
  response = HttpResponse()
  response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  response['Access-Control-Allow-Methods'] = 'POST'
  response['Access-Control-Allow-Credentials'] = 'true'
  response['Access-Control-Allow-Headers'] = 'Content-Type'
  return response

def add_cors_header(response):
  response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  response['Access-Control-Allow-Credentials'] = 'true'
  return response

def require_cors_POST(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return response_options()
        if request.method == 'POST':
            return func(request, *args, **kwargs)
        
    return inner

def cors_Jsresponse(ret):
    return add_cors_header(JsonResponse(ret))

@csrf_exempt
@require_cors_POST
def register(request):
    register_info = json.loads(request.body)
    name = register_info['username']
    password = register_info['password']
        
    if User.objects.filter(username=name).exists():
        return cors_Jsresponse({'code': 1, 'msg': 'The username has been used'})
    else:
        new_account = User()
        new_account.username = name
        new_account.password_hash = password
        new_account.save()
        return cors_Jsresponse({'code': 0, 'msg': 'success'})

@csrf_exempt
@require_cors_POST
def login(request):
    login_info = json.loads(request.body)
    name = login_info['username']
    password = login_info['password']

    if User.objects.filter(username=name).exists():
        user_check = User.objects.get(username=name)
        if user_check.password_hash == password:
            request.session['is_login'] = '1'
            request.session['name'] = name
            return cors_Jsresponse({'code': 0, 'msg': 'success'})
        else:
            return cors_Jsresponse({'code': 1, 'msg': 'The password is wrong'})
    else:
        return cors_Jsresponse({'code': 1, 'msg': 'The username does not exist'})

def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        ret = request.session.get('is_login')

        if ret == '1':
            return func(request, *args, **kwargs)
        else:
            return cors_Jsresponse({'code': 123, 'msg': 'Please login'})
    return inner

@csrf_exempt
@check_login
def logout(request):
    request.session.flush()
    return cors_Jsresponse({
        'code': 0,
        'msg': 'logout successfully'
    })

@csrf_exempt
@require_cors_POST
@check_login
def set_password(request):
    name = request.session['name']
    info = json.loads(request.body)
    old_password = info['oldPassword']
    new_password = info['newPassword']
    cur_user = User.objects.get(username=name)
    if old_password == cur_user.password_hash:
        cur_user.password_hash = new_password
        cur_user.save()
        return cors_Jsresponse({
            'code': 0,
            'msg': 'Change password successfully.'
        })
    else:
        return cors_Jsresponse({
            'code': 2,
            'msg': 'Password is wrong.'
        })

@csrf_exempt
@require_GET
@check_login
def get_my_information(request):
    name = request.session['name']
    cur_user = User.objects.get(username=name)
    return cors_Jsresponse({
        'username': cur_user.username,
        'email': cur_user.email,
        'profile': cur_user.profile,
        'public': cur_user.public,
        'follow': cur_user.like_users,
        'subscribe': cur_user.like_tags,
    })

@csrf_exempt
@require_GET
def get_others_information(request):
    name = request.GET['username']
    if not User.objects.filter(username=name).exists():
        return cors_Jsresponse({'code': 1, 'msg': 'The user does not exist'})
    else:
        cur_user = User.objects.get(username=name) 
        if cur_user.public == True:
            return cors_Jsresponse({
                'username': cur_user.username,
                'email': cur_user.email,
                'profile': cur_user.profile,
                'follow': cur_user.like_users,
                'like': cur_user.like_tags,
            })
        else:
            return cors_Jsresponse({
                'username': cur_user.username,
                'email': cur_user.email,
                'profile': 'This is private',
                'follow': 'This is private',
                'like': 'This is private',
            })

@csrf_exempt
@require_cors_POST
@check_login
def set_my_information(request):
    name = request.session['name']
    set_info = json.loads(request.body)
    email = set_info['email']
#    password = set_info['password']
    profile = set_info['profile']
    public = set_info['public']
    cur_user = User.objects.get(username=name)
    cur_user.email = email
#    cur_user.password_hash = password
    cur_user.profile = profile
    cur_user.public = public
    cur_user.save()
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_GET
def get_history(request):
    name = request.GET['username']
    if not User.objects.filter(username=name).exists():
        return cors_Jsresponse({'code': 1, 'msg': 'The user does not exist'})
    else:
        return cors_Jsresponse({'code': 1, 'msg': 'not implement yet'})

@csrf_exempt
@require_cors_POST
@check_login
def add_follow(request):
    name = request.session['name']
    re_info = json.loads(request.body)
    follow = re_info['follow']
    cur_user = User.objects.get(username=name)
    cur_user.add_like_user(follow)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_cors_POST
@check_login
def delete_follow(request):
    name = request.session['name']
    re_info = json.loads(request.body)
    follow = re_info['follow']
    cur_user = User.objects.get(username=name)
    cur_user.delete_like_user(follow)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_cors_POST
@check_login
def add_subscribe(request):
    name = request.session['name']
    re_info = json.loads(request.body)
    subscribe = re_info['subscribe']
    cur_user = User.objects.get(username=name)
    cur_user.add_like_tags(subscribe)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_cors_POST
@check_login
def delete_subscribe(request):
    name = request.session['name']
    re_info = json.loads(request.body)
    subscribe = re_info['subscribe']
    cur_user = User.objects.get(username=name)
    cur_user.delete_like_tags(subscribe)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })