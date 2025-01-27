import os
from pymongo import MongoClient
from datetime import datetime

def create_initial_database():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    dbft = client['dbft']
    
    # Define collections
    user_collection = dbft['userCollection']
    user_credentials = dbft['userCredentials']
    definition_draft_collection = dbft['definitionDraftCollection']
    definition_collection = dbft['definitionCollection']
    trails = dbft['trails']

    # Initial user details
    username = "Admin"
    hire_date = "23/08/1990"
    user_role = "admin"
    user_languages = ['Eng', 'Fr', 'De']
    user_email = "khalid.khalyl.12@gmail.com"
    born_date = "23/08/1990"
    notification = [[{
                "title": "Account creation",
                "message": "Your account is activated now",
                "timestamp": datetime.now(),
                "read": False}]]
    password = "Admin"

    # Insert user data into user_collection
    inserted_user = user_collection.insert_one({
        "UserName": username,
        "HireDate": hire_date,
        "UserRole": user_role,
        "UserLanguages": user_languages,
        "UserEmail": user_email,
        "BornDate": born_date,
        "selectedLanguage": "en",
        "Notifications": notification
    })

    # Add UserID to the user document
    inserted_user_id = inserted_user.inserted_id
    user_collection.update_one(
        {"_id": inserted_user_id},
        {"$set": {"UserID": str(inserted_user_id)}}
    )

    # Insert user credentials into user_credentials
    user_credentials.insert_one({
        "UserID": str(inserted_user_id),
        "UserName": username,
        "Password": password
    })

    print("Database setup completed. Initial admin user created.")

if __name__ == "__main__":
    create_initial_database()
