from django.shortcuts import render
from django.http import JsonResponse 

# Create your views here.
def experiment(request):
    return JsonResponse({'username': 'Alice', 'password': 'Bob'}) 