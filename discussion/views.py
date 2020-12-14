from django.shortcuts import render
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json
from user_system.models import User, Discussion, DisCenter
from user_system.views import check_login

@csrf_exempt
@require_POST
@check_login
def create_discussion(request):
    name = request.session['name']
    set_info = json.loads(request.body)
    tittle = set_info['tittle']
    info = set_info['text']
    new_dis = Discussion()
    new_dis.creator = name
    new_dis.tittle = tittle
    new_dis.information = info
    new_dis.save()
    return JsonResponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_GET
def get_discussion(request):
    get_info = json.loads(request.body)
    cur_dis = Discussion.objects.get(id=get_info['id'])
    return JsonResponse({
        'creator': cur_dis.creator,
        'tittle': cur_dis.tittle,
        'text': cur_dis.information,
        'tags': cur_dis.tag_list,
        'reco': cur_dis.recommend,
        'repy_n': cur_dis.reply_number,
        'reply': cur_dis.reply,
        'ct': cur_dis.create_time,
        'lp': cur_dis.last_reply,
        'ln': cur_dis.last_name,
        'lt': cur_dis.last_time,
    })

@csrf_exempt
@require_POST
@check_login
def add_tag(request):
    add_info = json.loads(request.body)
    tag = add_info['tag']
    cur_dis = Discussion.objects.get(id=add_info['id'])
    cur_dis.add_tag(tag)
    return JsonResponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_POST
@check_login
def delete_tag(request):
    delete_info = json.loads(request.body)
    tag = delete_info['tag']
    cur_dis = Discussion.objects.get(id=delete_info['id'])
    cur_dis.delete_tag(tag)
    return JsonResponse({
        'code': 0,
        'msg': 'set successfully'
    })

#reply具有两个参数，一个为整数是回复对象，0为初始讨论信息，另一个为回复字符串
@csrf_exempt
@require_POST
@check_login
def reply(request):
    name = request.session['name']
    info = json.loads(request.body)
    reply_to = info['reply_to']
    reply_text = info['text']
    cur_dis = Discussion.objects.get(id=info['id'])
    cur_dis.add_reply(reply_to, reply_text, name)
    return JsonResponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_POST
@check_login
def reco_up(request):
    name = request.session['name']
    info = json.loads(request.body)
    cur_dis = Discussion.objects.get(id=info['id'])
    if name in cur_dis.reco_list:
        return JsonResponse({
            'code': 1,
            'msg': 'you have recommended before'
        })
    else:
        cur_dis.recommend += 1
        cur_dis.reco_list.append(name)
        cur_dis.save()
        return JsonResponse({
            'code': 0,
            'msg': 'recommend successfully'
        })

@csrf_exempt
@require_POST
@check_login
def reco_down(request):
    name = request.session['name']
    info = json.loads(request.body)
    cur_dis = Discussion.objects.get(id=info['id'])
    if name in cur_dis.reco_list:
        cur_dis.recommend -= 1
        cur_dis.reco_list.remove(name)
        cur_dis.save()
        return JsonResponse({
            'code': 0,
            'msg': 'derecommend successfully'
        })
    else:
        return JsonResponse({
            'code': 1,
            'msg': 'you have not recommended yet'
        })