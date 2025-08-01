from datetime import timedelta, datetime

from .models import Project, TaskLoop, Team, ActivityLog, TaskLoopDependency


def plan_order_of_task_loops():
    print(f"____________________________________\n" * 3)
    print("⏩⏩⏩⏩⏩ NEW RELOAD: ", datetime.now())
    print(f"____________________________________\n" * 3)

    ActivityLog.objects.filter(type="schedule_log").delete()
    TaskLoop.objects.update(order_number=None)

    all_task_loops = sorted(TaskLoop.objects.all(), key=lambda t: t.magnitude, reverse=True)

    order_counter = -1

    while not check_if_all_task_loops_distributed():
        order_counter += 1
        # print(f"Order Counter: {order_counter}")



        for task_loop in all_task_loops:
            #Check if Task is already scheduled
            if task_loop.order_number is not None:
                continue

            # Check if Team has already scheduled task on same order number
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

            #Check if all dependencies are met and are not on the same order number
            if not check_if_dependencies_are_met(task_loop, order_counter):
                continue

            #Check if inside the team of the Taskloop, every taskloop that has a lower taskloop index is already scheduled
            if not check_if_all_loop_indexes_inside_team_are_finished(task_loop, order_counter):
                continue




            #All conditions are met here
            ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                       title="✅ [TRUE]",
                                       message=f"All conditions are met!",
                                       order_number=order_counter)
            task_loop.order_number = order_counter
            task_loop.save()
            task_loop.task.team.schedule_flag = True
            task_loop.task.team.save()

    project = Project.objects.first()
    if project:
        project.order_counter = order_counter
        project.save()

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
    dependencies = TaskLoopDependency.objects.filter(
        dependent_task_loop=task_loop
    ).select_related("master_task_loop")

    for dep in dependencies:

        master_task = dep.master_task_loop
        if master_task.order_number is None:
            ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                       title="⛔️ [SKIP] ",
                                       message=f"dependency '{master_task}' not met",
                                       order_number=order_counter)
            return False

        if master_task.order_number >= order_counter:
            ActivityLog.objects.create(task_loop=task_loop, type="schedule_log",
                                       title="⛔️ [SKIP] ",
                                       message=f"dependency '{master_task}' scheduled on same day {order_counter}",
                                       order_number=order_counter)
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
























