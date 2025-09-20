from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("toggle/<int:pk>/", views.toggle_task, name="toggle_task"),
    path("delete/<int:pk>/", views.delete_task, name="delete_task"),
    path("delete_ajax/<int:pk>/", views.delete_task_ajax, name="delete_task_ajax"),
    path("undo_create/", views.undo_create, name="undo_create"),
]
