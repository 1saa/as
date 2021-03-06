from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from user_system.models import Papers, Discussion

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from user_system.views import check_login
from functools import wraps
# Create your views here.
#search_papers url: search/?Type=paper|discussion&Keywords =&KeywordsEntire =&KeywordsAvoid=&KeywordsAvoidEntire =&Authors =&Tags =
#return: JSON: fail--{'ret':1,'msg':'msg'},suscess--{'ret': 0,'retlist': retlist}
#search_discussion url: data/search/discussion/?tag=*&up=*(true/false)
#return: JSON: fail--{'ret':1,'msg':'msg'},suscess--{'ret': 0,'retlist': retlist}
#{
#	?Type = all|paper|discussion
#	&Keywords =
#	&KeywordsEntire =
#	&KeywordsAvoid=
#	&KeywordsAvoidEntire =
#	&Tags =
#	&Authors =
#}
#{
#	'key': int,#1+++++
#	'id': int,
#	'type': 'paper|discussion',
#	'title': str,
#	'abstract': str,
#	'tags':
#	'authors': str,
#	'publishtime':
#		paper: pubyear,
#		discussion: createtime
#	'updatetime': paper,discussion: lasttime
#}
def response_options():
    response = HttpResponse()
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response['Access-Control-Allow-Methods'] = 'GET'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def add_cors_header(response):
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response['Access-Control-Allow-Credentials'] = 'true'
    return response


