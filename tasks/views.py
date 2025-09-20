from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
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


@login_required
def delete_task_ajax(request, pk):
    """Delete task via AJAX and return JSON. Expects POST."""
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request')

    task = get_object_or_404(Task, pk=pk, owner=request.user)
    # Return task data so client can offer undo
    data = {'id': task.pk, 'title': task.title, 'due_date': task.due_date.isoformat() if task.due_date else None, 'priority': task.priority}
    task.delete()
    return JsonResponse({'status': 'ok', 'task': data})


@login_required
def undo_create(request):
    """Recreate a task sent by the client (used for undo). Expects POST JSON with title, due_date (ISO) and priority."""
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request')

    title = request.POST.get('title')
    due = request.POST.get('due_date')
    priority = request.POST.get('priority') or 'medium'
    if not title:
        return JsonResponse({'status': 'error', 'message': 'Missing title'}, status=400)

    task = Task.objects.create(owner=request.user, title=title, priority=priority)
    # parse due if provided
    if due:
        from django.utils.dateparse import parse_datetime
        dt = parse_datetime(due)
        if dt:
            task.due_date = dt
            task.save(update_fields=['due_date'])

    return JsonResponse({'status': 'ok', 'task_id': task.pk})
