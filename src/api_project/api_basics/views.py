from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import UserAPI
from .serializers import BasicSerializer, RegisterSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework.authtoken.models import Token


# Create your views here.

# generics api views
class UserListMixin(generics.ListCreateAPIView):
    queryset = UserAPI.objects.all()
    serializer_class = BasicSerializer


class UserDetailMixin(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAPI.objects.all()
    serializer_class = BasicSerializer


# class based api views
class UserList(APIView):
    def get(self, request, format=None):
        instance = UserAPI.objects.all()
        serializer = BasicSerializer(instance, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BasicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            instance = UserAPI.objects.get(pk=pk)
            return instance
        except UserAPI.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = BasicSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = BasicSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# function based api views
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        instance = UserAPI.objects.all()
        serializer = BasicSerializer(instance, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BasicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user_detail(request, pk):
    try:
        instance = UserAPI.objects.get(pk=pk)
    except UserAPI.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BasicSerializer(instance)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BasicSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        instance.delete()
        return HttpResponse(status=204)


@api_view(['POST'], )
def user_reg_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            instance = serializer.save()
            data['response'] = 'user created successfully'
            data['name'] = instance.name
            data['email'] = instance.email
            token = Token.objects.get(user=instance).key
            data['token'] = token
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
