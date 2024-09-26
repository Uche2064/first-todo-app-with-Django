from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Todo

def signin(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        authenticate_user = authenticate(username=username, password=password)
        if authenticate_user is None:
            messages.error(request, "Invalid credentials.")
            return redirect('signin')
        else:
            
            login(request, authenticate_user)
            return redirect('home')
        
    return render(request, "todoapp/signin.html",)

def signout(request: HttpRequest):
    logout(request)
    return redirect('signin')

@login_required
def home(request: HttpRequest):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title == "":
            messages.error(request, "Title cannot be empty.")
            return redirect('home')
        new_todo = Todo(user = request.user,title=title, created_at=datetime.now())
        new_todo.save()
        print(new_todo.created_at)
    all_todos = Todo.objects.filter(user = request.user)
    context = {'todos': all_todos}
    return render(request, "todoapp/home.html", context)

def register(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password) < 4:
            messages.error(request, "Password should be at least 4 characters long.")
            return redirect('register')
            
         
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, "Account created successfuly")
        authenticate_user = authenticate(username=username, password=password)
        login(request, authenticate_user)
        return redirect('home')
        
    return render(request, "todoapp/register.html",)
@login_required
def deleteTodo(request: HttpRequest, id: int):
    get_todo = Todo.objects.filter(user = request.user, id=id)
    get_todo.delete()
    return redirect('home')
@login_required
def updateTodo(request: HttpRequest, id: int):
    get_todo = Todo.objects.filter(user = request.user, id=id)
    get_todo.update(status = True)
    return redirect('home') 