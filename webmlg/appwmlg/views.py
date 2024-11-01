
# from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
import pymongo

from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import secrets
from django.core.mail import send_mail

from django.utils import timezone


# Create your views here.
"""
def index(request):
    return render(request, 'appwmlg/index.html')
"""

#@login_required(login_url="login")

'''
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
from pymongo import MongoClient

# Set up MongoDB client
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGO_DB_NAME]  # Use your actual database name here

def search_acronym(request):
    definition = None
    error_message = None
    
    if 'acronym' in request.GET:
        acronym = request.GET.get('acronym').strip()
        
        # Access the collection and search for the document
        collection = db['engDefinitionDraftCollection']
        document = collection.find_one({"acronym": acronym})
        
        if document:
            definition = document.get("definition")  # Get the definition if the document exists
        else:
            error_message = "The acronym doesn't exist."
            #messages.error(request, "Invalid credentials")
    
    return render(request, 'searchpage.html', {'definition': definition, 'error_message': error_message})

'''
def search_view(request):
    if request.session.get("logedUser") != True :
        return redirect("login")  # Redirect to login if user is not authenticated
    elif 'acronym' in request.GET:
        #request.method == "GET":
        docDef = None
        message = None
        definition = None
        acronym = request.GET.get('acronym')
        docDef = eng_definition_draft_collection.find_one({"Acronym": acronym})
        
        print("#################################################")
        print("je suis la")
        print(message)

        if docDef:
            definition = docDef["Definition"]  
        else:
            message = "The acronym doesn't exist."
        return render(request, 'appwmlg/searchpage.html', {'definition': definition, 'message': message})

    else :
        return render(request, 'appwmlg/searchpage.html')


def logout_view(request):
    request.session.flush()  # Clear the session
    return redirect('login')  # Redirect to login page


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
dbft = client['dbft']
user_collection = dbft['userCollection']

def login_view(request):
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
            request.session["username"] = user['UserName']
            print(request.session.get("logedUser"))
            print(request.session.get("username"))
            return redirect('search')  # Ensure this matches your URL pattern name for the search page
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
            print("Login failed: Invalid credentials")  # Debugging line
            #return render(request, 'appwmlg/index.html', {"error": "Invalid username or password"})

    return render(request, 'appwmlg/index.html')


#######################################

eng_definition_draft_collection = dbft['engDefinitionDraftCollection'] # Use your actual collection name

def define_view(request):
    
    if request.session.get("logedUser") != True:
        return redirect("login")
    elif request.method == 'POST':
        acronym = request.POST.get('acronym')
        definition = request.POST.get('definition')
        source = request.POST.get('source')
        industry = request.POST.getlist('industry')  
        definition_submission_date = timezone.now()  
        definition_author = request.session.get("username")
        
        # Add to MongoDB
        eng_definition_draft_collection.insert_one({
            "Acronym": acronym,
            "Definition": definition,
            "Source": source,
            "Industry": industry,
            "DefinitionSubmissionDate": definition_submission_date,
            "DefinitionAuthor": definition_author,
            "Approvers": [],
            "ApproversNumber": 0 
        })
        
        return redirect('search')  # Redirect to search page or another page after submission

    else :
        print(request.session.get("username"))
        return render(request, 'appwmlg/define.html')



############################


def addUser_view(request):

    if request.session.get("logedUser") != True:
        return redirect("login")
    elif request.method == 'POST':
        username = request.POST.get('username')
        hire_date = request.POST.get('hire_date')
        user_role = request.POST.get('user_role')
        user_languages = request.POST.getlist('languages')  # Get multiple selections as a list
        user_email = request.POST.get('user_email')
        born_date = request.POST.get('born_date')

        # Generate a random password
        password = secrets.token_urlsafe(8)  # Generates an 8-character password

        # Insert into MongoDB
        user_collection.insert_one({
            "UserName": username,
            "HireDate": hire_date,
            "UserRole": user_role,
            "UserLanguages": user_languages,
            "UserEmail": user_email,
            "BornDate": born_date,
            "Password": password
        })

        # Send the congratulatory email with the password
        send_mail(
            'Welcome to the Glossary App!',
            f'Hello {username},\n\nCongratulations on joining! Here is your access information:\n\nUsername: {username}\nPassword: {password}\n\nPlease keep this information safe.\n\nBest regards,\nThe Glossary App Team',
            'talaltago@gmail.com',  # Replace with your email
            [user_email],
            fail_silently=False,
        )

        return redirect('search')  # Redirect after submission
    else :
        return render(request, 'appwmlg/addUser.html')
