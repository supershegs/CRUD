import re
from rest_framework import serializers
from .models import Person
from django.core.exceptions import ValidationError

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        # fields = '__all__'
        fields = ['first_name', 'last_name','username', 'email', 'date_of_birth','phone_number', 'address']
    def get_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = self.get_name(instance)
        return data

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
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        name = f'{first_name} {last_name}'  
        validated_data['name'] = name
        person = Person.objects.create(**validated_data)
        return person
        
    def update(self, instance, validated_data):
        # Update instance fields based on validated_data
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        # Recalculate full_name = name
        instance.name = f'{instance.first_name} {instance.last_name}'
        instance.save()
        return instance
        