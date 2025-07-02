from django.db import models


class Doctor(models.Model):
    DESIGNATIONS = (
        ('Dr.', 'Dr.'),
        ('Optician', 'Optician'),
    )
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=20, choices=DESIGNATIONS)
    hospital_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.designation} {self.name}\n{self.hospital_name}\n{self.city}"
