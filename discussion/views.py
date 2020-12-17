from django.shortcuts import render
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import json
from user_system.models import User, Discussion, DisCenter
from user_system.views import require_cors_POST, check_login, cors_Jsresponse

@csrf_exempt
@require_cors_POST
@check_login
def create_discussion(request):
    name = request.session['name']
    set_info = json.loads(request.body)
    title = set_info['title']
    info = set_info['text']
    new_dis = Discussion()
    new_dis.creator = name
    new_dis.title = title
    new_dis.add_reply(-1, info, name)
    new_dis.save()
    return cors_Jsresponse({
        'code': 0,
        'msg': 'create successfully',
        'id': new_dis.id,
    })

@csrf_exempt
@require_GET
def get_discussion(request):
    get_info = json.loads(request.body)
    cur_dis = Discussion.objects.get(id=get_info['id'])
    return cors_Jsresponse({
        'id': cur_dis.id,
        'creator': cur_dis.creator,
        'title': cur_dis.title,
        'time': cur_dis.create_time,
        'tags': cur_dis.tag_list,
        'repy_n': cur_dis.reply_number,
        'reply': cur_dis.reply,
        'last': cur_dis.last,
    })

@csrf_exempt
@require_cors_POST
@check_login
def add_tag(request):
    add_info = json.loads(request.body)
    addlist = add_info['tag']
    cur_dis = Discussion.objects.get(id=add_info['id'])
    for tag in addlist:
        if tag not in cur_dis.tag_list:
            dis_centers = DisCenter.objects.filter(tag_title=tag)
            if dis_centers.exists():
                dis_center = dis_centers[0]
                dis_center.number += 1
                dis_center.save()
        cur_dis.add_tag(tag)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_cors_POST
@check_login
def delete_tag(request):
    delete_info = json.loads(request.body)
    tag = delete_info['tag']
    cur_dis = Discussion.objects.get(id=delete_info['id'])
    if tag in cur_dis.tag_list:
        dis_centers = DisCenter.objects.filter(tag_title=tag)
        if dis_centers.exists():
            dis_center = dis_centers[0]
            dis_center.number -= 1
            dis_center.save()
    cur_dis.delete_tag(tag)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })

#reply具有两个参数，一个为整数是回复对象，0为初始讨论信息，另一个为回复字符串
@csrf_exempt
@require_cors_POST
@check_login
def reply(request):
    reply_name = request.session['name']
    info = json.loads(request.body)
    reply_to = info['to']
    reply_text = info['text']
    cur_dis = Discussion.objects.get(id=info['id'])
    cur_dis.add_reply(reply_to, reply_text, reply_name)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'reply successfully'
    })

@csrf_exempt
@require_cors_POST
@check_login
def reco_up(request):
    name = request.session['name']
    info = json.loads(request.body)
    numb = info['number']
    cur_dis = Discussion.objects.get(id=info['id'])
    if name in cur_dis.reply[numb]["recolist"]:
        return cors_Jsresponse({
            'code': 1,
            'msg': 'you have recommended before'
        })
    else:
        cur_dis.reply[numb]["reconumb"] += 1
        cur_dis.reply[numb]["recolist"].append(name)
        cur_dis.save()
        return cors_Jsresponse({
            'code': 0,
            'msg': 'recommend successfully'
        })

@csrf_exempt
@require_cors_POST
@check_login
def reco_down(request):
    name = request.session['name']
    info = json.loads(request.body)
    numb = info['number']
    cur_dis = Discussion.objects.get(id=info['id'])
    if name in cur_dis.reply[numb]["recolist"]:
        cur_dis.reply[numb]["reconumb"] -= 1
        cur_dis.reply[numb]["recolist"].remove(name)
        cur_dis.save()
        return cors_Jsresponse({
            'code': 0,
            'msg': 'derecommend successfully'
        })
    else:
        return cors_Jsresponse({
            'code': 1,
            'msg': 'you have not recommended yet'
        })

@csrf_exempt
@require_cors_POST
@check_login
def create_center(request):
    info = json.loads(request.body)
    tag = info['tag']
    new_dc = DisCenter()
    new_dc.tag_title = tag
    count = 0
    for dis in Discussion.objects.all():
        if tag in dis.tag_list:
            count += 1
    new_dc.number = count
    new_dc.save()
    return cors_Jsresponse({
        'code': 0,
        'msg': 'create a center successfully'
    })

@csrf_exempt
@require_GET
def get_center(request):
    info = json.loads(request.body)
    tag = info['tag']
    dis_centers = DisCenter.objects.filter(tag_title=tag)
    if dis_centers.exists():
        dis_center = dis_centers[0]
        return cors_Jsresponse({
            'number': dis_center.number
        })
    else:
        return cors_Jsresponse({
            'code': 1,
            'msg': 'There is no such discuss center'
        })

@csrf_exempt
@require_GET
def get_related_dis(request):
    info = json.loads(request.body)
    tag = info['tag']
    dislist = []
    for dis in Discussion.objects.all().order_by('-last.time'):
        if tag in dis.tag_list:
            udic = {}
            udic['id'] = dis.id
            udic['creator'] = dis.creator
            udic['title'] = dis.title
            udic['creatTime'] = dis.create_time
            udic['replyNumber'] = dis.reply_number
            dislist.append(udic)
    return cors_Jsresponse({
        'list': dislist
    })