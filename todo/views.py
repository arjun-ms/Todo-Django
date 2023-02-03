from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

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
            return redirect('/')
        else:
            return render(request,'login.html',{'error': "Invalid Credentials"})
    else:
        return render(request,'login.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)

    return redirect('/')