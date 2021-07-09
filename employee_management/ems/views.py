from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        auth.logout(request)
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('project')
            else:
                messages.error(request, 'Invalid Credentials!', extra_tags='login')
                return redirect('login')
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


def project(request):
    if not request.user.is_authenticated:
        return redirect('login')
    projects = Project.objects.all()
    length = len(projects)
    return render(request, 'projects.html', {'projects': projects, 'length': length})


def add_project(request):
    if not request.user.is_authenticated:
        return redirect('login')
    all_status = ProjectProgressStatus.objects.all()

    if request.method == 'POST':
        name = request.POST['p_name']
        status = request.POST['status']
        start_date = request.POST['start_date']
        if request.POST['end_date']:
            end_date = request.POST['end_date']
        else:
            end_date = None
        desc = request.POST['desc']
        desc = " ".join(desc.splitlines())
        status_obj = ProjectProgressStatus.objects.get(id=status)
        if end_date is not None and start_date > end_date:
            error = 'yes'
            messages.error(request, 'Please make sure the end date is after the start date')
            # return render(request, 'edit_project.html', {'status': status, 'project': project, 'end_date': end_date,
            #                                              'start_date': start_date})
            return render(request, 'add_project.html', {'status': all_status, 'error': error, 'p_name': name,
                                                        'p_status': status, 'start': start_date, 'end': end_date,
                                                        'desc': desc})
        else:
            Project.objects.create(project_name=name, project_details=desc, project_start_date=start_date,
                                   project_expected_end_date=end_date, progress_status=status_obj)
            return redirect('project')
    return render(request, 'add_project.html', {'status': all_status})


def edit_project(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    project = Project.objects.get(id=pk)
    status = ProjectProgressStatus.objects.all()
    if project.project_expected_end_date:
        end_date = project.project_expected_end_date.strftime('%Y-%m-%d')
    else:
        end_date = None
    if project.project_start_date:
        start_date = project.project_start_date.strftime('%Y-%m-%d')
    else:
        start_date = None
    if request.method == 'POST':
        name = request.POST['p_name']
        status = request.POST['status']
        start_date = request.POST['start_date']
        if request.POST['end_date']:
            end_date = request.POST['end_date']
        else:
            end_date = None
        desc = request.POST['desc']
        desc = " ".join(desc.splitlines())
        status_obj = ProjectProgressStatus.objects.get(id=status)
        if end_date is not None and start_date > end_date:
            messages.error(request, 'Please make sure the end date is after the start date')
            # return render(request, 'edit_project.html', {'status': status, 'project': project, 'end_date': end_date,
            #                                              'start_date': start_date})
            return redirect('edit_project', pk=pk)
        else:
            project.project_name = name
            project.project_details = desc
            project.project_start_date = start_date
            project.project_expected_end_date = end_date
            project.progress_status = status_obj
            project.save()
            return redirect('project')
    return render(request, 'edit_project.html', {'status': status, 'project': project, 'end_date': end_date,
                                                 'start_date': start_date})


def delete_project(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    project = Project.objects.get(id=pk)
    employees = Employee.objects.filter(project=project).update(project=None)
    project.delete()
    return redirect('project')


def employees(request):
    if not request.user.is_authenticated:
        return redirect('login')
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees})


