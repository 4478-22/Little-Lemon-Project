from django.test import TestCase
from .models import Booking, Menu
from django.contrib.auth import get_user_model

User = get_user_model()

class BookingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.booking = Booking.objects.create(
            first_name='John Doe',
            reservation_date='2023-10-01',
            reservation_slot='18:00'
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.first_name, 'John Doe')
        self.assertEqual(str(self.booking.reservation_date), '2023-10-01')
        self.assertEqual(self.booking.reservation_slot, '18:00')

    def test_str_method(self):
        self.assertEqual(str(self.booking), 'John Doe - 2023-10-01 18:00')

class MenuModelTests(TestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            name='Pizza',
            description='Cheesy pizza with peppers',
            price='10.99'
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, 'Pizza')
        self.assertEqual(self.menu_item.description, 'Cheesy pizza with peppers')
        self.assertEqual(float(self.menu_item.price), 10.99)

    def test_str_method(self):
        self.assertEqual(str(self.menu_item), 'Pizza')