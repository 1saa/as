from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from user_system.models import Papers, Discussion
# Create your views here.
#search_papers url: data/search/papers/?name=*&authors=*&tag=*
#return: JSON: fail--{'ret':1,'msg':'msg'},suscess--{'ret': 0,'retlist': retlist}
#search_discussion url: data/search/discussion/?tag=*
#return: JSON: fail--{'ret':1,'msg':'msg'},suscess--{'ret': 0,'retlist': retlist}
def search_papers(request):
    if request.method != 'GET':
        return JsonResponse({'ret':1,'msg':'不支持此类型的http请求'})
    else:
        paperset = Papers.objects.values()
        na = request.GET.get('name',None)
        au = request.GET.get('authors',None)#
        ta = request.GET.get('tag',None)
        if na:
            paperset = paperset.filter(name=na)
        if au:
            paperset = paperset.filter(authors=au)
        if ta:
            paperset = paperset.filter(tag_list=ta)
        if paperset.count() == 0 :
            return JsonResponse({'ret': 1, 'msg': '找不到此类型论文'})
        else:
            retlist = list(paperset)
            return JsonResponse({'ret': 0,'retlist': retlist})
def search_discussions(request):
    if request.method != 'GET':
        return JsonResponse({'ret':1,'msg':'不支持此类型的http请求'})
    else:
        discussionset = Discussion.objects.values()
        ta = request.GET.get('tag',None)
        if ta:
            discussionset = discussionset.filter(tag_list=ta)
        if discussionset.count() == 0 :
            return JsonResponse({'ret': 1, 'msg': '找不到此类型讨论'})
        else:
            retlist = list(discussionset)
            return JsonResponse({'ret': 0,'retlist': retlist})
