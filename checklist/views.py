from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from .models import *
from .forms import *


def index(request):
    if request.user.is_authenticated:
        incomplete_count = get_incomplete_count(request.user) 
        return task_list(request)
    else:
        return redirect('login')


def get_incomplete_count(user):
    return SetTask.objects.filter(user=user, complete=False).count()


def task_list(request):
    incomplete_count = get_incomplete_count(request.user) 
    search_input = request.GET.get('search-area', '').lower()
    tasks = get_filtered_tasks(request.user, search_input)
    search = TaskSearcher()
    context = {'tasks': tasks, 'search': search, 'search_input': search_input, 'incomplete_count': incomplete_count}
    return render(request, 'checklist/task_list.html', context=context)


def get_filtered_tasks(user, search_input):
    return SetTask.objects.filter(user=user, title__icontains=search_input)


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'checklist/login.html', {'form': form})


def custom_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'checklist/register.html', {'form': form})


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.is_authenticated:
                task.user = request.user
                task.save()
                return redirect('home')
            else:
                return redirect('login')
    else:
        form = TaskForm()
    return render(request, 'checklist/task_form.html', {'form': form})



def save_task(request, form):
    task = form.save(commit=False)
    if request.user.is_authenticated:
        task.user = request.user
        task.save()
        return redirect('home')
    else:
        return redirect('login')


def delete_task(request, pk):
    task = get_object_or_404(SetTask, id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request, 'checklist/delete_warning.html', {'task': task})


def search_task(request):
    if request.user.is_authenticated:
        return task_list(request)
    else:
        return redirect('login')


def edit_task(request, pk):
        task = get_object_or_404(SetTask, id=pk)
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid:
                form.save()
                return redirect('home')
        else:
            form = TaskForm(instance=task)
        return render(request, 'checklist/task_form.html', {'form': form})
