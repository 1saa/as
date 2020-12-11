from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
import json
from functools import wraps
from .models import User, Papers, Discussion, Dis_center

# Create your views here.
def experiment(request):
    return JsonResponse({'username': 'Alice', 'password': 'Bob'})



@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def register(request):

    if (request.method == 'OPTIONS'):
      return response_options()
    
    register_info = json.loads(request.body)
    name = register_info['username']
    password = register_info['password']
        
    if User.objects.filter(username=name).exists():
        return add_cors_header(JsonResponse({'code': 1, 'msg': 'The username has been used'}))
    else:
        new_account = User()
        new_account.username = name
        new_account.password_hash = password
        new_account.save()
        return add_cors_header(JsonResponse({'code': 0, 'msg': 'success'}))

@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def login(request):

    if (request.method == 'OPTIONS'):
      return response_options()

    login_info = json.loads(request.body)
    name = login_info['username']
    password = login_info['password']

    if User.objects.filter(username=name).exists():
        user_check = User.objects.get(username=name)
        if user_check.password_hash == password:
            request.session['is_login'] = '1'
            request.session['name'] = name
            return add_cors_header(JsonResponse({'code': 0, 'msg': 'success'}))
        else:
            return add_cors_header(JsonResponse({'code': 1, 'msg': 'The password is wrong'}))
    else:
        return add_cors_header(JsonResponse({'code': 1, 'msg': 'The username does not exist'}))

def check_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        ret = request.session.get('is_login')

        if ret == '1':
            return func(request, *args, **kwargs)
        else:
            return add_cors_header(JsonResponse({'code': 1, 'msg': 'Please login'}))
    return inner

@csrf_exempt
@require_GET
@check_login
def get_user_basic(request):
    return add_cors_header(JsonResponse({'username': request.session['name']}))

@csrf_exempt
@require_GET
@check_login
def get_user_detail(request):
    name = request.session['name']
    cur_user = User.objects.get(username=name)
    if cur_user.public == True:
        return add_cors_header(JsonResponse({
            'username': cur_user.username,
            'email': cur_user.email,
            'profile': cur_user.profile,
            'follow': cur_user.like_users,
            'like': cur_user.like_tags,
        }))
    else:
        return add_cors_header(JsonResponse({
            'username': cur_user.username,
            'email': cur_user.email,
            'profile': 'This is private',
            'follow': 'This is private',
            'like': 'This is private',
        }))

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
