from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['GET'])
def get_info(request):
    data = {"message": "Hello from Django!"}
    return Response(data)

def get_info(request):
    return JsonResponse({"message": "This is a placeholder response"})
