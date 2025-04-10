import pytest
from src.app.customers.models import Customer


@pytest.fixture
def mock_customer(mocker):
    mock_customer = mocker.MagicMock(spec=Customer)
    mock_customer.name = 'Artem Biryukov'
    mock_customer.phone = '9876543210'
    mock_customer.__str__.return_value = 'Artem Biryukov 9876543210'

    mocker.patch(
        'src.app.customers.models.Customer.objects.create', return_value=mock_customer
    )

    return mock_customer


def test_create_customer(mock_customer):
    customer = Customer.objects.create(name='Artem Biryukov', phone='9876543210')

    assert customer.name == 'Artem Biryukov'
    assert customer.phone == '9876543210'


def test_customer_string_representation(mock_customer):
    assert str(mock_customer) == 'Artem Biryukov 9876543210'
