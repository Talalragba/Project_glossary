from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#################### For mongodb-django connection ####################
import pymongo
from pymongo import MongoClient

#################### For sending emails to new users ####################
import secrets
from django.core.mail import send_mail

#################### For timezone ####################
from django.utils import timezone

#################### Connect to MongoDB ####################
client = MongoClient('mongodb://localhost:27017/')
dbft = client['dbft']
user_collection = dbft['userCollection']
eng_definition_draft_collection = dbft['engDefinitionDraftCollection']
eng_definition_collection = dbft['engDefinitionCollection'] 

#################### This is the login view ####################
#In this view we get the username and password from the login page
#then we look if the user attempting to login is exist in the userCollection 
#so if yes we create a session where we store logedUser (boolen value), 
#username and userRole (we might add other parameters as the project evolve)
#after that we redirect the user to the search page, but if not exist in 
#the userCollection we send a message using django.contrib's messages library
#and we redirect to login page again else if now one is attempting to login
#we just render the login page
#################################################################
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

#################### This is the lougout view ####################
# First we clear the session then we redirect to the login page
def logout_view(request):
    request.session.flush()  # Clear the session
    return redirect('login')  # Redirect to login page

#################### This is the search view ####################
#to pevent non authenticated users to get into this view we first check the
#the session's logedUser variable if it is a False value we then redirect
#to the login page but in case it is a True value we wait (render the search page)
#until the user type in an acronym if it is exit in the engDefinitionCollection
#we then show the user the definition of the acronym but if not we show him
#that "The acronym doesn't exist"
##################################################################
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

#################### This is the define view ####################
#1) to pevent non authenticated users to get into this view we first check the
#the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) as long as the author is just typing in or just being in the define page
#we keep rendring the define page but when he start submitting a new definiton we get the
#informations from the define page to the define view and we procced by inserting 
#the draft into engDefinitionDraftCollection for reviewing and approving or refusing it 
#then the author is redirected the search page (a notification might be added 
#to notify thr author that his definition is sent for check)
#################################################################
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

#################### This is the addUser view ####################
#1) to pevent non authenticated users to get into this view we first check the
#the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) as long as the admin is just typing in or just being in the addUser page
#we keep rendring the addUser page but when he start submitting a new user we get the
#informations from the addUser page to the addUser view and we procced by inserting
#the new user into userCollection and sending a congratulation email containing
#the user's username and password to his email adress then we redirect to search page
# ################################################################ 
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

#################### This is the users view ####################
#1) to pevent non authenticated users to get into this view we first check the
#the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) but if it is a True value we then read all the existing users and put 
#them in the users variable which then is passed to the users page as an object
#that conatin all users data
################################################################
def users_view(request):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else : 
        users = list(user_collection.find()) 
        print(users)
        return render(request, 'appwmlg/users.html', {'users': users})       

#################### This is the user view ####################
#0) first thing here is that this view gets a variable passed to it from the
#users page which is in this case 'username' 
#1) and to pevent non authenticated users to get into this view directly from the url
#we first check the the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) after that we take the variable that was passed to this view which is the username
#and we look for the document corresponding to this username and  we store the data extracted
#into a variable called user which is then passed to the user page as a parameter
############################################################### 
def user_view(request, username):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else :
        user = user_collection.find_one({"UserName": username})
        return render(request, 'appwmlg/user.html', {'user': user})
    
#################### This is the user update view ####################
#0) first thing here is that this view gets a variable passed to it from the
#user page which is in this case 'username' 
#1) we also get the now role and new email if updated from the user page using
#the POST method after that we store/update this data into the user document 
#corresponding to the username that we got passed as a parameter to the view 
#and finally we redirect to the search page
#######################################################################
def user_update_view(request, username):
    if request.method == 'POST':
        newRole = request.POST.get('role')
        newEmail = request.POST.get('email')

        # Update the user in the database
        user_collection.update_one({"UserName": username}, {"$set": {"UserRole": newRole, "UserEmail": newEmail}})
        return redirect('search') 

