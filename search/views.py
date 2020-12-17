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
            paperset = paperset.filter(tag_list=ta)
        if paperset.exists():
            if up:
                paperset = paperset.order_by('create_time')
            else:
                paperset = paperset.order_by('-create_time')
            retlist = list(paperset)
            return JsonResponse({'ret': 0,'retlist': retlist})
        else:
            return JsonResponse({'ret': 1, 'msg': '找不到此类型论文'})

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
            discussionset = discussionset.filter(tag_list=ta)
        if discussionset.exists():
            if up:
                discussionset = discussionset.order_by('reply_number')
            else:
                discussionset = discussionset.order_by('-reply_number')
            retlist = list(discussionset)
            return JsonResponse({'ret': 0, 'retlist': retlist})
        else:
            return JsonResponse({'ret': 1, 'msg': '找不到此类型讨论'})

def response_options():
  response = HttpResponse()
  response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
  response['Access-Control-Allow-Methods'] = 'POST'
  response['Access-Control-Allow-Headers'] = 'Content-Type'
  return response
