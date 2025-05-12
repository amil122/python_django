from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth import authenticate, login,logout
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def home(request):
    if 'username' in request.session:
        uname=request.session['username']
        context={
            'uname':uname
        }
        return render(request,'authentication/index.html',context)
    else:
        return render(request,'authentication/signin.html')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        cnf_password = request.POST['cnf_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('home')

        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('home')

        if password != cnf_password:
            messages.error(request, "Passwords don't match!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request,'username must be alpha numeric')
            return redirect('home')

        try:
            myuser = User.objects.create_user(username, email, password)
            myuser.save()
            messages.success(request, "Your account is created successfully")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('home')
    return render(request, 'authentication/signup.html')

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def signin(request):
    if 'username' in request.session:
        uname=request.session['username']
        context={
            'uname':uname
        }
        return render(request,'authentication/index.html',context)
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not (username):
            messages.info(request, "Please fill in all the required fields")
            return redirect('signin')
        elif not(password):
            messages.info(request, "Please fill password")
            return redirect('signin') 
        
        if user is not None:
            login(request, user)
            request.session['username']= username
            context ={
                'uname':username    
            }
            return render(request, 'authentication/index.html',context)
        else:
            messages.error(request, "Bad Credentials !!")
            return redirect('signin')
    return render(request, 'authentication/signin.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('signin')


def hello(request):
    return render(request,'authentication/hell0.html')