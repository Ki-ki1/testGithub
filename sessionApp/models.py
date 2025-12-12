from django.db import models
from conferenceApp.models import Conference
from django.core.exceptions import ValidationError 
from django.core.validators import RegexValidator



class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)



    def clean(self):
        if self.conference:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError(  
                    f"La date de la session doit être comprise entre les dates de la conférence "
                )
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être avant l'heure de fin.")
       






 
