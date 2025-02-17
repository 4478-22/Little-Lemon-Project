from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Booking, Menu

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        url = reverse('user-register')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        url = reverse('api-token-auth')
        response = self.client.post(url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class BookingViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        self.booking_data = {
            'first_name': 'John Doe',
            'reservation_date': '2023-10-01',
            'reservation_slot': '18:00'
        }

    def test_create_booking(self):
        url = reverse('bookings')
        response = self.client.post(url, self.booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reservations(self):
        Booking.objects.create(**self.booking_data)
        url = reverse('reservations')
        response = self.client.get(url, {'date': '2023-10-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'John Doe')

class MenuViewsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        self.menu_data = {
            'name': 'Pasta',
            'description': 'Delicious pasta with marinara sauce',
            'price': '12.99'
        }

    def test_create_menu_item(self):
        url = reverse('menu')
        response = self.client.post(url, self.menu_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_display_menu_item(self):
        menu_item = Menu.objects.create(**self.menu_data)
        url = reverse('menu_item', args=[menu_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Pasta')