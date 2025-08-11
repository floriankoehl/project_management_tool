from django.db import models

# Create your models here.
from users.models import Team

#Here was the team but now its in users/models.py






class Process(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)



    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


    @property  # or @cached_property if positions don’t change during the request
    def positions_of_tasks(self):
        # Use .values_list for a single field
        positions = list(self.milestones.all().values_list('position', flat=True))
        # print("positions_list", positions)  # shows in the server console
        return positions


















class Task(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=True, blank=True, related_name='milestones')
    loops = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    approval_required = models.BooleanField(default=False)
    generated_deadline = models.DateField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    hierarchy_in_process = models.IntegerField(default=0)


    initial_dependencies = models.ManyToManyField(
    "self",
    through="TaskDependency",
    through_fields=("presuccessor", "successor"),
    symmetrical=False,
    related_name="required_by",
    blank=True,
)

    def __str__(self):
        if self.process:
            return f"{self.process} - {self.name}"
        else:
            return f"{self.name}"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


    @property
    def order_numbers_of_tasks(self):
        order_numbers = []

        all_taskloops = self.taskloop_set.all()
        for taskloop in all_taskloops:
            order_numbers.append(taskloop.order_number)

        return order_numbers

    @property
    def end_number_of_tasks(self):
        # print("not even in the same function ")
        end_numbers = []

        all_taskloops = self.taskloop_set.all()
        # print(all_taskloops)
        for taskloop in all_taskloops:
            # print("in the for loop")
            print(taskloop.order_end)
            end_numbers.append(taskloop.order_end)
            # print(f"End nUmebr: {taskloop.order_end}")

        # print(end_numbers)     # print(end_numbers)
        return end_numbers

    @property
    def in_between_numbers_of_tasks(self):
        in_between_numbers = []

        all_taskloops = self.taskloop_set.all()
        for taskloop in all_taskloops:
            for in_between_number in taskloop.time_frame_orders:
                in_between_numbers.append(in_between_number)

        return in_between_numbers

    @property
    def check_if_deadline_is_met(self):
        deadline = self.generated_deadline
        current_date = Project.objects.first().current_date

        if deadline < current_date:
            return False
        else:
            return True

    @property
    def days_till_deadline(self):
        deadline = self.generated_deadline
        current_date = Project.objects.first().current_date

        return (deadline - current_date).days







from django.db import models
from django.core.exceptions import ValidationError

class TaskDependency(models.Model):
    presuccessor = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="presuccessor_set",
    )
    successor = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="successor_set",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["presuccessor", "successor"],
                name="uniq_task_dependency",
            ),
            models.CheckConstraint(
                check=~models.Q(presuccessor=models.F("successor")),
                name="no_self_dependency",
            ),
        ]

    def clean(self):
        if self.presuccessor_id == self.successor_id:
            raise ValidationError("A task cannot depend on itself.")

    def __str__(self):
        return f"Master Task: {self.presuccessor} ➝ Dependent Task: {self.successor}"
















































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

    # defined_dependencies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="defined_dependencies_set")
    # prior_loop_dependencies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="generated_dependencies_set")
    # cross_loop_dependencies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="cross_loop_dependencies_set")

    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    approval_required = models.BooleanField(default=False)

    order_number = models.IntegerField(null=True, blank=True)
    order_end = models.IntegerField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    magnitude = models.FloatField(default=0)

    def __str__(self):
        return f"{self.task} - {self.loop_index} [{self.task.generated_deadline}]"

    @property
    def duration(self):
        coefficient = 1
        # print(self.task.approval_required, "lookldjslfkj")
        if self.task.approval_required:
            coefficient = 3

        ideal_break_days = self.difficulty + coefficient
        return ideal_break_days

    @property
    def time_frame_orders(self):
        order_days = []
        counter = 0
        while self.order_number + counter < self.order_end and counter < 20:
            counter += 1
            order_days.append(counter + self.order_number)
            # print(f"append {counter} + {self.order_number}")

        return order_days[:-1]



    # @property
    # def all_dependencies(self):
    #     """
    #     Returns a combined queryset of all dependencies for this TaskLoop,
    #     including prior_loop_dependencies and cross_loop_dependencies.
    #     """
    #     return (
    #             self.prior_loop_dependencies.all() |
    #             self.cross_loop_dependencies.all() |
    #             self.defined_dependencies.all()
    #     ).distinct().order_by('task__team__name')
    #
    # @property
    # def all_required_by(self):
    #     """
    #     Returns a combined queryset of all TaskLoops that depend on this TaskLoop,
    #     whether through defined, prior_loop, or cross_loop dependencies.
    #     """
    #     return (
    #             self.defined_dependencies_set.all() |
    #             self.generated_dependencies_set.all() |
    #             self.cross_loop_dependencies_set.all()
    #     ).distinct().order_by("task__team__name")

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










class TaskLoopDependency(models.Model):
    master_task_loop = models.ForeignKey("TaskLoop",
                                         related_name="required_by",
                                         on_delete=models.CASCADE)

    dependent_task_loop = models.ForeignKey('TaskLoop',
                                            related_name="dependencies",
                                            on_delete=models.CASCADE)

    type=models.CharField(max_length=50,
                          choices=[
                              ("defined", "Defined"),
                              ("prior_loop", "Prior Loop"),
                              ("cross_loop", "Cross Loop"),
                          ]
                          )

    weight = models.FloatField(default=0)

    class Meta:
        unique_together = (("master_task_loop", "dependent_task_loop"),)

    def __str__(self):
        return f"[{self.type}]: Master Task Loop: {self.master_task_loop} ➝ Dependent Task Loop{self.dependent_task_loop}"




















class ActivityLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    task_loop = models.ForeignKey(TaskLoop, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.IntegerField(null=True, blank=True)


    type = models.CharField(max_length=100)

    title = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=500)















































from datetime import date

class Project(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    order_counter = models.IntegerField(default=0)
    current_date = models.DateField(default=date.today)
