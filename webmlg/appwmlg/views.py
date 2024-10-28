
# from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
import pymongo

from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
"""
def index(request):
    return render(request, 'appwmlg/index.html')
"""

#@login_required(login_url="login")
def search_view(request):
    if request.session.get("logedUser") != True :
        return redirect("login")  # Redirect to login if user is not authenticated
    return render(request, 'appwmlg/searchpage.html')


def logout_view(request):
    request.session.flush()  # Clear the session
    return redirect('login')  # Redirect to login page


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
dbft = client['dbft']
user_collection = dbft['userCollection']

def index_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(f"Attempting login with username: {username}")  # Debugging line

        user = user_collection.find_one({"UserName": username, "Password": password})
        print("###################################")
        print(user)
        print("###################################")
        if user : 
            if user['UserRole'] == "Admin":
                print("Role:", user['UserRole'])
            print("###################################")
            print("Languages:", user['UserLanguages'][0])
            print("###################################")
        print("###################################")
        if user:
            print("Login successful!")  # Debugging line
            print("Username:", username)
            print(request.session.get("logedUser"))
            request.session["logedUser"] = True
            print(request.session.get("logedUser"))
            print(request.session.get("blabla"))
            return redirect('search')  # Ensure this matches your URL pattern name for the search page
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
            print("Login failed: Invalid credentials")  # Debugging line
            #return render(request, 'appwmlg/index.html', {"error": "Invalid username or password"})

    return render(request, 'appwmlg/index.html')


#######################################

eng_definition_draft_collection = dbft['engDefinitionDraftCollection'] # Use your actual collection name


def add_definition(request):
    
    if request.session.get("logedUser") != True:
        return redirect("login")
    elif request.method == 'POST':
        term = request.POST.get('term')
        definition = request.POST.get('definition')
        example = request.POST.get('example')
        
        # Add to MongoDB
        eng_definition_draft_collection.insert_one({
            "term": term,
            "definition": definition,
            "example": example
        })
        
        return redirect('search')  # Redirect to search page or another page after submission

    else :
        return render(request, 'appwmlg/define.html')