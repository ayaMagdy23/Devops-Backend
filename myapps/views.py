# from django.shortcuts import render

# # Create your views here.
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import JsonResponse

# @api_view(['GET'])
# def get_info(request):
#     data = {"message": "Hello from Django!"}
#     return Response(data)

# def get_info(request):
#     return JsonResponse({"message": "This is a placeholder response"})
# In myapps/views.py
from django.http import JsonResponse  # For regular Django views
from rest_framework.views import APIView  # For DRF views
from rest_framework.response import Response
from .models import Script  # Your model
from .serializers import ScriptSerializer  # Your serializer

# This is your regular Django view that returns a JSON response
def get_info(request):
    data = {
        'message': 'This is the information you requested.'
    }
    return JsonResponse(data)

# This is your DRF API view that handles GET and POST for Script objects
class ScriptAPIView(APIView):
    # GET method to retrieve all Script objects
    def get(self, request):
        scripts = Script.objects.all()  # Retrieve all Script objects
        serializer = ScriptSerializer(scripts, many=True)  # Serialize them
        return Response(serializer.data)

    # POST method to create a new Script object
    def post(self, request):
        serializer = ScriptSerializer(data=request.data)  # Deserialize incoming data
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save to the database
            return Response(serializer.data, status=201)  # Return the serialized data
        return Response(serializer.errors, status=400)  # Return validation errors

