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
    # messages = models.CharField(max_length=200)

    def __str__(self):
        return self.username




class Message(models.Model):
    status = models.CharField(max_length=50, choices=[
        ('read', 'read'),
        ('unread', 'unread'),
    ],
                              default='unread')
    type = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.text}"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.type == other.type and self.text == other.text














class Team(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#FFFFFF")
    schedule_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash(self.id)



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


class TaskAssignment(models.Model):
    task = models.ForeignKey('distributor.Task', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True)  # e.g. "Assignee", "Reviewer"
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'user')  # Prevent duplicate assignments

    def __str__(self):
        return f"{self.user.username} assigned to {self.task.name}"










