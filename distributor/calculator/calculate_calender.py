from datetime import datetime
from distributor.models import Task, Process


def setup_process_dependencies():
    all_processes = Process.objects.all().prefetch_related('milestones')
    print("setup_process_dependencies()")
    for process in all_processes:
        for milestone in process.milestones.all():
            if milestone.hierarchy_in_process <= 1:
                continue
            else:
                milestone_to_add = [x for x in milestone.process.milestones.all() if x.hierarchy_in_process < milestone.hierarchy_in_process]
                print(f"{milestone} has these: {milestone_to_add}")
                milestone.initial_dependencies.add(*milestone_to_add)
                milestone.save()



def plan_raw_order():
    setup_process_dependencies()
    tasks = Task.objects.all()
    print(f"____________________________________\n" * 3)
    print("⏩⏩⏩⏩⏩ NEW RELOAD: ", datetime.now())
    print(f"____________________________________\n" * 1)

    scheduled_tasks = {}
    all_processes = Process.objects.all()

    # process_dict_overload_checker = {}
    # for process in all_processes:
    #     process_dict_overload_checker[process] = False


    position = -1
    while len(scheduled_tasks) < len(tasks) and position < 20:
        position += 1
        teams_scheduled_on_that_position = []
        # for process in process_dict_overload_checker:
        #     process_dict_overload_checker[process] = False

        # for sche_task in scheduled_tasks:
        #     if sche_task.process and task
        #         process_dict_overload_checker[sche_task.process] = False


        for task in tasks:
            print(f"▶️{position}: Looping through {task}. Index: {task.hierarchy_in_process}")
            if task in scheduled_tasks:
                print("     ⏩ Task already scheduled.")
                continue

            # if task.process and task.hierarchy_in_process > 1:
            #     if not check_if_all_prior_indexes_are_met(task, scheduled_tasks, position):
            #         print(f"    ❌ Not all prior indexes of {task} are met. Index: {task.hierarchy_in_process}")
            #         continue
            # print(f"    ✔️ {task} all prior milestones are done")

            # if task.process:
            #     if process_dict_overload_checker[task.process]:
            #         print(f"    ❌ {task.process} would overload this")
            #         # process_dict_overload_checker[task.process] = False
            #         continue

            if task.team in teams_scheduled_on_that_position:
                print(f"    ❌ The Team {task.team} has already been scheduled for this day ({position})")
                continue
            print(f"    ✔️ {task} teams has no task scheduled on same day ({position})")

            if not check_if_deps_met(task, scheduled_tasks, position):
                continue
            print(f"    ✔️ {task}'s dependencies are met. {task.initial_dependencies}")



            # if not check_if_tasks_vary(task, scheduled_tasks):
            #     print(f"    ❌ The Team {task.team} has not fulfilled other tasks yet")
            #     continue


            # for process in process_dict_overload_checker:
            #     process_dict_overload_checker[process] = False




            print(f"    ✅ {task} is now scheduled on {position}")
            scheduled_tasks[task] = position
            teams_scheduled_on_that_position.append(task.team)

            # if task.process:
            #     process_dict_overload_checker[task.process] = True
            task.position = position
            task.save()
            print(f"    ➖Scheduled Tasks List: {scheduled_tasks}")



    print("While Loop sucesfully ended")




def check_if_deps_met(task, scheduled_tasks, current_position):
    deps_of_task = task.initial_dependencies.all()
    # print("DEBUGS", deps_of_task)

    for dep in deps_of_task:
        if dep not in scheduled_tasks:
            print(f"    ❌ Dependency {dep} not scheduled.")
            return False
        if scheduled_tasks[dep] == current_position:
            print("    ❌ Dependency scheduled on same position")
            return False

    return True


def check_if_all_prior_indexes_are_met(task, scheduled_tasks, current_position):
    all_prior_indexes = [x for x in task.process.milestones.all() if x.hierarchy_in_process < task.hierarchy_in_process]
    # print(all_prior_indexes)
    for prior_index in all_prior_indexes:
        if prior_index not in scheduled_tasks:
            # print("returns false")
            return False
        if scheduled_tasks[prior_index] == current_position:
            # print("returns false because current postions")
            return False
    return True


# def check_if_tasks_vary(task, scheduled_tasks):
#     team = task.team
#     for task_of_team in team.task_set.all():
#         if task_of_team.process and task_of_team.hierarchy_in_process > 1:
#             for task_with_no_process in [x for x in team.task_set.all() if not x.process]:
#                 if task_with_no_process not in scheduled_tasks:
#                     print("This task is not scheudled: ", task_with_no_process)
#                     return False
#
#     else:
#         return True



























