from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm, TaskStatusForm, UserForm, UserEditForm

def is_admin(user):
    return user.is_staff

@login_required
def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user).distinct().order_by('-created_at')
    return render(request, 'dashboard.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not request.user.is_staff and not task.assigned_to.filter(pk=request.user.pk).exists():
        raise Http404("Task not found or not assigned to you.")
    return render(request, 'task_detail.html', {'task': task})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not request.user.is_staff and not task.assigned_to.filter(pk=request.user.pk).exists():
        raise Http404("You cannot update this task.")
    
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskStatusForm(instance=task)
    return render(request, 'task_update.html', {'form': form, 'task': task})

@user_passes_test(is_admin)
def admin_task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'admin_task_list.html', {'tasks': tasks})

@user_passes_test(is_admin)
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            form.save_m2m()  # Important for ManyToManyField
            return redirect('admin_task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'title': 'Create Task'})

@user_passes_test(is_admin)
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return redirect('admin_task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'task': task, 'title': 'Edit Task'})

@user_passes_test(is_admin)
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('admin_task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})

# User CRUD Views
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'user_list.html', {'users': users})

@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = form.cleaned_data['role'] == 'True'
            user.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form, 'title': 'Create User'})

@user_passes_test(is_admin)
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj, request_user=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['role'] == 'True'
            
            # Update password if provided (validation handled in form)
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                
            user.save()
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user_obj, request_user=request.user)
    return render(request, 'user_form.html', {'form': form, 'user_obj': user_obj, 'title': 'Edit User'})

@user_passes_test(is_admin)
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj == request.user:
        return HttpResponseForbidden("You cannot delete your own account.")
    if request.method == 'POST':
        user_obj.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user_obj': user_obj})
