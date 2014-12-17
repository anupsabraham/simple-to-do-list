from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from tasks.forms import CreateTaskForm
from tasks.models import Tasks


@login_required()
def list_tasks(request):
    temp_dict = {}
    tasks = Tasks.objects.filter(user=request.user)
    temp_dict['tasks'] = tasks
    temp_dict['today'] = datetime.today()
    return render_to_response(
        'tasks/list.html',
        temp_dict,
        context_instance=RequestContext(request)
    )


@login_required()
def create_task(request):
    temp_dict = {}
    task_form = CreateTaskForm()
    if request.POST:
        task_form = CreateTaskForm(request.POST)
        if task_form.is_valid():
            task_object = task_form.save(commit=False)
            task_object.user = request.user
            task_object.save()
            return HttpResponseRedirect('/tasks/')
    temp_dict['task_form'] = task_form
    return render_to_response(
        'tasks/create.html',
        temp_dict,
        context_instance=RequestContext(request)
    )


@login_required()
def edit_task(request, task_id=None):
    temp_dict = {}
    try:
        task = Tasks.objects.get(pk=task_id, user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    task_form = CreateTaskForm(instance=task)
    if request.POST:
        task_form = CreateTaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return HttpResponseRedirect('/tasks/')
    temp_dict['task_form'] = task_form
    return render_to_response(
        'tasks/edit.html',
        temp_dict,
        context_instance=RequestContext(request)
    )


@login_required()
def delete_task(request, task_id=None):
    temp_dict = {}
    try:
        task = Tasks.objects.get(pk=task_id, user=request.user).delete()
    except ObjectDoesNotExist:
        raise Http404
    return HttpResponseRedirect('/tasks/')