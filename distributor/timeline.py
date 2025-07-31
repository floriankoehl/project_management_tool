from datetime import timedelta, datetime

from .models import Project, TaskLoop, Team, ActivityLog


def plan_order_of_task_loops():
    print(f"____________________________________\n" * 3)
    print("⏩⏩⏩⏩⏩ NEW RELOAD: ", datetime.now())
    print(f"____________________________________\n" * 3)

    ActivityLog.objects.filter(type="schedule_log").delete()
    TaskLoop.objects.update(order_number=None)

    all_task_loops = TaskLoop.objects.all()
    order_counter = -1

    while not check_if_all_task_loops_distributed():
        order_counter += 1
        # print(f"Order Counter: {order_counter}")



        for task_loop in all_task_loops:
            if task_loop.order_number is not None:
                continue

            has_conflict, conflict_task_loop = check_if_team_has_already_scheduled_task_on_same_order_counter(task_loop,
                                                                                                              order_counter)

            if has_conflict:
                ActivityLog.objects.create(
                    task_loop=task_loop,
                    type="schedule_log",
                    title="↗️ [SKIP] ",
                    message=f"Team {task_loop.task.team} already scheduled in round {order_counter} (→ {conflict_task_loop})",
                    order_number=order_counter
                )
                continue

            if not check_if_dependencies_are_met(task_loop, order_counter):

                # print(f"     ⛔️ [SKIP] Task: {task_loop} dependencies are not met")
                continue

            if not check_if_all_loop_indexes_inside_team_are_finished(task_loop, order_counter):
                continue

            #ALL CONDITIONS ARE MET
            # print(f"     ✅ [TRUE] - All conditions are met! {task_loop} is therefore scheduled")
            # print(f"    ▶️ Before")
            # print(f"        ➖ Task Loop: {task_loop}")
            # print(f"        ➖ Task Loop Order Number: {task_loop.order_number}")
            ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                       title="✅ [TRUE]",
                                       message=f"All conditions are met!",
                                       order_number=order_counter)
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
    Returns a tuple:
    - True and the conflicting TaskLoop if one exists (with same team and order_number)
    - False and None otherwise
    """
    team = task_loop.task.team

    match = TaskLoop.objects.filter(
        task__team=team,
        order_number=current_order_counter
    ).exclude(id=task_loop.id).first()

    return (match is not None, match)


def check_if_dependencies_are_met(task_loop, order_counter):
    dependencies = task_loop.all_dependencies

    for dep in dependencies:
        if dep.order_number is None:
            ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                       title="⛔️ [SKIP] ",
                                       message=f"dependency '{dep}' not met",
                                       order_number=order_counter)
            return False

        if dep.order_number >= order_counter:
            ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                       title="⛔️ [SKIP] ",
                                       message=f"dependency '{dep}' scheduled on same day {order_counter}",
                                       order_number=order_counter)
            return False
            return False

    return True

def check_if_all_loop_indexes_inside_team_are_finished(task_loop, order_counter):
    """
    Returns False if any TaskLoop in the same team with a lower loop_index is still unscheduled.
    Otherwise returns True.
    """
    current_loop_index = task_loop.loop_index
    team = task_loop.task.team

    # Get all TaskLoops from the same team with a smaller loop_index
    earlier_task_loops = TaskLoop.objects.filter(
        task__team=team,
        loop_index__lt=current_loop_index
    )

    for loop in earlier_task_loops:
        if loop.order_number is None:
            ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                       title="↗️ [SKIP] ",
                                       message=f"Not all prior task indexes finished {loop}",
                                       order_number=order_counter)
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
























