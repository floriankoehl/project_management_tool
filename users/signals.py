from datetime import timedelta, datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from distributor.models import Project, Task
from users.models import Message, CustomUser, TaskAssignment

@receiver(pre_save, sender=Project)
def handle_project_date_update(sender, instance, **kwargs):
    try:
        old_instance = Project.objects.get(pk=instance.pk)
    except Project.DoesNotExist:
        return

    old_date = old_instance.current_date
    new_date = instance.current_date

    if old_date == new_date:
        print("🔁 current_date unchanged, skipping.")
        return

    print(f"📅 current_date changed: {old_date} ➡️ {new_date}")

    # STEP 1: Get all tasks due on the new date
    due_tasks = Task.objects.filter(generated_deadline=new_date)

    if not due_tasks.exists():
        print("📭 No tasks due today.")
        return

    print(f"📌 {due_tasks.count()} task(s) due today.")

    # STEP 2: For each due task, send a message to the assigned user(s) only
    for task in due_tasks:
        assignments = TaskAssignment.objects.filter(task=task)

        if not assignments.exists():
            print(f"⚠️ No user assigned to task '{task.name}'")
            continue

        for assignment in assignments:
            user = assignment.user

            # STEP 3: Check if the same message already exists for this user
            message_text = f"The task '{task.name}' is due today!"
            message_type = "Deadline"

            exists = Message.objects.filter(
                user=user,
                type=message_type,
                text=message_text
            ).exists()

            if not exists:
                Message.objects.create(
                    user=user,
                    status="unread",
                    type=message_type,
                    text=message_text
                )
                print(f"📨 Sent message to {user.username} for task '{task.name}'")
            else:
                print(f"⚠️ Message already exists for {user.username} — skipping")
