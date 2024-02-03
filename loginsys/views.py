# loginsys/views.py
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import UserProfileForm

def dashboard(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'dashboard.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'loginsys/dashboard.html')
# Create your views here.
def home(request):
    return render(request, "loginsys/index.html")
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('home')


        if User.objects.filter(username=username):
             messages.error(request, "Email already registered.")
             return redirect('home')
        

        if len(username)>10:
            messages.error(request, "Username cannot be more than 10 characters")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")

        if not username.isalnum():
            messages.error(request, "Username should be Alpha-Numeric")
            return redirect('home')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been succesfully created.")

        return redirect('signin')

    return render(request, "loginsys/signup.html")
def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "loginsys/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')

    return render(request, "loginsys/signin.html")
def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('home')
