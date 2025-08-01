from .models import *


def get_valid_possible_dependencies(main_task):
    """
    Returns Task instances that can be added to main_task.initial_dependencies
    without forming a circular dependency chain.
    """

    def creates_cycle(candidate_task):
        """
        Simulates adding candidate_task as a dependency of main_task,
        and checks if this would eventually lead back to main_task.
        """
        def dfs(current_task, visited):
            if current_task == main_task:
                return True  # We've looped back – cycle detected
            if current_task in visited:
                return False  # Already checked
            visited.add(current_task)
            for dep in current_task.initial_dependencies.all():
                if dfs(dep, visited):
                    return True
            return False

        return dfs(candidate_task, set())

    all_other_tasks = Task.objects.exclude(id=main_task.id)
    valid_candidates = []

    for task in all_other_tasks:
        if not creates_cycle(task):
            valid_candidates.append(task)

    return valid_candidates







from .timeline import plan_order_of_task_loops



def create_task_loop_objects():
    all_inital_tasks = Task.objects.all()
    TaskLoop.objects.all().delete()


    for task in all_inital_tasks:
        # if task.loops <= 1:
        #     TaskLoop.objects.create(task=task)
        # else:
        for index, loop in enumerate(range(task.loops)):
            prio = (task.priority-index)
            if prio < 1:
                prio = 1

            TaskLoop.objects.create(task=task, priority=prio, difficulty=task.difficulty, approval_required=task.approval_required,  loop_index=loop+1)

    setup_up_prior_loop_dependencies()
    setup_up_cross_loop_dependencies()
    setup_up_inital_dependencies()
    cache_magnitudes()





def cache_magnitudes():
    magnitude_list = []

    for loop in TaskLoop.objects.all():
        visited = set()

        def dfs(tl):
            if tl.pk in visited:
                return 0
            visited.add(tl.pk)
            total_val = 0 if tl.task_id == loop.task_id and tl != loop else tl.priority
            for dep_relation in TaskLoopDependency.objects.filter(master_task_loop=tl).select_related(
                    "dependent_task_loop"):
                dep = dep_relation.dependent_task_loop
                total_val += dfs(dep)
            return total_val

        mag = dfs(loop)
        magnitude_list.append((loop, mag))

    # Sort by raw magnitude
    sorted_by_mag = sorted(magnitude_list, key=lambda x: x[1], reverse=True)

    # Assign a percentile score
    total_loops = len(sorted_by_mag)
    for idx, (loop, raw_mag) in enumerate(sorted_by_mag):
        percentile = 100 * (1 - idx / (total_loops - 1)) if total_loops > 1 else 100
        loop.magnitude = round(percentile, 2)
        loop.save()


# def cache_magnitudes():
#     loop_magnitudes = {}
#     total = 0
#
#     for loop in TaskLoop.objects.all():
#         visited = set()
#
#         def dfs(tl):
#             if tl.pk in visited:
#                 return 0
#             visited.add(tl.pk)
#             total_val = 0 if tl.task_id == loop.task_id and tl != loop else tl.priority
#             for dep in tl.all_required_by:
#                 total_val += dfs(dep)
#             return total_val
#
#         mag = dfs(loop)
#         loop_magnitudes[loop.pk] = mag
#         total += mag
#
#     for loop in TaskLoop.objects.all():
#         standardized = loop_magnitudes[loop.pk] / total if total else 0
#         percentage = standardized * 100
#         loop.magnitude = round(percentage, 2)
#         loop.save()




def setup_up_prior_loop_dependencies():
    all_task_loop_objects = TaskLoop.objects.all()

    for task_loop in all_task_loop_objects:
        if task_loop.loop_index > 1:
            prior_task_numbers = task_loop.loop_index - 1
            task_loop_set_list = task_loop.task.taskloop_set.all()

            for index in range(1, prior_task_numbers + 1):
                for compare_loop in task_loop_set_list:
                    if compare_loop.loop_index == index:
                        dependency_added = TaskLoopDependency.objects.create(
                            master_task_loop=compare_loop,
                            dependent_task_loop=task_loop,
                            type="prior_loop",
                            weight=1.0
                        )
                        ActivityLog.objects.create(
                                                    task_loop=task_loop,
                                                    type="setup_up_dependencies_taskloop",
                                                    title="1️⃣ Prior Loop Dependencies",
                                                    message=f"{dependency_added}"
                                                )


