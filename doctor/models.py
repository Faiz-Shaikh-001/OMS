from django.db import models
from django.utils.timezone import now

class Doctor(models.Model):
    class Meta:
        ordering = ['name', 'city']
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


    DESIGNATIONS = (
        ('Dr.', 'Dr.'),
        ('Optician', 'Optician'),
    )
    name = models.CharField(
            max_length=100,
            verbose_name="Doctor's Name",
            help_text="Enter the doctor's name."
        )
    designation = models.CharField(
            max_length=20,
            choices=DESIGNATIONS,
            verbose_name="Designation",
            help_text="Enter the doctor's designation."
        )
    hospital_name = models.CharField(
            max_length=100,
            help_text="Enter the hospital name the doctor works at."
        )
    city = models.CharField(
            max_length=100,
            help_text="Enter the city where the hospital is located."
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.designation} {self.name}\n{self.hospital_name}\n{self.city}"
