from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.views.decorators.cache import  never_cache,cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def admin_login(request):
    if 'user_name' in request.session:
        return redirect('admin_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if not (username):
            messages.info(request, "Please fill in all the required fields")
            return redirect('admin_login')
        elif not(password):
            messages.info(request, "Please fill password")
            return redirect('admin_login') 
        
        if user is not None and user.is_superuser:
            login(request, user)
            request.session['user_name']= username
            return redirect('admin_page')
        else:
            messages.error(request, "Bad Credentials !!")
            return redirect('admin_login')
    return render(request, 'admin_panel/admin_login.html')
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def admin_page(request):
    if 'user_name' in request.session:
        users_info = User.objects.filter(is_superuser=False)
        context = {
            'user_info': users_info,
        }
    else:
        return redirect('admin_login')
    return render(request,'admin_panel/index.html',context)



def add(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists!')
            return redirect('admin_page')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('home')
        
        users_info = User.objects.create_user(
            username = uname,
            first_name = fname,
            last_name = lname,
            email = email,
            password= password)
        users_info.save()
        return redirect('admin_page')
    return render(request,'admin_panel/index.html')

def edit(request):
    users_info = User.objects.all()
    context = {
        'user_info': users_info,
    }
    return render(request,'admin_panel/index.html',context)


def update(request,id):
    if request.method =="POST":
        uname = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        
        users_info = User(
            id = id,
            username = uname,   
            first_name = fname,
            last_name = lname,
            email = email,
        )
        users_info.save()
        return redirect('admin_page')
        
    
    return render(request,'admin_panel/index.html')

def search(request):
    if 'q' in request.GET:
        q=request.GET['q']
        user_info = User.objects.filter(username__icontains=q)
        context={
            'user_info':user_info
        }
        
    return render(request,'admin_panel/index.html',context)

def logoutt(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('admin_login')
def delete(request,id):
    
    User.objects.filter(id=id).delete()
    return redirect('admin_page')
