from django.db import models

# Create your models here.
class classe (models.Model):
    name = models.CharField(max_length=30)
    
class Student(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    dateBirth = models.DateField()
    classe = models.ForeignKey(classe, on_delete=models.CASCADE, related_name ='students', null=True , blank = True)


