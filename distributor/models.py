from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#FFFFFF")
    schedule_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    loops = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    approval_required = models.BooleanField(default=False)

    initial_dependencies = models.ManyToManyField("self",
                                                  symmetrical=False,
                                                  blank=True,
                                                  related_name="required_by")

    def __str__(self):
        return self.name


class TaskLoop(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    loop_index = models.IntegerField(default=1)
    scheduled_date = models.DateField(null=True, blank=True)
    defined_dependencies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="defined_dependencies_set")
    prior_loop_dependencies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="generated_dependencies_set")
    cross_loop_dependencies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="cross_loop_dependencies_set")

    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    approval_required = models.BooleanField(default=False)

    order_number = models.IntegerField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task} - {self.loop_index}"

    @property
    def all_dependencies(self):
        """
        Returns a combined queryset of all dependencies for this TaskLoop,
        including prior_loop_dependencies and cross_loop_dependencies.
        """
        return (
                self.prior_loop_dependencies.all() |
                self.cross_loop_dependencies.all() |
                self.defined_dependencies.all()
        ).distinct().order_by('task__team__name')



class ActivityLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    task_loop = models.ForeignKey(TaskLoop, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.IntegerField(null=True, blank=True)


    type = models.CharField(max_length=100)

    title = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=500)
































class Project(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()