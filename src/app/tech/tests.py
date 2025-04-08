from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.app.tech.models import Car, CarType

class CarModelTest(TestCase):
    @patch("src.app.tech.models.Car")
    @patch("src.app.tech.models.CarType")
    def setUp(self, MockCarType, MockCar):
        self.mock_car_type = MagicMock(spec=CarType)
        self.mock_car_type.make = "Audi"
        self.mock_car_type.model = "B5"

        self.mock_car = MagicMock(spec=Car)
        self.mock_car.year = 2004
        self.mock_car.color = "Green"
        self.mock_car.car_type = self.mock_car_type
        self.mock_car.__str__.return_value = "Audi B5 (2004) Green"

        MockCarType.objects.create.return_value = self.mock_car_type
        MockCar.objects.create.return_value = self.mock_car

        self.CarType = MockCarType
        self.Car = MockCar

    def test_create_car(self):
        car_type = self.CarType.objects.create(make="Audi", model="B5")
        car = self.Car.objects.create(year=2004, color="Green", car_type=car_type)

        self.assertEqual(car.car_type.make, "Audi")
        self.assertEqual(car.car_type.model, "B5")

    def test_car_string_representation(self):
        self.assertEqual(str(self.mock_car), "Audi B5 (2004) Green")
