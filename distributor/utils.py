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
