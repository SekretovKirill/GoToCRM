from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
# Create your views here.
from crm.models import *


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    students = Student.objects.all()
    return render(request, 'index.html', {'students': students})

def courslist(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    courses = Course.objects.all()
    return render(request, 'courslist.html', {'courses': courses})


def details(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)
        return render(request, 'details.html', {'student': student})



def coursedet(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    course = Course.objects.get(pk=id)
    students = Student.objects.filter(course=course).all()
    return render(request, 'coursedet.html', {'course': course, 'students' : students})






def addcourse(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        return render(request, 'addcourse.html',)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        teacher = request.POST.get('teacher', '')
        if name == '' or teacher == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('//addcourse?id={}'.format(id))
        course = Course()
        course.name = name
        course.teacher = teacher
        course.save()
        return redirect('/course?id={}'.format(course.id))

def add(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        courses = Course.objects.all()
        return render(request, 'add.html', {'courses': courses})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        course_id = request.POST.get('course_id', '')
        email = request.POST.get('email', '')
        room = request.POST.get('room', '')
        description = request.POST.get('description', '')

        if name == '' or surname == '' or email == '' or room == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/add')

        student = Student()
        student.name = name
        student.surname = surname
        student.email = email
        student.room = room
        student.description = description

        if course_id != '':
            course = Course.objects.get(pk=course_id)
            student.course = course
        else:
            student.course = None
        student.save()

        return redirect('/student?id={}'.format(student.id))


def editcourse(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        id = request.GET.get('id')
        course = Course.objects.get(pk=id)
        return render(request, 'editcourse.html', {'course': course})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        teacher = request.POST.get('teacher', '')
        id = request.GET.get('id')

        if name == '' or teacher == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/editcourse?id={}'.format(id))

        course = Course.objects.get(pk=id)
        course.teacher = teacher
        course.save()

        return redirect('/course?id={}'.format(course.id))

def edit(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        id = request.GET.get('id')
        courses = Course.objects.all()
        student = Student.objects.get(pk=id)
        return render(request, 'edit.html', {'student': student, 'courses': courses})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        surname = request.POST.get('surname', '')
        course_id = request.POST.get('course_id', '')
        email = request.POST.get('email', '')
        room = request.POST.get('room', '')
        description = request.POST.get('description', '')
        id = request.GET.get('id')

        if name == '' or surname == '' or email == '' or room == '':
            messages.add_message(request, messages.ERROR, 'Заполните все поля!')
            return redirect('/edit')

        student = Student.objects.get(pk=id)
        student.name = name
        student.surname = surname
        student.email = email
        student.room = room
        student.description = description
        if course_id != '':
            course = Course.objects.get(pk=course_id)
            student.course = course
        else:
            student.course = None
        student.save()

        return redirect('/student?id={}'.format(student.id))

def delete(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    student = Student.objects.get(pk=id)
    student.delete()

    return redirect('/')


def delcourse(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    id = request.GET.get('id')
    course = Course.objects.get(pk=id)
    course.delete()
    return redirect('/courses')


class RegisterValidation(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)


class LoginValidation(forms.Form):
    login = forms.CharField(max_length=30)
    password = forms.CharField(min_length=6)

def logout_page(request):
    logout(request)
    return redirect('/login')


def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginValidation(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Проверьте правильность заполнения формы!')
            return redirect('/login')

        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.add_message(request, messages.ERROR, 'Неверные данные!')
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterValidation(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Проверьте правильность заполнения формы!')
            return redirect('/register')
        elif User.objects.filter(username=request.POST['login']).exists()==True:
            messages.add_message(request, messages.ERROR, 'Пользователь с таким логином уже существует!')
            return redirect('/register')
        else:
            user = User()
            user.username = request.POST.get('login')
            user.email = request.POST.get('email')
            user.set_password(request.POST.get('password'))
            user.save()
            login(request, user)
            return redirect('/')

