# from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
import pymongo

# Create your views here.
"""
def index(request):
    return render(request, 'appwmlg/index.html')
"""
def search_view(request):
    return render(request, 'appwmlg/searchpage.html')


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
dbft = client['dbft']
users_collection = dbft['users']

def index_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(f"Attempting login with username: {username}")  # Debugging line

        user = users_collection.find_one({"username": username, "password": password})
        print("###################################")
        print(user)
        print("###################################")
        if user : 
            if user['occupation'] == "Software Engineer":
                print("role:", user['occupation'])
            print("###################################")
            print("Languages:", user['languages'][0])
            print("###################################")
        print("###################################")
        if user:
            print("Login successful!")  # Debugging line
            return redirect('search')  # Ensure this matches your URL pattern name for the search page
        else:
            print("Login failed: Invalid credentials")  # Debugging line
            return render(request, 'appwmlg/index.html', {"error": "Invalid username or password"})

    return render(request, 'appwmlg/index.html')