#################### This is the user delete view ####################
#0) first thing here is that this view gets a variable passed to it from the
#user page which is in this case 'username' 
#1) and to pevent non authenticated users to get into this view directly from the url
#we first check the the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) else we delete the user corresponding to the username from the userCollection and
#we then redirect to search page
###############################################################
def user_delete_view(request, username):
    if request.session.get('logedUser') != True:
        return redirect('login')
    elif request.method == 'POST':
        user_collection.delete_one({"UserName": username})
        return redirect('search')

#################### This is the drafts view ####################
#1) and to pevent non authenticated users to get into this view directly from the url
#we first check the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) else we get all the drafts from engDefinitionDraftCollection and we put the into
#drafts varible which the is passed as parameter to the draft page which 
#will desplay them 
#################################################################
def drafts_view(request):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else : 
        drafts = list(eng_definition_draft_collection.find()) 
        print(drafts)
        return render(request, 'appwmlg/drafts.html', {'drafts': drafts})

#################### This is the user update view ####################
#0) first thing here is that this view gets a variable passed to it from the
#drafts page which is in this case 'acronym' 
#1) and to pevent non authenticated users to get into this view directly from the url
#we first check the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) after that we take the variable that was passed to this view which is the acronym
#and we look for the document corresponding to this acronym and  we store the data extracted
#into a variable called draft which is then passed to the draft page as a parameter
######################################################################
def draft_view(request, acronym):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else :
        draft = eng_definition_draft_collection.find_one({"Acronym": acronym})
        return render(request, 'appwmlg/draft.html', {'draft': draft})

'''######################################################################
0) first thing here is that this view gets a variable passed to it from the
draft page which is in this case 'acronym' 
1) and to pevent non authenticated users to get into this view directly from the url
we first check the session's logedUser variable if it is a False value we redirect
to the login page.
2) after that we get the draft correspondig to the acronym from the engDefinitionDraftCollection
then we procced with the approval procces and we get to the third approver, and he procced so
we then transfer the draft from engDefinitionDraftCollection to engDefinitionCollection
and we delete the draft eventually 
Note :
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

#################### This is the delete draft view ####################
#0) first thing here is that this view gets a variable passed to it from the
#draft page which is in this case 'acronym' 
#1) and to pevent non authenticated users to get into this view directly from the url
#we first check the the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) after that we only render the deleteDraft page until the approver chose the reason why 
#he is deleting this draft then we get the author of the drat and we delete the draft
#and send a notification to the author and redirect to search page
########################################################################
def delete_draft_view(request, acronym):

    if request.session.get('logedUser') != True:
        return redirect('login')
    
    draft = eng_definition_draft_collection.find_one({"Acronym": acronym})
    if request.method == "POST":
        author = draft['DefinitionAuthor']
        reason = request.POST.get("reason")  

        eng_definition_draft_collection.delete_one({"Acronym": acronym})
        user_collection.update_one({"UserName": author}, {"$push": {"Notifications":[{
            "message": reason,
            "timestamp": timezone.now(),
            "read": False}]}})

        return redirect('search')

    return render(request, 'appwmlg/deleteDraft.html', {'draft': draft})

#################### This is the notifications view ####################
#1) to pevent non authenticated users to get into this view directly from the url
#we first check the the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) after that we get the user document of the logged user and pass it to 
#the notifications page to be shown to the user
########################################################################
def notifications_view(request):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else : 
        user = user_collection.find_one({"UserName": request.session["username"]})
        print(user)
        print(user["_id"])
        return render(request, 'appwmlg/notifications.html', {'user': user})   

#################### This is the notification view ####################
#1) to pevent non authenticated users to get into this view directly from the url
#we first check the the session's logedUser variable if it is a False value we redirect
#to the login page.
#2) in this view instead of passing a paramter to the view we used another technique
#which is '?message={{ notification.message }}' in the notifications page then we passed
#once again the same message to notification page in order to be displayed correctly
########################################################################
def notification_view(request):
    if request.session.get('logedUser') != True:
        return redirect('login')
    else :
        message = request.GET.get("message")
        return render(request, 'appwmlg/notification.html', {'message': message})