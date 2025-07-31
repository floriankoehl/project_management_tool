from .models import Task

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


from .models import Task, TaskLoop

def create_task_loop_objects():
    all_inital_tasks = Task.objects.all()
    TaskLoop.objects.all().delete()


    for task in all_inital_tasks:
        # if task.loops <= 1:
        #     TaskLoop.objects.create(task=task)
        # else:
        for loop in range(task.loops):
            TaskLoop.objects.create(task=task, priority=task.priority, difficulty=task.difficulty, approval_required=task.approval_required,  loop_index=loop+1)

    setup_up_prior_loop_dependencies()
    setup_up_cross_loop_dependencies()
    setup_up_inital_dependencies()



def setup_up_prior_loop_dependencies():
    all_task_loop_objects = TaskLoop.objects.all()

    for task_loop in all_task_loop_objects:
        if task_loop.loop_index > 1:
            prior_task_numbers = task_loop.loop_index - 1
            # print(f"{task_loop}:")
            for index, prior_task_loop in enumerate(range(prior_task_numbers)):
                index = index + 1
                task_loop_set_list = task_loop.task.taskloop_set.all()
                for task_loop_set_object_compare in task_loop_set_list:
                    if task_loop_set_object_compare.loop_index == index:
                        # print(f"    -This should be added: {task_loop_set_object_compare}")
                        task_loop.prior_loop_dependencies.add(task_loop_set_object_compare)
                        task_loop.save()


def setup_up_cross_loop_dependencies():
    all_task_loop_objects = TaskLoop.objects.all()

    for task_loop in all_task_loop_objects:
        if task_loop.loop_index > 1:
            # print(f"    - {task_loop} - Should have a Croos Loop")
            # print(f"    Possible cross loops are: ")
            possibel_cross_lopps = task_loop.task.required_by.all()

            for poss_cross_loop in possibel_cross_lopps:
                # print(f"            ▶️ {poss_cross_loop}")
                poss_cross_loop_loop_objects = poss_cross_loop.taskloop_set.all()


                for poss_cross_loop_loop in poss_cross_loop_loop_objects:
                    if poss_cross_loop_loop.loop_index < task_loop.loop_index:
                        task_loop.cross_loop_dependencies.add(poss_cross_loop_loop)
                        # print(f"                    🌀 {poss_cross_loop_loop}")



def setup_up_inital_dependencies():
    all_task_loop_objects = TaskLoop.objects.all()

    for task_loop in all_task_loop_objects:
        print(f"{task_loop}")
        initial_dependencies = task_loop.task.initial_dependencies.all()
        first_items = []

        for init_dep in initial_dependencies:
            dep_to_add = init_dep.taskloop_set.first()
            print(f"         - {dep_to_add}")
            task_loop.defined_dependencies.add(dep_to_add)

        # task_loop.defined_dependencies.add(initial_dependencies)