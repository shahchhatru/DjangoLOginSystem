from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm


# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,"user/home.html")

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form =CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'account was created successfully for'+ user)
            print(form)
            return redirect('login')
    context={'form':form}
    return render(request,"user/register.html",context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username, password=password)
        #when we find a user
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Your username or password is incorrect")
        
    return render(request,"user/login.html")

def logoutUser(request):
    logout(request)
    return redirect('login')
