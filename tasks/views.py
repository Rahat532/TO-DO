from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    """Display tasks for the logged-in user and handle creation.

    Only tasks owned by request.user are shown. New tasks are saved with
    owner=request.user.
    """
    form = TaskForm(request.POST or None)
    tasks = Task.objects.filter(owner=request.user).order_by("completed", "due_date")

    if request.method == "POST":
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, "Task added.")
            return redirect("tasks:task_list")

    return render(request, "tasks/task_list.html", {"tasks": tasks, "form": form})


@login_required
def toggle_task(request, pk):
    """Toggle completion for a task owned by the current user.

    Only accepts POST. If the task does not belong to the user a 404 is raised.
    """
    if request.method != "POST":
        return redirect("tasks:task_list")

    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.completed = not task.completed
    task.save(update_fields=["completed"])
    return redirect("tasks:task_list")


@login_required
def delete_task(request, pk):
    """Delete a task owned by the current user (POST only)."""
    if request.method != "POST":
        return redirect("tasks:task_list")

    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect("tasks:task_list")
