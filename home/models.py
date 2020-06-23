from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_mail = models.CharField(max_length=50)
    user_password = models.CharField(max_length=20)
    user_first_name = models.CharField(max_length=20)
    user_last_name = models.CharField(max_length=20)
    user_student = models.BooleanField(default=False)
    user_worker = models.BooleanField(default=False)
    user_born = models.IntegerField()
    user_photo = models.CharField(max_length=50,blank=True)

class Vacancy(models.Model):
    vacancy_id = models.AutoField(primary_key=True)
    vacancy_user = models.ForeignKey(User,on_delete=models.CASCADE)
    vacancy_type = models.CharField(max_length=20)
    vacancy_city = models.CharField(max_length=30)
    vacancy_neighborhood = models.CharField(max_length=50)
    vacancy_adress = models.CharField(max_length=50)
    vacancy_has_smokers = models.BooleanField(default=False)
    vacancy_has_students = models.BooleanField(default=False)
    vacancy_has_workers = models.BooleanField(default=False)
    vacancy_has_animals = models.BooleanField(default=False)
    vacancy_animals_type = models.CharField(max_length=30)
    vacancy_path_photos = models.CharField(max_length=20)