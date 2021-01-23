from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Deity

#start render functions
def index(request):
    return render(request, "welcome_page.html")

def log_in_page_render(request):
    return render(request, "log_in_page.html")

def home_page_render(request):
    return render(request, "home_page.html")

def register_page_render(request):
    return render(request, "register_page.html")

def deities_by_location_page(request):
    return render(request, "deities_by_location_page.html")

def deities_by_religion_page(request):
    return render(request, "deities_by_religion_page.html")

def top_ten_page(request):
    return render(request, "top_ten_page.html")

def user_profile_page(request, user_id):
    return render(request, "user_profile_page.html")
    # doublecheck this one

def add_entry_page(request):
    return render(request, "add_entry_page.html")

def deity_info_page(request, deity_id): 
    return render(request, "deity_info_page.html")
    # doublecheck this one 

#end render pages
def back(request):
    return redirect("welcome_page.html")

def register(request):
    if request.method == "GET":
        return redirect('register_page')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('register_page')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/home_page')

def login(request):
    if request.method == "GET":
        return redirect('register_page')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('register_page')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('home_page')

def logout(request):
    request.session.clear()
    return redirect('/')