from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Deity
from urllib.parse import parse_qs
import bcrypt
from django.db.models import Q

#start render functions
def index(request):
    return render(request, "welcome_page.html")

def log_in_page_render(request):
    return render(request, "log_in_page.html")

def home_page_render(request):
    context = {
        "user": User.objects.get(id = request.session['user_id']),
        "deity": Deity.objects.all(),
    }
    return render(request, "home_page.html", context)

def register_page_render(request):
    return render(request, "register_page.html")

def deities_by_location_page(request):
    return render(request, "deities_by_location_page.html")

def deities_by_religion_page(request):
    return render(request, "deities_by_religion_page.html")

def top_ten_page(request):
    return render(request, "top_ten_page.html")

def user_profile_page(request, user_id):
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request, "user_profile_page.html", context)
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
        return redirect('log_in')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('log_in')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/home_page')

def logout(request):
    request.session.clear()
    return redirect('/')

def searchbar(request):
    if request.method == "GET":
        search = request.GET["search"],
        print(search[0]),
        deity = Deity.objects.filter(Q(name__contains=search[0])|Q(location__contains=search[0])|Q(alt_name__contains=search[0])|Q(culture__contains=search[0])|Q(religion__contains=search[0])|Q(description__contains=search[0])|Q(pop_culture__contains=search[0])),

        context = {
            "user": User.objects.get(id = request.session['user_id']),
            "deity": deity,
            "search": search[0],
        }
        print(context['deity'])
        return render(request, 'search_results.html', context)

def add_deity(request):
    errors = Deity.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_entry_page')
    else:
        User.objects.get(id=request.session['user_id']),
        Deity.objects.create(
            name = request.POST['name'],
            contributor = User.objects.get(id = request.session['user_id']),
            alt_name = request.POST['alt_name'],
            culture = request.POST['culture'],
            location = request.POST['location'],
            religion = request.POST['religion'],
            description = request.POST['description'],
            pop_culture = request.POST['pop_culture'],
            source = request.POST['source']
        )
    return redirect('/home_page')