import pytest
from src.app.tech.models import Car, CarType

@pytest.fixture
def mock_car_and_car_type(mocker):
    mock_car_type = mocker.MagicMock(spec=CarType)
    mock_car_type.make = "Audi"
    mock_car_type.model = "B5"

    mock_car = mocker.MagicMock(spec=Car)
    mock_car.year = 2004
    mock_car.color = "Green"
    mock_car.car_type = mock_car_type
    mock_car.__str__.return_value = "Audi B5 (2004) Green"

    mocker.patch("src.app.tech.models.CarType.objects.create", return_value=mock_car_type)
    mocker.patch("src.app.tech.models.Car.objects.create", return_value=mock_car)

    return mock_car, mock_car_type


def test_create_car(mock_car_and_car_type):
    mock_car, mock_car_type = mock_car_and_car_type

    car_type = CarType.objects.create(make="Audi", model="B5")
    car = Car.objects.create(year=2004, color="Green", car_type=car_type)

    assert car.car_type.make == "Audi"
    assert car.car_type.model == "B5"


def test_car_string_representation(mock_car_and_car_type):
    mock_car, _ = mock_car_and_car_type
    assert str(mock_car) == "Audi B5 (2004) Green"
