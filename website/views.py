from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout # authenticaltion stuff
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
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

def customer_record(request, pk):
    #make it so you can view your records only if youre logged in 
    if request.user.is_authenticated:
        #look up record  (get a single object )
        customer_record  = Record.objects.get(id = pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id = pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Succesfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')
    
def add_record(request):

    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')
    
def update_record(request, pk):

    if request.user.is_authenticated:
        current_record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance = current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        else:
            return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')