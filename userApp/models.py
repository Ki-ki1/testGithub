from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

import uuid

from django.core.validators import RegexValidator
name_validator = RegexValidator(r'^[a-zA-Z\s]+$', 'Only alphabetic characters are allowed.')
userid_validator = RegexValidator(r' [USER]\d+[a-z0-9]{4}$', 'User ID must be in the format USERXXXX where X is a digit.')

def generate_user_id():
    return "user" + uuid.uuid4().hex[:4].upper() 

def validateEmail(value):
    allowed_domains = ['esprit.tn', 'univ.tn', 'mit.edu' , 'gmail.com']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f'Email domain must be one of the following: {", ".join(allowed_domains)}')


class User (AbstractUser):
    ROLE_CHOICES = [
        ('participant', 'Participant'),
        ('commiteee', 'Organization committee member'),
        
    ]
    user_id = models.CharField(max_length = 8, primary_key=True, unique=True, editable=False , validators=[userid_validator])
    first_name = models.CharField(max_length=30 , blank=True, validators=[name_validator])
    last_name = models.CharField(max_length=30,blank=True, validators=[name_validator] )
    affiliation = models.CharField(max_length=255 , blank=True , null=True)
    role = models.CharField(max_length=20 , choices=ROLE_CHOICES , default="participant")
    nationality = models.CharField(max_length=30,blank=True, null=True)
    email = models.EmailField(unique=True , validators=[validateEmail])

    def save(self, *args, **kwargs):
        if  not self.user_id:
            new_id = generate_user_id()
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_user_id()
            self.user_id = new_id
        super().save(*args, **kwargs)
            


     