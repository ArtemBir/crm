from django.test import TestCase

from src.app.tech.models import Car, Customer


class CarModelTest(TestCase):
    def setUp(self):
        customer = Customer.objects.create(name="Artem Biryukov", phone="9876543210")
        self.car = Car.objects.create(make="Audi", model="B5", year=2004, color="Green", customer=customer)

    def test_create_car(self):
        self.assertEqual(self.car.make, "Audi")
        self.assertEqual(self.car.customer.name, "Artem Biryukov")

    def test_car_string_representation(self):
        self.assertEqual(str(self.car), "Audi B5 (2004) Green Customer ID: 1")

    def test_car_can_exist_without_customer(self):
        car = Car.objects.create(make="BMW", model="X5", year=2019, color="Blue", customer=None)
        self.assertIsNone(car.customer)
