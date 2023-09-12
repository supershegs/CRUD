import re
from rest_framework import serializers
from .models import Person
from django.core.exceptions import ValidationError

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth','phone_number', 'address']

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
    
        if re.match(r'^\d+$', first_name):
            raise serializers.ValidationError('First name can not be digit.')
        if re.match(r'^\d+$', last_name):
            raise serializers.ValidationError('Last name can not be digit.')
        if re.match(r'^\d+$', username):
            raise serializers.ValidationError('username must can not be digit.')
        if first_name == last_name:
            raise serializers.ValidationError('First name and last name cannot be the same.')
        if username == first_name or username == last_name:
            raise serializers.ValidationError('username cannot be the same as your firstname or lastname')
        return data

    def create(self, validated_data):
        # person = Person.objects.create(**validated_data)
        person = Person.objects.create(
            first_name= validated_data['first_name'],
            last_name = validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],  
            date_of_birth=validated_data['date_of_birth'],
            phone_number = validated_data['phone_number'],
            address = validated_data['address']
        )
        return person
        