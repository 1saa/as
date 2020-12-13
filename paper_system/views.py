from django.http import HttpResponse, JsonResponse
import json
from user_system.models import Papers, Discussion

def discussionaction(request):
    if(request.method == 'GET'):
        return get_discussions(request)
    else:
        return add_discussions(request)
def get_discussions(request):
    discussionset = Discussion.objects.values()
    na = request.GET.get('name', None)
    if na:
        discussionset= discussionset.filter(name=na).order_by('-create_time','-reply_number')
    else:
        return JsonResponse({'ret': 1, 'msg': '未指定论文名称'})
    retlist = list(discussionset)
    return JsonResponse({'noteList': retlist})
def add_discussions(request):
    request.params = json.loads(request.body)
    na = request.GET.get('name', None)
    if na:
        info = request.params['noteList']
        Discussion.objects.create(
            creater = info['name'],
            title = na,
            information=info['note'],
            create_time = info['time']
        )
        return JsonResponse({'ret': 0, 'msg': '添加成功'})
    else:
        return JsonResponse({'ret': 1, 'msg': '未指定论文名称'})