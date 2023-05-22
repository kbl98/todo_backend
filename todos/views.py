from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TodoItem
from .serializers import TodoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status





# Create your views here.

class TodoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        todos = TodoItem.objects.filter(author=request.user)
        serializer = TodoSerializer(instance=todos, many=True)
       
        return Response(serializer.data)
    
    def post(self, request):
        postreq=request.data
        print(postreq['title'])
        newTodo=TodoItem.objects.create(author=request.user,title=postreq['title'])
        serializer=TodoSerializer(instance=newTodo)
        return Response(serializer.data)
    
    def delete(self,request,id=None):

        delTodo=TodoItem.objects.filter(author=request.user)
        delTodo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

class TodoDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self,request,pk,format=None):
        print(pk)
        try:
            snippet = TodoItem.objects.get(pk=pk)
        except TodoItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

       
        serializer = TodoSerializer(snippet)
        print(serializer.data)
        return Response(serializer.data)
    
    def patch(self,request, pk,format=None):
        try:
            snippet = TodoItem.objects.get(pk=pk)
        except TodoItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
        serializer = TodoSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request, pk,format=None):
        try:
            snippet = TodoItem.objects.filter(pk=pk)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TodoItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

           
 


class  loginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })