from django.contrib.auth.models import AbstractUser
from django.db import models

from main_app.compress import animal_image_folder, WEBPField
from main_app.enums import GenderEnum, VaccinationStatusEnum


class MyUser(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=100)


class Animal(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='animals')
    name = models.CharField(max_length=100)
    unicode = models.CharField(max_length=100)
    image = WEBPField(upload_to=animal_image_folder, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='animals', null=True)
    gender = models.IntegerField(choices=GenderEnum.choices)
    birthday = models.DateField()
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children_as_mother')
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children_as_father')
    popular_line = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='popular_lines')

    class Meta:
        ordering = ('-id',)


class Measurement(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='measurements')
    date = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()
    head_length = models.FloatField()
    body_length = models.FloatField()
    ear_length = models.FloatField()


class MeasurementFile(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='measurements')



class Vaccination(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='vaccinations')
    date = models.DateField()
    preparation = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=VaccinationStatusEnum.choices)


