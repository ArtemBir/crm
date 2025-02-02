from django.test import TestCase
from src.app.customers.models import Customer

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Artem Biryukov", phone="9876543210")

    def test_create_customer(self):
        self.assertEqual(self.customer.name, "Artem Biryukov")

    def test_customer_string_representation(self):
        self.assertEqual(str(self.customer), "Artem Biryukov 9876543210")
