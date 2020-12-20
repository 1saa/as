from django.shortcuts import render
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import json
from user_system.models import User, Papers, Discussion, DisCenter
from user_system.views import require_cors_POST, check_login, cors_Jsresponse

@csrf_exempt
@require_cors_POST
@check_login
def create_paper(request):
    author_name = request.session['name']
    info = json.loads(request.body)
    paper_name = info['name']
    paper_puby = info['year']
    paper_pubr = info['author']
    paper_info = info['information']
    new_paper = Papers()
    new_paper.name = paper_name
    new_paper.pubyear = paper_puby
    new_paper.publisher = paper_pubr
    new_paper.information = paper_info
    new_paper.admins = [author_name]
    new_paper.save()
    return cors_Jsresponse({
        'code': 0,
        'msg': 'Create paper successfully.',
        'id': new_paper.id
    })

@csrf_exempt
@require_GET
def get_paper(request):
    pid = request.GET['id']
    cur_paper = Papers.objects.get(id=pid)
    return cors_Jsresponse({
        'id': cur_paper.id,
        'name': cur_paper.name,
        'year': cur_paper.pubyear,
        'author': cur_paper.publisher,
        'info': cur_paper.information,
        'admins': cur_paper.admins,
        'file': cur_paper.file,
        'tag': cur_paper.tag_list,
        'time': cur_paper.create_time,
        'ln': cur_paper.last_name,
        'lt': cur_paper.last_time,
    })

@csrf_exempt
@require_cors_POST
@check_login
def set_info(request):
    name = request.session['name']
    info = json.loads(request.body)
    text = info['text']
    cur_paper = Papers.objects.get(id=info['id'])
    cur_paper.edit_info(text, name)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_cors_POST
@check_login
def add_tag(request):
    add_info = json.loads(request.body)
    tag = add_info['tag']
    cur_paper = Papers.objects.get(id=add_info['id'])
    cur_paper.add_tag(tag)
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
    cur_paper = Papers.objects.get(id=delete_info['id'])
    cur_paper.delete_tag(tag)
    return cors_Jsresponse({
        'code': 0,
        'msg': 'set successfully'
    })

@csrf_exempt
@require_GET
def get_all_paper(request):
    paper_lsit = Papers.objects.values('id', 'name')
    return cors_Jsresponse({
        'paperlist': list(paper_lsit)
    })