from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=100)
    schedule_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    loops = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TaskLoop(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    loop_index = models.IntegerField(default=0)
    scheduled_date = models.DateField()
    dependencies = models.ManyToManyField("self", symmetrical=False, blank=True)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    approval_required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task} - {self.loop_index}"


class Project(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()