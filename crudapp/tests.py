import json
from django.test import TestCase

# Create your tests here.
from .models import Person

from .serializers import PersonSerializer
from rest_framework.exceptions import ValidationError

from django.urls import reverse
from rest_framework.test import APIClient



sample_data = [
    {
            "first_name": "Mark",  
            "last_name": "Essien",
            "username": "MarkEssien",
            "email": "MarkEssien@example.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "1234567890",
            "address": "123 Main St",
            "name": "Mark Essien"
        },

        {
            "first_name": "John",  
            "last_name": "Essien",
            "username": "JohnEssien",
            "email": "JohnEssien@example.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "1234567890",
            "address": "123 Main St",
            "name": "John Essien"
        }
]
class PersonModelTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(
            first_name="Mark",
            last_name="Essien",
            username="MarkEssien",
            email= "MarkEssien@example.com",
            date_of_birth="2000-01-01",
            phone_number="1234567890",
            address="123 Main St"
        )

    def test_person_creation(self):
        self.assertEqual(self.person.__str__(), "Mark Essien")
        self.assertEqual(self.person.first_name, "Mark")
        self.assertEqual(self.person.last_name, "Essien")
        self.assertEqual(self.person.username, "MarkEssien")
        self.assertEqual(self.person.email, "MarkEssien@example.com")
        self.assertEqual(self.person.date_of_birth, "2000-01-01")
        self.assertEqual(self.person.phone_number, "1234567890")
        self.assertEqual(self.person.address, "123 Main St")



class PersonSerializerTest(TestCase):
    def test_serializer_with_valid_data(self):
        data = {
            "first_name": "Mark",
            "last_name": "Essien",
            "username": "MarkEssien",
            "email": "MarkEssien@example.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "1234567890",
            "address": "123 Main St",
            'name' : 'Mark Essien'
        }
        serializer = PersonSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_with_invalid_data(self):
        data = {
            "first_name": "123",  # Invalid, as it contains digits
            "last_name": "Essien",
            "username": "MarkEssien",
            "email": "MarkEssien@example.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "1234567890",
            "address": "123 Main St",
            'name' : 'Mark Essien'
        }
        serializer = PersonSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn('First name can not be digit.', str(context.exception.detail))  
        self.assertEqual(str(context.exception.detail['non_field_errors'][0]), 'First name can not be digit.')
        
    def test_serializer_with_the_samedata(self):
        data = {
            "first_name": "Mark",  # the same firstname and last name
            "last_name": "Mark",
            "username": "MarkEssien",
            "email": "MarkEssien@example.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "1234567890",
            "address": "123 Main St",
            'name' : 'Mark Essien'
        }
        serializer = PersonSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn('First name and last name cannot be the same', str(context.exception.detail))  
        self.assertEqual(str(context.exception.detail['non_field_errors'][0]), 'First name and last name cannot be the same.')
    
    def test_serializer_with_the_emptydata(self):
        data = {
            "first_name": "Mark",  
            "last_name": "Mark",
            "username": "",# the username is empty/''
            "email": "MarkEssien@example.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "1234567890",
            "address": "123 Main St",
            'name' : 'Mark Essien'
        }
        serializer = PersonSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("This field may not be blank.", str(context.exception.detail))  
        self.assertEqual(str(context.exception.detail['username'][0]), 'This field may not be blank.')
    
    def test_serializer_with_the_missingdata(self):
        data = {
            "first_name": "Mark",  
            # "last_name": "Mark", last_name missing
            "username": "MarkEssien",
            "email": "MarkEssien@example.com",
            "date_of_birth": "2000-01-01",
            "phone_number": "1234567890",
            "address": "123 Main St",
            'name' : 'Mark Essien'
        }
        serializer = PersonSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertIn("This field is required.", str(context.exception.detail))  
        self.assertEqual(str(context.exception.detail['last_name'][0]), 'This field is required.')



class PersonViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person = Person.objects.create(
            first_name="Mark",
            last_name="Essien",
            username="MarkEssien",
            email= "MarkEssien@example.com",
            date_of_birth="2000-01-01",
            phone_number="1234567890",
            address="123 Main St"
        )
        self.person = Person.objects.create(
            first_name="John",
            last_name="Essien",
            username="JohnEssien",
            email= "JohnEssien@example.com",
            date_of_birth="2000-01-01",
            phone_number="1234567890",
            address="123 Main St"
        )

    #To get all person in DB
    def test_get_all_persons(self):
        url = reverse('person')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        data = json.dumps(response.data)        
        data = json.loads(data)
        self.assertEqual(data, sample_data)
    
    # Fetching details of a person.  
    def test_get_person_by_id(self):
        url = reverse('get-person-by-user_id', args=[self.person.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], "John")
        name = '{} {}'.format(response.data['first_name'], response.data['last_name'])
        self.assertEqual(response.data['name'], name)
        # person.id not found
        self.person.id = 11 # let pick a random id not in db
        url = reverse('get-person-by-user_id', args=[self.person.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'message': 'Person details not found'})

    
    # Modifying details of an existing person 
    def test_put_person_by_id(self):
        updated_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "username": "updated_username",
            "email": "updated_email@example.com",
            "date_of_birth": "2001-01-01",
            "phone_number": "9876543210",
            "address": "456 Updated St"
        }
        url = reverse('get-person-by-user_id', args=[self.person.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.data, {'message': 'Person updated successfully.'})
        self.assertEqual(response.status_code, 200)
        updated_person = Person.objects.get(pk=self.person.id)

        name = '{} {}'.format(updated_data['first_name'], updated_data['last_name'])
        self.assertEqual(updated_person.name, name)
        
        self.assertEqual(updated_person.first_name, updated_data['first_name'])
        self.assertEqual(updated_person.last_name, updated_data['last_name'])
        self.assertEqual(updated_person.username, updated_data['username'])
        self.assertEqual(updated_person.email, updated_data['email'])
        self.assertEqual(str(updated_person.date_of_birth), updated_data['date_of_birth'])
        self.assertEqual(updated_person.phone_number, updated_data['phone_number'])
        self.assertEqual(updated_person.address, updated_data['address'])
        
        # if person not found
        self.person.id = 11 # let pick a random id not in db
        url = reverse('get-person-by-user_id', args=[self.person.id])
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'message': 'Person not found'})
        
    def test_delete_person_by_id(self):
        url = reverse('get-person-by-user_id', args=[self.person.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {'message': 'Person deleted successfully.'})
        # if person not found
        self.person.id = 11 # let pick a random id not in db
        url = reverse('get-person-by-user_id', args=[self.person.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'message': 'Person not found'})

