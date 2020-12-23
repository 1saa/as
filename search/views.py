from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from user_system.models import Papers, Discussion

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from user_system.views import check_login
# Create your views here.
#search_papers url: data/search/papers/?name=*&authors=*&tag=*&up=*
#return: JSON: fail--{'ret':1,'msg':'msg'},suscess--{'ret': 0,'retlist': retlist}
#search_discussion url: data/search/discussion/?tag=*&up=*(true/false)
#return: JSON: fail--{'ret':1,'msg':'msg'},suscess--{'ret': 0,'retlist': retlist}
@csrf_exempt
@require_http_methods(['GET','OPTIONS'])
@check_login
def search_papers(request):
    if (request.method == 'OPTIONS'):
        response_options()
    if request.method != 'GET':
        return JsonResponse({'ret':1,'msg':'不支持此类型的http请求'})
    else:
        paperset = Papers.objects.values()
        na = request.GET.get('name', None)
        au = request.GET.get('authors', None)
        ta = request.GET.get('tag', None)
        up = request.GET.get('up', None)
        if na:
            paperset = paperset.filter(name=na)
        if au:
            paperset = paperset.filter(authors__name=au)
        if ta:
            for q in paperset:
                count  = 0
                for p in q.tag_list:
                    if(p == ta):
                        count += 1
                        break
                if(count == 0):
                    paperset = paperset.remove(q)
        if paperset.exists():
            if up:
                paperset = paperset.order_by('create_time')
            else:
                paperset = paperset.order_by('-create_time')
            retlist = list(paperset)
            response = JsonResponse({'ret': 0,'retlist': retlist})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response
        else:
            response = JsonResponse({'ret': 1, 'msg': '找不到此类型论文'})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response
@csrf_exempt
@require_http_methods(['GET','OPTIONS'])
@check_login
def search_new_papers(request):
    if (request.method == 'OPTIONS'):
        response_options()
    if request.method != 'GET':
        return JsonResponse({'ret':1,'msg':'不支持此类型的http请求'})
    else:
        paperset = Papers.objects.values()
        if paperset.exists():
            paperset = paperset.order_by('-create_time')
            retlist = list(paperset)
            response = JsonResponse({'ret': 0,'retlist': retlist})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response
        else:
            response = JsonResponse({'ret': 1, 'msg': '论文库为空'})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response

@csrf_exempt
@require_http_methods(['GET','OPTIONS'])
@check_login
def search_discussions(request):
    if (request.method == 'OPTIONS'):
        response_options()
    if request.method != 'GET':
        return JsonResponse({'ret':1,'msg':'不支持此类型的http请求'})
    else:
        discussionset = Discussion.objects.values()
        ta = request.GET.get('tag', None)
        up = request.GET.get('up', None)
        if ta:
            for q in discussionset:
                count = 0
                for p in q.tag_list:
                    if (p == ta):
                        count += 1
                        break
                if (count == 0):
                    paperset = paperset.remove(q)
        if discussionset.exists():
            if up:
                discussionset = discussionset.order_by('reply_number')
            else:
                discussionset = discussionset.order_by('-reply_number')
            retlist = list(discussionset)
            response =  JsonResponse({'ret': 0, 'retlist': retlist})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response
        else:
            response =  JsonResponse({'ret': 1, 'msg': '找不到此类型讨论'})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response
@csrf_exempt
@require_http_methods(['GET','OPTIONS'])
@check_login
def search_hot_discussions(request):
    if (request.method == 'OPTIONS'):
        response_options()
    if request.method != 'GET':
        return JsonResponse({'ret':1,'msg':'不支持此类型的http请求'})
    else:
        discussionset = Discussion.objects.values()
        if discussionset.exists():
            discussionset = discussionset.order_by('-reply_number')
            retlist = list(discussionset)
            response =  JsonResponse({'ret': 0, 'retlist': retlist})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response
        else:
            response =  JsonResponse({'ret': 1, 'msg': '找不到此类型讨论'})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response

@csrf_exempt
@require_http_methods(['GET', 'OPTIONS'])
@check_login
def search_new_discussions(request):
    if (request.method == 'OPTIONS'):
        response_options()
    if request.method != 'GET':
        return JsonResponse({'ret': 1, 'msg': '不支持此类型的http请求'})
    else:
        discussionset = Discussion.objects.values()
        if discussionset.exists():
            discussionset = discussionset.order_by('-last_time')
            retlist = list(discussionset)
            response = JsonResponse({'ret': 0, 'retlist': retlist})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response
        else:
            response = JsonResponse({'ret': 1, 'msg': '找不到此类型讨论'})
            response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            return response
def response_options():
  response = HttpResponse()
  response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  response['Access-Control-Allow-Methods'] = 'POST'
  response['Access-Control-Allow-Headers'] = 'Content-Type'
  return response