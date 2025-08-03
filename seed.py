import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_management_tool.settings")
django.setup()

from users.models import CustomUser, Team, TeamMembership
from distributor.models import Task, TaskLoop, Project

SIZE_PRESETS = {
    "small": {"users": 5, "teams": 2, "tasks": 5},
    "medium": {"users": 15, "teams": 5, "tasks": 15},
    "large": {"users": 30, "teams": 10, "tasks": 30}
}


def run_seed():
    print("🌱 Starting seed...")

    confirm = input("⚠️  Do you want to DELETE ALL existing data? Type 'yes' to confirm: ")
    if confirm.lower() == 'yes':
        print("🧨 Deleting all existing data...")
        TeamMembership.objects.all().delete()
        TaskLoop.objects.all().delete()
        Task.objects.all().delete()
        Project.objects.all().delete()
        Team.objects.all().delete()
        CustomUser.objects.all().delete()
        print("✅ All data deleted.")
    else:
        print("ℹ️ Skipping deletion. Continuing with seeding.")

    size_choice = input("📦 Choose seed size [small, medium, large]: ").strip().lower()
    if size_choice not in SIZE_PRESETS:
        print("❌ Invalid choice. Defaulting to 'small'.")
        size_choice = "small"

    config = SIZE_PRESETS[size_choice]
    num_users = config["users"]
    num_teams = config["teams"]
    num_tasks = config["tasks"]

    print(f"\n🔧 Using config: {num_users} users, {num_teams} teams, {num_tasks} tasks\n")

    roles = ['member', 'team_lead', 'supervisor']
    team_roles = ['member', 'lead', 'observer']

    # === Users ===
    print("👤 Creating users...")
    users = []
    for i in range(1, num_users + 1):
        username = f"user{i:02}"
        email = f"{username}@example.com"
        role = random.choice(roles)
        user, _ = CustomUser.objects.get_or_create(username=username, defaults={'email': email, 'role': role})
        user.set_password("test123")
        user.save()
        users.append(user)

    # === Teams ===
    print("👥 Creating teams...")
    base_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa']
    teams = []
    for i in range(num_teams):
        name = f"Team {base_names[i % len(base_names)]}"
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        team, _ = Team.objects.get_or_create(name=name, defaults={'color': color})
        teams.append(team)

    # === Memberships ===
    print("🔗 Assigning team memberships...")
    for user in users:
        team = random.choice(teams)
        role = random.choice(team_roles)
        TeamMembership.objects.get_or_create(user=user, team=team, defaults={'role_in_team': role})

    # === Tasks & Loops ===
    print("📋 Creating tasks and loops...")
    for i in range(1, num_tasks + 1):
        task_name = f"Task {i:02}"
        team = random.choice(teams)
        loops = random.randint(1, 4)
        priority = random.randint(1, 3)
        difficulty = random.randint(1, 3)
        approval_required = random.choice([True, False])

        task, _ = Task.objects.get_or_create(
            name=task_name,
            team=team,
            defaults={
                'loops': loops,
                'priority': priority,
                'difficulty': difficulty,
                'approval_required': approval_required
            }
        )

        # Dependencies
        deps = Task.objects.exclude(id=task.id)
        if deps.exists() and random.random() < 0.3:
            task.initial_dependencies.add(random.choice(deps))

        # Create TaskLoop
        TaskLoop.objects.get_or_create(
            task=task,
            loop_index=1,
            defaults={
                'priority': priority,
                'difficulty': difficulty,
                'approval_required': approval_required,
                'scheduled_date': None
            }
        )

    # === Project timeframe ===
    print("🗓️ Creating global project timeframe...")
    Project.objects.get_or_create(
        start_date=date.today(),
        end_date=date.today() + timedelta(days=30),
        defaults={'order_counter': 0}
    )

    print("✅ Seeding completed 🎉")


if __name__ == "__main__":
    run_seed()
