from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib import messages


# Create your views here.
@never_cache
def home_render(request):
    if 'user_id' in request.session and not request.user.is_superuser:
        return render(request,'home.html')
    elif 'user_id' in request.session and request.user.is_superuser:
        return redirect('adminDash')
    else:
        return redirect('sign_in')
    
@never_cache
def my_login(request):
    if 'user_id' in request.session:
        return redirect("/")
    else:
        return render(request,'login.html')

@never_cache
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error_message': 'Username is already taken'})
        Obj_user= User.objects.create_user(username=username, email=email, password=password)
        Obj_user.save()
        return redirect('sign_in')
    return render(request, 'signup.html')

@never_cache
def perform_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password = password)
        if user is not None and not user.is_superuser:
            login(request, user)
            request.session['user_id'] = user.id
            return redirect("/")
        else:
            return render(request, 'login.html', {'error_message': 'incorrect username password combination, please try again'})
    return render(request, 'login.html')

def perform_logout(request):
    logout(request)
    request.session.flush()
    return redirect('sign_in')


@never_cache
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if  user is not None and user.is_superuser:
            request.session['user_id']=user.id
            login(request, user)
            return redirect('adminDash')
        else:
            messages.info(request, 'incorrect username or password')
            return redirect('perform_admin')
    return render (request,'admin_login.html')

@never_cache       
def adminDashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user_set = User.objects.filter(is_superuser=False)
        admin_id = request.session['user_id']
        admin= User.objects.get(id=admin_id)
        admin_name = admin.username
        return render(request,'adminDashboard.html',{'userlist':user_set, 'admin_name':admin_name} )
    else:
        return redirect('sign_in')

def delete(request,pk):
    instance= User.objects.get(pk=pk)
    instance.delete()
    user_set = User.objects.filter(is_superuser=False)
    return render(request,'adminDashboard.html',{'userlist':user_set} )

@never_cache
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('adminDash')  
    return render(request, 'edit.html', {'user': user})