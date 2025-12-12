from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, FileExtensionValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Validator pour le nom
name_validator = RegexValidator(r'^[a-zA-Z\s]+$', 'Only alphabetic characters are allowed.')

# ----------------- Conference -----------------
class Conference(models.Model):
    THEMES = [
        ('CS_AI', 'Computer Science & Artificial Intelligence'),
        ('SE', 'Science & Engineering'),
        ('SSE', 'Social Sciences & Education'),
        ('IT', 'Interdisciplinary Themes'),
    ]

    name = models.CharField(max_length=200, validators=[name_validator])
    theme = models.CharField(max_length=20, choices=THEMES)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(validators=[MinLengthValidator(30, "Description must be at least 30 characters long")])

    def clean(self):
        # Vérifier que la date de début est dans le futur
        if self.start_date <= timezone.now().date():
            raise ValidationError({'start_date': 'The start date must be in the future.'})
        # Vérifier que la date de fin est après la date de début
        if self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date cannot be earlier than start date.'})

    def __str__(self):
        return self.name


# Validator pour les mots-clés
def keyword_validator(value):
    keywords = [kw.strip() for kw in value.split(',')]
    if len(keywords) > 10:
        raise ValidationError('At most 10 keywords are allowed, separated by commas.')


# ----------------- Submission -----------------
class Submission(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    abstract = models.TextField()
    keywords = models.CharField(max_length=200, validators=[keyword_validator])
    paper = models.FileField(
        upload_to='papers/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)

    # Références
    conference = models.ForeignKey('Conference', on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')

    def __str__(self):
        return f"{self.title} ({self.user})"


# ----------------- Organizing Committee -----------------
class OrganizingCommittee(models.Model):
    ROLE_CHOICES = [
        ('chair', 'Conference Chair'),
        ('co_chair', 'Conference Co-Chair'),
        ('member', 'Committee Member'),
    ]

    committee_role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    date_joined = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='committees')
    conference = models.ForeignKey('Conference', on_delete=models.CASCADE, related_name='committees')

    def __str__(self):
        return f"{self.user} - {self.committee_role} ({self.conference.name})"
