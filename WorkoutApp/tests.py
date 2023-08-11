from django.test import TestCase
from django.urls import reverse

def test_registration(self):
    data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }
    response = self.client.post(reverse('register'), data)

    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['Location'], reverse('home'))
