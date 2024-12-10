from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Event
import json

class EventCreationTestCase(TestCase):

    def setUp(self):
        # Create a test user
        User.objects.filter(username='testuser').delete()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_event_creation_success(self):
        # Simulate user login
        self.client.login(username='testuser', password='testpass')

        # Define the data to be sent for creating an event
        event_data = {
            'title': 'Test Event',
            'date': '2024-10-19',
            'description': 'This is a test event description.'
        }

        # Send POST request to the 'add_event' URL without namespace
        response = self.client.post(
            reverse('add_event'),  # Removed 'events:' namespace
            data=json.dumps(event_data),
            content_type='application/json'
        )

        # Ensure the response was successful
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON data
        response_data = response.json()

        # Ensure the response contains the expected success message
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Event added successfully')

        # Ensure the event was created in the database
        event = Event.objects.get(title='Test Event')
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.date.strftime('%Y-%m-%d'), '2024-10-19')
        self.assertEqual(event.description, 'This is a test event description.')

    def test_event_creation_invalid_data(self):
        # Simulate user login
        self.client.login(username='testuser', password='testpass')

        # Define incomplete/invalid data for event creation (empty title)
        invalid_data = {
            'title': '',  # Missing title (empty string)
            'date': '2024-10-19',
            'description': 'This is a test event description.'
        }

        # Send POST request to the 'add_event' URL without namespace
        response = self.client.post(
            reverse('add_event'),  # Removed 'events:' namespace
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        # Ensure the response indicates failure
        self.assertEqual(response.status_code, 400)

        # Ensure the response contains an error status and message
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Missing or invalid required fields')

    def test_event_creation_with_invalid_method(self):
        # Simulate user login
        self.client.login(username='testuser', password='testpass')

        # Send GET request instead of POST
        response = self.client.get(reverse('add_event'))  # Removed 'events:' namespace

        # Ensure the response indicates an invalid request method
        self.assertEqual(response.status_code, 405)

        # Parse the response JSON data
        response_data = response.json()

        # Ensure the response contains an error status and message
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Invalid request method')
