from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Doctor
from django.urls import reverse
from django.utils.timezone import now

class DoctorModelTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Ayaan Khan",
            "designation": "Dr.",
            "hospital_name": "City Hospital",
            "city": "Mumbai"
        }

    def test_doctor_creation(self):
        doctor = Doctor.objects.create(**self.valid_data)
        self.assertEqual(Doctor.objects.count(), 1)
        self.assertEqual(str(doctor), "Dr. Ayaan Khan\nCity Hospital\nMumbai")

    def test_created_at_auto_set(self):
        doctor = Doctor.objects.create(**self.valid_data)
        self.assertIsNotNone(doctor.created_at)

    def test_updated_at_auto_now(self):
        doctor = Doctor.objects.create(**self.valid_data)
        old_updated_at = doctor.updated_at
        doctor.hospital_name = "New Care Hospital"
        doctor.save()
        self.assertNotEqual(doctor.updated_at, old_updated_at)

    def test_ordering(self):
        Doctor.objects.create(name="Zaid", designation="Dr.", hospital_name="A", city="Delhi")
        Doctor.objects.create(name="Ayaan", designation="Dr.", hospital_name="B", city="Delhi")
        doctors = Doctor.objects.all()
        self.assertEqual(doctors[0].name, "Ayaan")


class DoctorSerializerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "name": "John Doe",
            "designation": "Dr.",
            "hospital_name": "MediCare",
            "city": "Pune"
        }

    def test_create_doctor_api(self):
        response = self.client.post(reverse('doctor-list'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_name_numeric(self):
        invalid_payload = {**self.valid_payload, "name": "John123"}
        response = self.client.post(reverse('doctor-list'), data=invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_invalid_name_symbols(self):
        invalid_payload = {**self.valid_payload, "name": "Dr. @John"}
        response = self.client.post(reverse('doctor-list'), data=invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_field_name(self):
        payload = self.valid_payload.copy()
        del payload["name"]
        response = self.client.post(reverse('doctor-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_field_designation(self):
        payload = self.valid_payload.copy()
        del payload["designation"]
        response = self.client.post(reverse('doctor-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_field_hospital(self):
        payload = self.valid_payload.copy()
        del payload["hospital_name"]
        response = self.client.post(reverse('doctor-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_field_city(self):
        payload = self.valid_payload.copy()
        del payload["city"]
        response = self.client.post(reverse('doctor-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_designation(self):
        payload = {**self.valid_payload, "designation": "Surgeon"}
        response = self.client.post(reverse('doctor-list'), data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_doctors(self):
        Doctor.objects.create(**self.valid_payload)
        response = self.client.get(reverse('doctor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_doctor(self):
        doctor = Doctor.objects.create(**self.valid_payload)
        response = self.client.get(reverse('doctor-detail', args=[doctor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_doctor(self):
        doctor = Doctor.objects.create(**self.valid_payload)
        response = self.client.put(reverse('doctor-detail', args=[doctor.id]), data={
            **self.valid_payload,
            "hospital_name": "Updated Hospital"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["hospital_name"], "Updated Hospital")

    def test_partial_update_doctor(self):
        doctor = Doctor.objects.create(**self.valid_payload)
        response = self.client.patch(reverse('doctor-detail', args=[doctor.id]), data={
            "city": "Delhi"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "Delhi")

    def test_delete_doctor(self):
        doctor = Doctor.objects.create(**self.valid_payload)
        response = self.client.delete(reverse('doctor-detail', args=[doctor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Doctor.objects.count(), 0)
