from django.db import models
from customers.models import Customer
from doctor.models import Doctor
from datetime import date

# Create your models here.
class Prescription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    checkup_date = models.DateField(default=date.today)

    # Distance vision presctiption
    distance_sphere = models.FloatField()
    distance_cylinder = models.FloatField()
    distance_axis = models.FloatField()
    distance_va = models.IntegerField()

    # Near vision prescription
    near_sphere = models.FloatField()
    near_cylinder = models.FloatField()
    near_axis = models.FloatField()
    near_va = models.IntegerField()

    # Additional magnifying power prescription for bifocal or progressive lens
    additional_sphere = models.FloatField()

    # Contact Lens values (if any)
    contact_sphere = models.FloatField()
    contact_cylinder = models.FloatField()
    contact_axis = models.FloatField()
    contact_va = models.IntegerField()

    # Pupilary Distance Adjustments
    pd_right = models.FloatField()
    pd_left = models.FloatField()

    @property
    def pd_total(self):
        return self.pd_right + self.pd_left

    def __str__(self):
        return f"Rx for {self.customer}"

