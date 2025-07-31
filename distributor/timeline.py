from datetime import timedelta, datetime

from .models import Project, TaskLoop, Team, ActivityLog


def plan_order_of_task_loops():
    print(f"____________________________________\n" * 3)
    print("⏩⏩⏩⏩⏩ NEW RELOAD: ", datetime.now())
    print(f"____________________________________\n" * 3)

    TaskLoop.objects.update(order_number=None)

    all_task_loops = TaskLoop.objects.all()
    order_counter = -1

    while not check_if_all_task_loops_distributed():
        order_counter += 1
        # print(f"Order Counter: {order_counter}")



        for task_loop in all_task_loops:
            if task_loop.order_number is not None:
                continue


            if check_if_team_has_already_scheduled_task_on_same_order_counter(task_loop, order_counter):
                # print(f"     ↗️ [SKIP] Team {task_loop.task.team} already scheduled in round {order_counter}")
                ActivityLog.objects.create(task_loop=task_loop, type="schedule_log", message=f"↗️ [SKIP] Team {task_loop.task.team} already scheduled in round {order_counter}")
                continue

            if not check_if_dependencies_are_met(task_loop, order_counter):
                ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                           message=f"⛔️ [SKIP] Task: {task_loop} dependencies are not met")
                # print(f"     ⛔️ [SKIP] Task: {task_loop} dependencies are not met")
                continue


            #ALL CONDITIONS ARE MET
            # print(f"     ✅ [TRUE] - All conditions are met! {task_loop} is therefore scheduled")
            # print(f"    ▶️ Before")
            # print(f"        ➖ Task Loop: {task_loop}")
            # print(f"        ➖ Task Loop Order Number: {task_loop.order_number}")
            ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                       message=f"✅ [TRUE] - All conditions are met! {task_loop} is therefore scheduled")
            task_loop.order_number = order_counter

            # print(f"    ▶️ After")
            # print(f"        ➖ Task Loop: {task_loop}")
            # print(f"        ➖ Task Loop Order Number: {task_loop.order_number}")
            task_loop.save()

            task_loop.task.team.schedule_flag = True
            task_loop.task.team.save()





    print(order_counter)
    return order_counter




def check_if_all_task_loops_distributed():
    all_task_loops = TaskLoop.objects.all()

    for task_loop in all_task_loops:
        if task_loop.order_number is None:
            return False

    return True

def check_if_team_has_already_scheduled_task_on_same_order_counter(task_loop, current_order_counter):
    """
    Returns True if the team of the given task_loop already has
    another task loop scheduled in the current order round.
    """
    team = task_loop.task.team

    return TaskLoop.objects.filter(
        task__team=team,
        order_number=current_order_counter
    ).exclude(id=task_loop.id).exists()

def check_if_dependencies_are_met(task_loop, order_counter):
    dependencies = task_loop.all_dependencies

    for dep in dependencies:
        if dep.order_number is None or dep.order_number >= order_counter:
            return False
    return True





























# def transform_to_boolean_list():
#     order_counter = plan_order_of_task_loops()
#     all_task_loops = TaskLoop.objects.all()
#
#     all_task_loop_boolean_dict = {}
#
#     for task_loop in all_task_loops:
#         task_loop_boolean_list = []
#         for order_number_compare in range(order_counter):
#             if task_loop.order_number == order_number_compare:
#                 task_loop_boolean_list.append(True)
#             else:
#                 task_loop_boolean_list.append(False)
#             print(f"        - {task_loop}: {task_loop_boolean_list}")
#             all_task_loop_boolean_dict[task_loop]: task_loop_boolean_list
#
#     return all_task_loop_boolean_dict
























