from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import  PersonSerializer
from .models import Person
from rest_framework import status

class PersonView(APIView):
    def get(self, request, user_id= None):
        try:
            if user_id is None:
                person_details = Person.objects.all()
                # serializer = PersonSerializer(data=request.data)
                serializer = PersonSerializer(person_details, many= True)
            else:
                try:
                    person_details = Person.objects.get(pk=user_id)
                    serializer = PersonSerializer(person_details)
                except Person.DoesNotExist:
                    return Response({'message': 'Person details not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({'message': 'No record yet on DB.'}, status=status.HTTP_404_NOT_FOUND)   
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id, 'message': 'Person created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,  user_id= None):
        try:
            person_details = Person.objects.get(pk=user_id)
            # 
        except Person.DoesNotExist:
            return Response({'message': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PersonSerializer(person_details, data= request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({'message': 'Person updated successfully.'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,  user_id= None):
        try:
            person_details = Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            return Response({'message': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
        
        person_details.delete()
        return Response({'message': 'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    