# def setup_up_prior_loop_dependencies():
#     all_task_loop_objects = TaskLoop.objects.all()
#
#     for task_loop in all_task_loop_objects:
#         if task_loop.loop_index > 1:
#             prior_task_numbers = task_loop.loop_index - 1
#             # print(f"{task_loop}:")
#             for index, prior_task_loop in enumerate(range(prior_task_numbers)):
#                 index = index + 1
#                 task_loop_set_list = task_loop.task.taskloop_set.all()
#                 for task_loop_set_object_compare in task_loop_set_list:
#                     if task_loop_set_object_compare.loop_index == index:
#                         # print(f"    -This should be added: {task_loop_set_object_compare}")
#                         ActivityLog.objects.create(
#                             task_loop=task_loop,
#                             type="setup_up_dependencies_taskloop",
#                             title="1️⃣ Prior Loop Dependencies",
#                             message=f"Dependency {task_loop_set_object_compare} was added"
#                         )
#                         task_loop.prior_loop_dependencies.add(task_loop_set_object_compare)
#                         task_loop.save()






#TODO might crass if 'required_by' attribute is now different. Might have to look at it later if something crashes
def setup_up_cross_loop_dependencies():
    all_task_loop_objects = TaskLoop.objects.all()

    for task_loop in all_task_loop_objects:
        if task_loop.loop_index > 1:
            possible_cross_tasks = task_loop.task.required_by.all()

            for cross_task in possible_cross_tasks:
                for cross_loop in cross_task.taskloop_set.all():
                    if cross_loop.loop_index < task_loop.loop_index:
                        dependency_added = TaskLoopDependency.objects.create(
                            master_task_loop=cross_loop,
                            dependent_task_loop=task_loop,
                            type="cross_loop",
                            weight=1.0
                        )
                        ActivityLog.objects.create(
                            task_loop=task_loop,
                            type="setup_up_dependencies_taskloop",
                            title="2️⃣ Cross Loop Dependencies",
                            message=f"{dependency_added}"
                        )
























# def setup_up_cross_loop_dependencies():
#     all_task_loop_objects = TaskLoop.objects.all()
#
#     for task_loop in all_task_loop_objects:
#         if task_loop.loop_index > 1:
#             # print(f"    - {task_loop} - Should have a Croos Loop")
#             # print(f"    Possible cross loops are: ")
#             possibel_cross_lopps = task_loop.task.required_by.all()
#
#             for poss_cross_loop in possibel_cross_lopps:
#                 # print(f"            ▶️ {poss_cross_loop}")
#                 poss_cross_loop_loop_objects = poss_cross_loop.taskloop_set.all()
#
#
#                 for poss_cross_loop_loop in poss_cross_loop_loop_objects:
#                     if poss_cross_loop_loop.loop_index < task_loop.loop_index:
#                         ActivityLog.objects.create(
#                             task_loop=task_loop,
#                             type="setup_up_dependencies_taskloop",
#                             title="2️⃣ Cross Loop Dependencies",
#                             message=f"Dependency {poss_cross_loop_loop} was added"
#                         )
#                         task_loop.cross_loop_dependencies.add(poss_cross_loop_loop)
#                         # print(f"                    🌀 {poss_cross_loop_loop}")



















def setup_up_inital_dependencies():
    all_task_loop_objects = TaskLoop.objects.all()

    for task_loop in all_task_loop_objects:
        initial_dependencies = task_loop.task.initial_dependencies.all()

        for init_dep in initial_dependencies:
            dep_to_add = init_dep.taskloop_set.first()
            if dep_to_add:
                dependency_added = TaskLoopDependency.objects.create(
                    master_task_loop=dep_to_add,
                    dependent_task_loop=task_loop,
                    type="defined",
                    weight=1.0
                )
                ActivityLog.objects.create(
                    task_loop=task_loop,
                    type="setup_up_dependencies_taskloop",
                    title="3️⃣ Cross Loop Dependencies",
                    message=f"{dependency_added}"
                )









#
# def setup_up_inital_dependencies():
#     all_task_loop_objects = TaskLoop.objects.all()
#
#     for task_loop in all_task_loop_objects:
#         # print(f"{task_loop}")
#         initial_dependencies = task_loop.task.initial_dependencies.all()
#         first_items = []
#
#         for init_dep in initial_dependencies:
#             dep_to_add = init_dep.taskloop_set.first()
#             print(f"         - {dep_to_add}")
#             ActivityLog.objects.create(
#                 task_loop=task_loop,
#                 type="setup_up_dependencies_taskloop",
#                 title="3️⃣ Cross Loop Dependencies",
#                 message=f"Dependency {dep_to_add} was added"
#             )
#
#
#             task_loop.defined_dependencies.add(dep_to_add)
#
#         # task_loop.defined_dependencies.add(initial_dependencies)