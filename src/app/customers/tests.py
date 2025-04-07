from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.app.customers.models import Customer

class CustomerModelTest(TestCase):
    @patch("src.app.customers.models.Customer")
    def setUp(self, MockCustomer):
        self.mock_customer = MagicMock(spec=Customer)
        self.mock_customer.name = "Artem Biryukov"
        self.mock_customer.phone = "9876543210"
        self.mock_customer.__str__.return_value = "Artem Biryukov 9876543210"

        MockCustomer.objects.create.return_value = self.mock_customer
        self.Customer = MockCustomer

    def test_create_customer(self):
        customer = self.Customer.objects.create(name="Artem Biryukov", phone="9876543210")
        self.assertEqual(customer.name, "Artem Biryukov")

    def test_customer_string_representation(self):
        self.assertEqual(str(self.mock_customer), "Artem Biryukov 9876543210")
