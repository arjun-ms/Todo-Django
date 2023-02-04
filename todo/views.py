from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Todo
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        first_name  = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                # messages.info(request,'Username Taken')
                # return redirect('register')
                return render(request, 'register.html',{'error': "Username Taken, Try Another Username"})
            elif User.objects.filter(email=email).exists():
                # messages.info(request,'Email Taken')
                # return redirect('register')
                return render(request, 'register.html', {'error': "Email Already Registered"})
                
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                print("user created")
                return redirect('login')
        else:
            messages.info(request,"password not matching")
            return render(request, 'register.html', {'error': "Password Mismatch"})
            

    else:
        return render(request,'register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        print(user)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            return render(request,'login.html',{'error': "Invalid Credentials"})
    else:
        return render(request,'login.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('/')

def create(request):
    if request.method == 'GET' and request.user.is_authenticated:
        return render(request,'create.html')
    
    elif request.method == 'POST' and request.user.is_authenticated:
        title = request.POST['title']
        description = request.POST['description']
        completiondate = request.POST['date']
        
        today = datetime.today()
        if datetime.strptime(completiondate, '%Y-%m-%d' ).date() < today.date(): 
            return render(request, 'create.html', {'error': 'Date Cannot be Validated!'})
        
        todo = Todo(title=title,description=description,completiondate=completiondate,user=request.user)
        todo.save()
        print("Todo Created")
        
        return redirect('/home')
    
    else:
        return redirect('/')
    
def home(request):
    if request.user.is_authenticated:

        pending = True
        expired = True
        completed = True

        todos = Todo.objects.filter(user=request.user)
        today = datetime.today()

        incomplete_todos = []
        inprogress_todos = []
        completed_todos = []

        for todo in todos:
            if todo.completiondate < today.date() and not todo.completed:
                incomplete_todos.append(todo)
                if expired:
                    expired = False
            elif not todo.completed:
                inprogress_todos.append(todo)
                if pending:
                    pending = False
               
            elif todo.completed:
                completed_todos.append(todo)
                if completed:
                    completed = False
                

        render_data = {
            'todos': todos,
            'inprogress_todos': inprogress_todos,
            'incomplete_todos':  incomplete_todos,
            'completed_todos': completed_todos,
            'pending': pending,
            'expired': expired,
            'completed': completed
        }

        return render(request, 'home.html', {'render_data': render_data})
    else:
        return redirect('/')
    
def completed(request):
    if request.method == 'POST':
        obj_id = request.POST.get("object_id")
        obj = Todo.objects.get(id=obj_id)
        obj.completed = True
        obj.save()

    return redirect('/home')


# def modify(request):
#     # Updating the task
#     if request.method == 'POST' and request.user.is_authenticated:
#         print("POST WORKING")
#         task_id = request.POST.get("modify_id")
#         print("Task ID: ", task_id)
#         return render(request,'modify.html')
        
#     elif request.method == 'PUT' and request.user.is_authenticated:
        
#         print("PUT WORKING")
#         todo = Todo.objects.get(id=task_id)
#         if todo.completed == False:
#             print("IF WORKING")
#             title = request.PUT.get('title')
#             description = request.PUT.get('description')
#             completiondate = request.PUT.get('completiondate')
            
#             print("Title: ", title)
#             print("Description: ", description)
#             print("Completion Date: ", completiondate)
            
#             if not title or not description or not completiondate:
#                 print(request.POST)
                
#             todo.title = title
#             todo.description = description
#             todo.completiondate = completiondate
#             todo.save()
#             return redirect('/home')
#         else:
#             print("Task Already Completed")
        
#         # rendering the page
#         todo = Todo.objects.get(id=task_id)
#         context = {
#             'title': todo.title,
#             'description': todo.description,
#             'completiondate': todo.completiondate,
#             'id': todo.id
#         }
#         print(context)
#         return render(request,'modify.html',context)