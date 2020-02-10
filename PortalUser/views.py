from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *


def is_faculty(user):
    try:
        Faculty.objects.get(userid=user)
        return True
    except (Faculty.DoesNotExist):
        return False


# Create your views here.

def index(request):
    response = {}
    return render(request, 'index.html', response)

def signin(request):
    response = {}
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['pswd'])
        if user:
            login(request, user)
            return redirect("/home")
        else:
            response['invalidlogin'] = "Invalid Username or Passowrd."
            return render(request, 'index.html', response)
    return redirect("/")

def signout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def home(request):
    response={}
    user = request.user
    response['name'] = user.first_name + " " + user.last_name
    response['isLoggedin'] = True
    if is_faculty(user):
        faculty = Faculty.objects.get(userid=user)
        response['dept'] = faculty.dept
        allStudents = Student.objects.filter(faculty=faculty)
        response['isFaculty'] = True
        students = []
        for student in allStudents:
            std = User.objects.get(id=student.userid.id)
            students.append({'id': student.id, 'name': std.first_name+" "+std.last_name, 'dept': student.dept, 'course': student.course})
        response['students'] = students
        return render(request, 'facultyHome.html', response)
    else:
        student = Student.objects.get(userid=user)
        response['regno'] = student.regno
        faculty = student.faculty
        if faculty:
            guide = User.objects.get(id=faculty.userid.id)
            response['guide'] = guide.first_name + " " + guide.last_name
        else:
            response['guide'] = "Not Alloted"
        response['files'] = File.objects.filter(student = student).order_by('-date')
        return render(request, 'studentHome.html', response)

@login_required(login_url='/')
def viewDocs(request):
    response = {}
    response['isLoggedin'] = True
    studentId = request.GET['studentId']
    response['files'] = File.objects.filter(student=studentId).order_by('-date')

    return render(request, 'viewDocs.html', response)

@login_required(login_url='/')
def uploadfile(request):
    file = File()
    file.title = request.POST['title']
    file.userid = request.user
    file.path = request.FILES['file']
    file.description = request.POST['description']
    file.save()
    return render(request, 'studentHome/')

def register(request):
    response = {}
    response['departments'] = Department.objects.all()
    return render(request, 'register.html', response)

def registerFaculty(request):
    response = {}
    if request.method == "POST":
        user = User.objects.create_user(username=request.POST['username'],password=request.POST['pswd'])
        # user.username = request.POST['username']
        # user.password = request.POST['pswd']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        faculty = Faculty()
        faculty.userid = user
        faculty.dept = Department.objects.get(id=request.POST['dept'])
        faculty.save()
    return redirect('/')

def registerStudent(request):
    response = {}
    if request.method == "POST":
        user = User()
        user.username = request.POST['username']
        user.password = request.POST['pswd']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        student = Student()
        student.userid = user
        student.dept = Department.objects.get(id=request.POST['dept'])
        student.regno = request.POST['regno']
        student.course = request.POST['course']
        student.save()
    return redirect('/')

@login_required(login_url='/')
def uploadfile(request):
    file = File()
    student = Student.objects.get(userid=request.user)
    file.student = student
    file.title = request.POST['title']
    file.description = request.POST['description']
    file.path = request.FILES['file']
    file.save()
    return redirect("/home/")

@login_required(login_url='/')
def selectStudent(request):
    response = {}
    response['isLoggedin'] = True
    user = request.user
    faculty = Faculty.objects.get(userid=user)
    if request.method=="POST":
        studentId = request.POST['studentId']
        student = Student.objects.get(id=studentId)
        student.faculty = faculty
        student.save()
    response['name'] = user.first_name + " " + user.last_name
    response['dept'] = faculty.dept
    allStudents = Student.objects.filter(dept=faculty.dept, faculty=None)
    students = []
    for student in allStudents:
        std = User.objects.get(id=student.userid.id)
        students.append({'id':student.id, 'name': std.first_name+" "+std.last_name, 'dept': student.dept, 'course': student.course})
    response['students'] = students
    return render(request, 'selectStudent.html', response)
