from datetime import timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver
from distributor.models import Project, Task
from users.models import Message, CustomUser

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

    # STEP 2: For each due task, send a message to users
    users = CustomUser.objects.all()  # Adjust this if you want only certain users

    for task in due_tasks:
        for user in users:
            Message.objects.create(
                user=user,
                status="unread",
                type="Deadline",
                text=f"The task '{task.name}' is due today! TESSSST"
            )
            print(f"📨 Sent message to {user.username} for task '{task.name}'")
