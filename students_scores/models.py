from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=200)
    discipline = models.CharField(max_length=200)
    score = models.PositiveIntegerField()


class StudentWithDebts(models.Model):
    name = models.CharField(max_length=200)
    discipline = models.CharField(max_length=200)
    score = models.PositiveIntegerField()

    # Ограничение для предотвращения создания повторяющихся записей
    class Meta:
        unique_together = ('name', 'discipline')
