from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer
from django.urls import reverse

class CustomerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
        "first_name": "Faiz",
        "last_name": "Shaikh",
        "gender": "Male",
        "age_group": "Youth (15-24)",
        "city": "Mumbai",
        "phone_number": "+911234567890",
        "second_phone_number": "+919999999999"
        }

        self.invalid_payload = {
            "first_name": "",  # Invalid: empty
            "last_name": "Shaikh",
            "gender": "Male",
            "age_group": "Youth (15-24)",
            "city": "Mumbai",
            "phone_number": ""  # Invalid: required
        }

    def test_create_valid_customer(self):
        response = self.client.post(reverse('customer-list'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(str(Customer.objects.first().phone_number), self.valid_payload["phone_number"])

    def test_create_invalid_customer(self):
        response = self.client.post(reverse('customer-list'), data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('phone_number', response.data)

    def test_get_customer_list(self):
        Customer.objects.create(
            first_name="Ayaan",
            last_name="Singh",
            gender="Male",
            age_group="Adult (25-59)",
            city="Delhi",
            phone_number="+919812345678"
        )
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_customer_str_representation(self):
        customer = Customer.objects.create(
            first_name="Sara",
            last_name="Ali",
            gender="Female",
            age_group="Youth (15-24)",
            city="Bangalore",
            phone_number="+918888888888"
        )
        expected_str = f"Sara Ali - {customer.phone_number}"
        self.assertEqual(str(customer), expected_str)

    def test_duplicate_phone_number_fails(self):
        Customer.objects.create(**self.valid_payload)
        response = self.client.post(reverse('customer-list'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)

    def test_optional_second_phone_number(self):
        payload = {
            **self.valid_payload,
            "phone_number": "+917000000001",
            "second_phone_number": None
        }
        response = self.client.post(reverse('customer-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(Customer.objects.get(phone_number="+917000000001").second_phone_number)

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer_data = {
            "first_name": "Sara",
            "last_name": "Ali",
            "city": "Bangalore",
            "gender": "Female",
            "age_group": "Adult (25-59)",
            "phone_number": "+918888888888",
            "second_phone_number": None,
        }

    def test_customer_creation(self):
        customer = Customer.objects.create(**self.customer_data)
        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.first_name, "Sara")
        self.assertEqual(customer.last_name, "Ali")

    def test_customer_str_representation(self):
        customer = Customer.objects.create(**self.customer_data)
        expected_str = "Sara Ali - +918888888888"
        self.assertEqual(str(customer), expected_str)

    def test_unique_phone_number(self):
        Customer.objects.create(**self.customer_data)
        with self.assertRaises(Exception):
            Customer.objects.create(**self.customer_data)

    def test_optional_second_phone_number(self):
        self.customer_data["second_phone_number"] = None
        customer = Customer.objects.create(**self.customer_data)
        self.assertIsNone(customer.second_phone_number)

    def test_duplicate_second_phone_number_fails(self):
        self.customer_data["second_phone_number"] = "+919999999999"
        Customer.objects.create(**self.customer_data)

    def test_customer_created_at_auto_set(self):
        customer = Customer.objects.create(**self.customer_data)
        self.assertIsNotNone(customer.created_at)

    def test_customer_updated_at_auto_set(self):
        customer = Customer.objects.create(**self.customer_data)
        self.assertIsNotNone(customer.updated_at)
