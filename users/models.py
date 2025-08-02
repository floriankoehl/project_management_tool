from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("member", "Member"),
        ("team_lead", "Team Lead"),
        ("supervisor", "Supervisor"),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


















class Team(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#FFFFFF")
    schedule_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name