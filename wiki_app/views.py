from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Deity
from urllib.parse import parse_qs
import bcrypt
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity



#start render functions
def index(request):
    context = {
        "deity_count": Deity.objects.count(),
        "user_count": User.objects.count(),
        "deity": Deity.objects.all().order_by('-created_at')[0:10]
    }
    return render(request, "welcome_page.html", context)

def log_in_page_render(request):
    return render(request, "log_in_page.html")

def home_page_render(request):
    
    context = {
        "user": User.objects.get(id = request.session['user_id']),
        "deity": Deity.objects.all().order_by('-created_at')[0:10],
        "deity_sidebar_L": Deity.objects.values('location').distinct().order_by('location'),
        "deity_sidebar_R": Deity.objects.values('religion').distinct().order_by('religion'),
    }
    return render(request, "home_page.html", context)

def register_page_render(request):
    return render(request, "register_page.html")

def deities_by_location_page(request, deity_location):
        context = {
            "user": User.objects.get(id = request.session['user_id']),
            "deity": Deity.objects.filter(location = deity_location),
            "deity_location": deity_location,
        }
        return render(request, "deities_by_location_page.html", context)

def deities_by_religion_page(request, deity_religion):
        context = {
            "user": User.objects.get(id = request.session['user_id']),
            "deity": Deity.objects.filter(religion = deity_religion),
            "deity_religion": deity_religion,
        }
        return render(request, "deities_by_religion_page.html", context)

def user_profile_page(request, user_id):
    context = {
        "user": User.objects.get(id=user_id),
        "deity": Deity.objects.filter(contributor = user_id)
    }
    return render(request, "user_profile_page.html", context)
    # doublecheck this one

def add_entry_page(request):
        context = {
            "user": User.objects.get(id = request.session['user_id']),
        }
        return render(request, "add_entry_page.html", context)

def deity_info_page(request, deity_id): 
    return render(request, "deity_info_page.html")
    # doublecheck this one 

def deity_edit_page(request, deity_id):
    context = {
        "user": User.objects.get(id = request.session['user_id']),
        "deity": Deity.objects.get(id=deity_id),
    }
    return render(request, "deity_edit_page.html", context)

#end render pages
def back(request):
    return redirect("welcome_page.html")

def register(request):
    if request.method == "GET":
        return redirect('/register_page')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/register_page')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/home_page')

def login(request):
    if request.method == "GET":
        return redirect('/log_in')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/log_in')
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
        print(search)
        print(search[0])
        # deity = Deity.objects.filter(Q(name__icontains=search[0])|Q(location__icontains=search[0])|Q(alt_name__icontains=search[0])|Q(culture__icontains=search[0])|Q(religion__icontains=search[0])|Q(description__icontains=search[0])|Q(pop_culture__icontains=search[0])),

        deity = Deity.objects.annotate(search=SearchVector('name', 'location', 'alt_name', 'culture', 'religion', 'description', 'pop_culture'),).filter(search=SearchQuery(search[0], search_type='phrase')),

        

        context = {
            "user": User.objects.get(id = request.session['user_id']),
            "deity": deity,
            "search": search[0],
        }
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

def edit_deity(request, deity_id):
    deity = Deity.objects.get(id = deity_id)
    errors = Deity.edits.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect(f'/deity_edit_page/{deity_id}')
    else:
        deity.name = request.POST['name']
        deity.alt_name = request.POST['alt_name']
        deity.culture = request.POST['culture']
        deity.location = request.POST['location']
        deity.religion = request.POST['religion']
        deity.description = request.POST['description']
        deity.pop_culture = request.POST['pop_culture']
        deity.source = request.POST['source']
        deity.save()
    return redirect('/home_page')