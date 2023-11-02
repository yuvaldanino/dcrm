from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout # authenticaltion stuff
from django.contrib import messages
from .forms import SignUpForm
from .models import Record



# Create your views here.
def home(request):
    records = Record.objects.all()

    
    
    #check to see if loggin in 
    if request.method == 'POST':
        print("POST method detected!")
        #assign user entered username and password 
        username = request.POST['username']
        password = request.POST['password']
        #authenticate 

        user = authenticate(request, username = username, password = password)
        if user is not None:
            print("User authentication succeeded!")
            login(request, user)
            messages.success(request, "You Have Been Logged In")
            return redirect('home')
        else:
            print("User authentication failed!")
            messages.success(request, "There Was an Error Loggin In Please Try Again...")
            return redirect('home')
    else:
        print("Not a POST request!")
        return render(request, 'home.html', {'records' : records})




def logout_user(request):
    logout(request) 
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save() # if good save it 
            #authenticate and log in new user

            username = form.cleaned_data['username'] # whatever they posted and pulls out username
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "You Have Successfully Registed. Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})