def add_employee(request):
    if not request.user.is_authenticated:
        return redirect('login')
    roles = Role.objects.all()
    projects = Project.objects.all()
    if request.method == 'POST':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        username = request.POST['username']
        if request.POST['role']:
            role = request.POST['role']
        else:
            role = None
        address1 = request.POST['address1']
        if request.POST['dob']:
            dob = request.POST['dob']
        else:
            dob = None
        password = request.POST['pwd']
        mobile_no = request.POST['mobile']
        project = request.POST['project']
        address2 = request.POST['address2']
        gender = request.POST.get('gender')
        address1 = ", ".join(address1.splitlines())
        address2 = ", ".join(address2.splitlines())
        role_obj = Role.objects.get(id=role)
        if request.POST['project']:
            project_obj = Project.objects.get(id=project)
        else:
            project_obj = None

        if Employee.objects.filter(username=username).exists():
            error = 'yes'
            messages.error(request, 'Username Must be Unique!')
            return render(request, 'add_employee.html', {
                "error": error, 'f_name': first_name, 'l_name': last_name, 'username': username,
                'password': password, 'role': role, 'dob': dob, 'mobile_no': mobile_no, 'project': project,
                'address1': address1, 'address2': address2, 'gender': gender, 'roles': roles, 'projects': projects
            })
        else:
            if len(password)>10 or len(password)<6:
                error = 'yes'
                messages.error(request, 'password length should be between 6 to 10 character')
                return render(request, 'add_employee.html', {
                    "error": error, 'f_name': first_name, 'l_name': last_name, 'username': username,
                    'password': password, 'role': role, 'dob': dob, 'mobile_no': mobile_no, 'project': project,
                    'address1': address1, 'address2': address2, 'gender': gender, 'roles': roles, 'projects': projects
                    })
            else:
                error = 'no'
                if dob == '':
                    Employee.objects.create(first_name=first_name, last_name=last_name, username=username, password=password,
                                            gender=gender, mobile_number=mobile_no, address_1=address1,
                                            address_2=address2, role=role_obj, project=project_obj)
                else:
                    Employee.objects.create(first_name=first_name, last_name=last_name, username=username,
                                            password=password,
                                            gender=gender, date_of_birth=dob, mobile_number=mobile_no,
                                            address_1=address1,
                                            address_2=address2, role=role_obj, project=project_obj)
                User.objects.create_user(username=username, password=password)
                return redirect('employees')
    return render(request, 'add_employee.html', {'roles': roles, 'projects': projects})


def edit_employee(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    projects = Project.objects.all()
    employee = Employee.objects.get(id=pk)
    print(len(employee.username))
    user = User.objects.get(username=employee.username)
    roles = Role.objects.all()
    if request.method == 'POST':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        username = request.POST['username']
        role = request.POST['role']
        address1 = request.POST['address1']
        if request.POST['dob']:
            dob = request.POST['dob']
        else:
            dob = None
        password = request.POST['pwd']
        mobile_no = request.POST['mobile']
        project = request.POST['project']
        address2 = request.POST['address2']
        gender = request.POST.get('gender')
        address1 = ", ".join(address1.splitlines())
        address2 = ", ".join(address2.splitlines())
        role_obj = Role.objects.get(id=role)
        print(dob)
        if request.POST['project']:
            project_obj = Project.objects.get(id=project)
        else:
            project_obj = None
        if username != employee.username and Employee.objects.filter(username=username).exists():
            error = 'username'
            messages.error(request, "Username must be unique!")
            return render(request, 'edit_employee.html', {'employee': employee, 'projects': projects, 'roles': roles,
                                                          'username': username, 'error': error})
        else:
            if len(password)>10 or len(password)<6:
                error = 'password'
                messages.error(request, 'password length should be between 6 to 10 character')
                return render(request, 'edit_employee.html',
                              {'employee': employee, 'projects': projects, 'roles': roles,
                               'password': password, 'error': error})
            else:
                error = 'no'
                employee.first_name = first_name
                employee.last_name = last_name
                employee.username = username
                employee.address_1 = address1
                employee.address_2 = address2
                employee.date_of_birth = dob
                employee.mobile_number = mobile_no
                employee.gender = gender
                employee.password = password
                employee.role = role_obj
                employee.project = project_obj
                employee.save()

                user.username = username
                user.set_password(password)
                user.save()
                return redirect('employees')
    return render(request, 'edit_employee.html', {'employee': employee, 'projects': projects, 'roles': roles})


def delete_employee(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        username = Employee.objects.get(id=pk).username
        user = User.objects.get(username=username)
        user.delete()
        Employee.objects.get(id=pk).delete()
        return redirect('employees')
    except():
        return redirect('employees')


def logout(request):
    auth.logout(request)
    return redirect('login')
