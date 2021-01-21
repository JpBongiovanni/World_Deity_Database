from django.shortcuts import render, HttpResponse

#start render functions
def index(request):
    return render(request, "welcome_page.html")

def home_page_render(request):
    return render(request, "home_page.html")

def register_page_render(request):
    return render(request, "register_page.html")

def deities_by_location_page(request):
    return render(request, "deities_by_location_page.html")

def deities_by_religion_page(request):
    return render(request, "deities_by_religion_page.html")

def top_ten_page(request):
    return render(request, "top_ten-page.html")

def user_profile_page(request, user_id):
    return render(request, "user_profile_page.html")
    # doublecheck this one

def add_entry_page(request):
    return render(request, "add_entry_page.html")

def deity_info_page(request, deity_id): 
    return render(request, "deity_info_page.html")
    # doublecheck this one 

#end render pages


