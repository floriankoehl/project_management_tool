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





class TeamMembership(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='team_memberships')
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='user_memberships')

    ROLE_CHOICES = (
        ('member', 'Member'),
        ('lead', 'Team Lead'),
        ('observer', 'Observer'),
    )
    role_in_team = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'team')  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.username} in {self.team.name} ({self.role_in_team})"