def require_cors_GET(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return response_options()
        if request.method == 'GET':
            return func(request, *args, **kwargs)

    return inner


def cors_Jsresponse(*args, **kwargs):
    return add_cors_header(JsonResponse(*args, **kwargs))
    
@csrf_exempt
@require_cors_GET
#@check_login
def search_results(request):
    Type = request.GET.get('Type', None)
    if(Type):
        if(Type == 'paper'):
            return search_papers(request)
        elif(Type == 'discussion'):
            return search_discussions(request)
        else:
            return cors_Jsresponse({'ret': 1, 'msg': 'Type内容非法'})
    else:
        return getall(request)

@csrf_exempt
@require_cors_GET
#@check_login
def getall(request):
    paperset = Papers.objects.values()
    discussionset = Discussion.objects.values()
    na = request.GET.get('Keywords', None)
    na2 = request.GET.get('KeywordsEntire', None)
    na3 = request.GET.get('KeywordsAvoid', None)
    na4 = request.GET.get('KeywordsAvoidEntire', None)
    au = request.GET.get('Authors', None)
    ta = request.GET.get('Tags', None)
    if na:
        paperset = paperset.filter(name__contains=na)
        discussionset = discussionset.filter(title__contains=na)
    if na2:
        paperset = paperset.filter(name__contains=na)
        discussionset = discussionset.filter(title__contains=na)
    if na3:
        paperset = paperset.filter(name__contains=na)
        discussionset = discussionset.filter(title__contains=na)
    if na4:
        paperset = paperset.filter(name__contains=na)
        discussionset = discussionset.filter(title__contains=na)
    if au:
        paperset = paperset.filter(publisher__name=au)
        discussionset = discussionset.filter(creator=au)
    count = 0
    to_be_deleted = []
    to_be_deleted2 = []
    if ta:
        for paper in paperset:
            if ta not in paper["tag_list"]:
                to_be_deleted.append(paper["id"])
        for dis in discussionset:
            if ta not in dis["tag_list"]:
                to_be_deleted2.append(dis["id"])
    paperset = paperset.exclude(id__in=to_be_deleted)
    discussionset = discussionset.exclude(id__in=to_be_deleted2)
    retlist = []
    if paperset.exists():
        paperset = paperset.order_by('-create_time')
        for paper in paperset:
            count = count + 1
            retlist.append(
                {
                'key': count,
                'id': paper["id"],
                'type': 'paper',
                'title': paper["name"],
                'abstract':paper["information"],
                'tags': paper["tag_list"],
                'authors': paper["publisher"],
                'publishtime':paper["pubyear"],
                'updatetime':paper["last_time"],
                }
            )
    if discussionset.exists():
        discussionset = discussionset.order_by('-create_time')
        for dis_2 in discussionset:
            count = count + 1
            retlist.append(
                {
                    'key': count,
                    'id': dis_2["id"],
                    'type': 'discussion',
                    'title': dis_2["title"],
                    'abstract': '',
                    'tags': dis_2["tag_list"],
                    'authors': dis_2["creator"],
                    'publishtime': dis_2["create_time"],
                    'updatetime': dis_2["last_time"],
                }
            )
    response = cors_Jsresponse(retlist,safe=False)
    return response

@csrf_exempt
@require_cors_GET
#@check_login
def search_papers(request):
    paperset = Papers.objects.values()
    na = request.GET.get('Keywords', None)
    na2 = request.GET.get('KeywordsEntire', None)
    na3 = request.GET.get('KeywordsAvoid', None)
    na4 = request.GET.get('KeywordsAvoidEntire', None)
    au = request.GET.get('Authors', None)
    ta = request.GET.get('Tags', None)
    if na:
        paperset = paperset.filter(name__contains=na)
    if na2:
        paperset = paperset.filter(name__contains=na)
    if na3:
        paperset = paperset.filter(name__contains=na)
    if na4:
        paperset = paperset.filter(name__contains=na)
    if au:
        paperset = paperset.filter(publisher__name=au)
    count = 0
    to_be_deleted = []
    if ta:
        for paper in paperset:
            if ta not in paper["tag_list"]:
                to_be_deleted.append(paper["id"])
    paperset = paperset.exclude(id__in = to_be_deleted)
    retlist = []
    if  paperset.exists():
        paperset = paperset.order_by('-create_time')
        for paper in paperset:
            count = count + 1
            retlist.append(
                {
                    'key': count,
                    'id': paper["id"],
                    'type': 'paper',
                    'title': paper["name"],
                    'abstract': paper["information"],
                    'tags': paper["tag_list"],
                    'authors': paper["publisher"],
                    'publishtime': paper["pubyear"],
                    'updatetime': paper["last_time"],
                }
            )
    response = cors_Jsresponse(retlist,safe=False)
    return response
@csrf_exempt
@require_cors_GET
@check_login
def search_new_papers(request):
    paperset = Papers.objects.values()
    if paperset.exists():
        paperset = paperset.order_by('-create_time')
        retlist = list(paperset)
        response = cors_Jsresponse({'ret': 0,'retlist': retlist})
        return response
    else:
        response = cors_Jsresponse({'ret': 1, 'msg': '论文库为空'})
        return response

@csrf_exempt
@require_cors_GET
#@check_login
def search_discussions(request):
    discussionset = Discussion.objects.values()
    na = request.GET.get('Keywords', None)
    na2 = request.GET.get('KeywordsEntire', None)
    na3 = request.GET.get('KeywordsAvoid', None)
    na4 = request.GET.get('KeywordsAvoidEntire', None)
    au = request.GET.get('Authors', None)
    ta = request.GET.get('Tags', None)
    if na:
        discussionset = discussionset.filter(title__contains=na)
    if na2:
        discussionset = discussionset.filter(title__contains=na)
    if na3:
        discussionset = discussionset.filter(title__contains=na)
    if na4:
        discussionset = discussionset.filter(title__contains=na)
    if au:
        discussionset = discussionset.filter(creator=au)
    count = 0
    to_be_deleted = []
    retlist = []
    if ta:
        for dis in discussionset:
            if ta not in dis["tag_list"]:
                to_be_deleted.append(dis["id"])
    discussionset = discussionset.exclude(id__in=to_be_deleted)
    if discussionset.exists():
        discussionset = discussionset.order_by('-create_time')
        for dis_2 in discussionset:
            count = count + 1
            retlist.append(
                {
                    'key': count,
                    'id': dis_2["id"],
                    'type': 'discussion',
                    'title': dis_2["title"],
                    'abstract': '',
                    'tags': dis_2["tag_list"],
                    'authors': dis_2["creator"],
                    'publishtime': dis_2["create_time"],
                    'updatetime': dis_2["last_time"],
                }
            )
    response = cors_Jsresponse(retlist, safe=False)
    return response
@csrf_exempt
@require_cors_GET
@check_login
def search_hot_discussions(request):
    discussionset = Discussion.objects.values()
    if discussionset.exists():
        discussionset = discussionset.order_by('-reply_number')
        retlist = list(discussionset)
        response =  cors_Jsresponse({'ret': 0, 'retlist': retlist})
        return response
    else:
        response =  cors_Jsresponse({'ret': 1, 'msg': '找不到此类型讨论'})
        return response

@csrf_exempt
@require_cors_GET
@check_login
def search_new_discussions(request):
    discussionset = Discussion.objects.values()
    if discussionset.exists():
        discussionset = discussionset.order_by('-last_time')
        retlist = list(discussionset)
        response = cors_Jsresponse({'ret': 0, 'retlist': retlist})
        return response
    else:
        response = cors_Jsresponse({'ret': 1, 'msg': '找不到此类型讨论'})
        return response
