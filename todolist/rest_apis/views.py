from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from tasks.models import Tasks


@csrf_exempt
def register(request):
    json_value = {}
    module_code = "01"
    module_status = ""
    if request.method == 'POST':
        if all(key in request.POST for key in ('username', 'password')):
            email = ''
            username = request.POST['username']
            password = request.POST['password']
            if 'email' in request.POST:
                email = request.POST['email']
            check_existing_username = User.objects.filter(username=username)
            if check_existing_username:
                module_status = "02"  # username already exist
            else:
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    password=password
                )
                module_status = "01"  # success
        else:
            module_status = "00"  # post data error, username and/or password not in post
    else:
        module_status = "00"  # method not post
    json_value['status_code'] = module_code + module_status
    return_value = json.dumps(json_value)
    return HttpResponse(return_value)


@csrf_exempt
def api_login(request):
    json_value = {}
    module_code = "02"
    module_status = ""
    if request.method == 'POST':
        if all(key in request.POST for key in ('username', 'password')):
            username = request.POST['username']
            password = request.POST['password']
            check_login = authenticate(username=username, password=password)
            if check_login:
                login(request, check_login)
                module_status = "01"  # success
            elif User.objects.filter(username=username):
                module_status = "03"  # username and password doesn't match
            else:
                module_status = "02"  # username doesn't exist
        else:
            module_status = "00"  # post data error, username and/or password not in post
    else:
        module_status = "00"  # method not post
    json_value['status_code'] = module_code + module_status
    return_value = json.dumps(json_value)
    return HttpResponse(return_value)


@csrf_exempt
def api_logout(request):
    json_value = {}
    module_code = "03"
    module_status = ""
    if request.method == 'POST':
        logout(request)
        module_status = "01"  # success
    else:
        module_status = "00"  # method not post
    json_value['status_code'] = module_code + module_status
    return_value = json.dumps(json_value)
    return HttpResponse(return_value)


@csrf_exempt
def create_task(request):
    json_value = {}
    module_code = "04"
    module_status = ""
    if request.method == 'POST':
        if request.user.is_authenticated():
            if all(key in request.POST for key in ('name', 'description', 'priority', 'state', 'due_date')):
                name = request.POST['name']
                description = request.POST['description']
                priority = request.POST['priority']
                state = request.POST['state']
                due_date = request.POST['due_date']
                if priority and state and name and description and due_date:
                    if 1 <= int(priority) <= 5 and 1 <= int(state) <= 3:
                        task_object = Tasks()
                        task_object.name = name
                        task_object.description = description
                        task_object.priority = priority
                        task_object.state = state
                        task_object.due_date = due_date
                        task_object.user = request.user
                        try:
                            task_object.save()
                            module_status = "01"  # success
                        except ValidationError:
                            module_status = "00"  # post data; date field format not correct yyyy-mm-dd
                    else:
                        module_status = "00"  # post data error
                else:
                    module_status = "00"  # post data error
            else:
                module_status = "00"  # post data error
        else:
            module_status = "02"  # user not logged in
    else:
        module_status = "00"  # method not post
    json_value['status_code'] = module_code + module_status
    return_value = json.dumps(json_value)
    return HttpResponse(return_value)


@csrf_exempt
def edit_task(request, task_id=None):
    json_value = {}
    module_code = "05"
    module_status = ""
    if request.user.is_authenticated():
        if request.method == 'POST':
            try:
                task = Tasks.objects.get(pk=task_id, user=request.user)
            except ObjectDoesNotExist:
                task = None
                module_status = "02"  # task doesn't exist
            if task:
                if all(key in request.POST for key in ('name', 'description', 'priority', 'state', 'due_date')):
                    name = request.POST['name']
                    description = request.POST['description']
                    priority = request.POST['priority']
                    state = request.POST['state']
                    due_date = request.POST['due_date']
                    if priority and state and name and description and due_date:
                        if 1 <= int(priority) <= 5 and 1 <= int(state) <= 3:
                            task.name = name
                            task.description = description
                            task.priority = priority
                            task.state = state
                            task.due_date = due_date
                            try:
                                task.save()
                                module_status = "01"  # success
                            except ValidationError:
                                module_status = "00"  # post data; date field format not correct yyyy-mm-dd
                        else:
                            module_status = "00"  # post data error
                    else:
                        module_status = "00"  # post data error
                else:
                    module_status = "00"  # post data error
        else:
            module_status = "00"  # method not post
    else:
        module_status = "03"  # user not logged in
    json_value['status_code'] = module_code + module_status
    return_value = json.dumps(json_value)
    return HttpResponse(return_value)


@csrf_exempt
def list_tasks(request):
    json_value = {}
    module_code = "06"
    module_status = ""
    if request.user.is_authenticated():
        tasks = Tasks.objects.filter(user=request.user)
        if tasks:
            json_value['tasks'] = {}
            for each_task in tasks:
                json_value['tasks'][each_task.id] = {}
                json_value['tasks'][each_task.id]['name'] = each_task.name
                json_value['tasks'][each_task.id]['description'] = each_task.description
                json_value['tasks'][each_task.id]['priority'] = each_task.get_priority_display()
                json_value['tasks'][each_task.id]['state'] = each_task.get_state_display()
                json_value['tasks'][each_task.id]['due_date'] = str(each_task.due_date)
            module_status = "01"
        else:
            module_status = "00"
    else:
        module_status = "02"
    json_value['status_code'] = module_code + module_status
    return_value = json.dumps(json_value)
    return HttpResponse(return_value)


@csrf_exempt
def delete_task(request, task_id=None):
    json_value = {}
    module_code = "07"
    module_status = ""
    if request.user.is_authenticated():
        try:
            task = Tasks.objects.get(pk=task_id, user=request.user)
        except ObjectDoesNotExist:
            task = None
            module_status = "00"  # task doesn't exist
        if task:
            task.delete()
            module_status = "01"  # success
    else:
        module_status = "02"  # user not logged in
    json_value['status_code'] = module_code + module_status
    return_value = json.dumps(json_value)
    return HttpResponse(return_value)


@csrf_exempt
def view_task(request, task_id=None):
    json_value = {}
    module_code = "08"
    module_status = ""
    if request.user.is_authenticated():
        try:
            task = Tasks.objects.get(pk=task_id, user=request.user)
        except ObjectDoesNotExist:
            task = None
            module_status = "00"  # task doesn't exist
        if task:
            json_value['task'] = {}
            json_value['task']['name'] = task.name
            json_value['task']['description'] = task.description
            json_value['task']['priority'] = task.get_priority_display()
            json_value['task']['state'] = task.get_state_display()
            json_value['task']['due_date'] = str(task.due_date)
            module_status = "01"  # success
    else:
        module_status = "02"  # user not logged in
    json_value['status_code'] = module_code + module_status
    return_value = json.dumps(json_value)
    return HttpResponse(return_value)