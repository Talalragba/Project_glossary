
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
        docDef = eng_definition_collection.find_one({"Acronym": acronym})
        
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
            request.session["userRole"] = user['UserRole']
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

eng_definition_draft_collection = dbft['engDefinitionDraftCollection'] 

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
        #print(request.session.get("username"))
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



##########################################

def users_view(request):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else : 
        users = list(user_collection.find()) 
        print(users)
        return render(request, 'appwmlg/users.html', {'users': users})       


def user_view(request, username):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else :
        user = user_collection.find_one({"UserName": username})
        return render(request, 'appwmlg/user.html', {'user': user})
    
    
def user_update_view(request, username):
    if request.method == 'POST':
        newRole = request.POST.get('role')
        newEmail = request.POST.get('email')

        # Update the user in the database
        user_collection.update_one({"UserName": username}, {"$set": {"UserRole": newRole, "UserEmail": newEmail}})
        return redirect('search') 


def user_delete_view(request, username):
    if request.session.get('logedUser') != True:
        return redirect('login')
    elif request.method == 'POST':
        user_collection.delete_one({"UserName": username})
        return redirect('search')

##################################

def drafts_view(request):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else : 
        drafts = list(eng_definition_draft_collection.find()) 
        print(drafts)
        return render(request, 'appwmlg/drafts.html', {'drafts': drafts})

def draft_view(request, acronym):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else :
        draft = eng_definition_draft_collection.find_one({"Acronym": acronym})
        return render(request, 'appwmlg/draft.html', {'draft': draft})


eng_definition_collection = dbft['engDefinitionCollection'] 

'''
The logic in the approve_draft_view is taken into account
the fact that when a loged moderator or admin if he alrady 
approved a draft it should not show in the drafts page which
means that a test condition should be considered in the drafts page
to prevent that 
'''
def approve_draft_view(request, acronym): 
    print("#############################")
    print("khalid")
    print("#############################")

    if request.session.get('logedUser') != True:
        return redirect('login')
    
    draft = eng_definition_draft_collection.find_one({"Acronym": acronym})

    if request.session.get("username") in draft['Approvers']: # in any case the by accedent the moderator know how to write the url of a draft directly into the browser so he can't approve two or more times the same draft.
        return redirect('search')
    
    if draft['ApproversNumber'] != 2 :
        approvers_number = draft['ApproversNumber'] + 1
        approver = draft['Approvers'] + [request.session.get("username")]
        eng_definition_draft_collection.update_one({"Acronym": acronym}, {"$set": {"Approvers": approver, "ApproversNumber": approvers_number}})
        return redirect('search')
    else :
        approvers_number = draft['ApproversNumber'] + 1
        approver = draft['Approvers'] + [request.session.get("username")]              
        definition_date = timezone.now()
        
        count = eng_definition_collection.count_documents({"Acronym": draft['Acronym']})
        dfs = eng_definition_collection.find({"Acronym": draft['Acronym']}) # The existing definition that with the same acronym

        for df in dfs : 
            eng_definition_collection.update_one({"Acronym": df['Acronym']}, {"$set": {"ActualDefinition": False}})
        
        eng_definition_collection.insert_one({
            "Acronym": draft['Acronym'],
            "Definition": draft['Definition'],
            "Source": draft['Source'],
            "Industry": draft['Industry'],
            "DefinitionDate": definition_date,
            "DefinitionAuthor": draft['DefinitionAuthor'],
            "Approvers": [approver],
            "ApproversNumber": approvers_number,
            "ActualDefinition": True,
            "DefinitionVersion": count+1
        })   
        eng_definition_draft_collection.delete_one({"Acronym": acronym})
        return redirect('search')

def delete_draft_view(request, acronym):
    
    draft = eng_definition_draft_collection.find_one({"Acronym": acronym})
    if request.method == "POST":
        author = draft['DefinitionAuthor']
        reason = request.POST.get("reason")  

        eng_definition_draft_collection.delete_one({"Acronym": acronym})
        user_collection.update_one({"UserName": author}, {"$set": {"Notifications": reason}})

        return redirect('search')

    return render(request, 'appwmlg/deleteDraft.html', {'draft': draft})



