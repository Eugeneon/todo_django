from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),

    path('', views.index, name='home'),
    # path('task/<int:pk>/', views.index, name='form'),
    path('create/', views.create_task, name='task-create'),
    path('update/<int:pk>', views.edit_task, name='task-update'),
    path('delete/<int:pk>/', views.delete_task, name='task-delete')
]