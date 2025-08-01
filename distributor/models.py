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



class Todo(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.description


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

    magnitude = models.FloatField(default=0)

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

    @property
    def all_required_by(self):
        """
        Returns a combined queryset of all TaskLoops that depend on this TaskLoop,
        whether through defined, prior_loop, or cross_loop dependencies.
        """
        return (
                self.defined_dependencies_set.all() |
                self.generated_dependencies_set.all() |
                self.cross_loop_dependencies_set.all()
        ).distinct().order_by("task__team__name")

    # @property
    # def magnitude(self):
    #     def magnitude_for(task_loop, origin_task_id, visited):
    #         if task_loop.pk in visited:
    #             return 0
    #         visited.add(task_loop.pk)
    #
    #         # Skip priority if it's from the same Task (unless it's the original)
    #         total = 0 if task_loop.task_id == origin_task_id and task_loop != self else task_loop.priority
    #
    #         for dep in task_loop.all_required_by:
    #             total += magnitude_for(dep, origin_task_id, visited)
    #         return total
    #
    #     # This TaskLoop's magnitude
    #     visited_self = set()
    #     own_magnitude = magnitude_for(self, self.task_id, visited_self)
    #
    #     # Total magnitude across all TaskLoops
    #     total_magnitude = 0
    #     for loop in TaskLoop.objects.all():
    #         visited = set()
    #         total_magnitude += magnitude_for(loop, loop.task_id, visited)
    #
    #     if total_magnitude == 0:
    #         return 0.0
    #
    #     return own_magnitude / total_magnitude


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