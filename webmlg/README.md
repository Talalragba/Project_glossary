# Glossary Web Application

## Overview
The Glossary Web Application is a web-based platform designed to manage and access a multilingual glossary. It provides features for user management, draft and approved definitions, and dynamic language support.

This project uses the following technologies:
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django (Python)
- **Database**: MongoDB

## Features
- User authentication and management
- Dynamic glossary definitions
- Multilingual support (English, French, German)
- Notifications for user activity
- Draft and approval workflows for definitions

## Prerequisites
Ensure the following are installed on your system:
- **Python** (version 3.12 or higher)
- **MongoDB** (configured and running on `localhost:27017`)
- **pip** (Python package manager)

To install MongoDB, you can visit the official MongoDB installation guide for Ubuntu [here](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/). Once MongoDB is installed, start the service with the following command:

```bash
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod # to check that mongodb is running properly
```
## Installation
Follow these steps to set up the application:

### Clone the Repository
```bash
git clone https://github.com/Talalragba/Project_glossary.git
cd Project_glossary
```

### Set Up the Virtual Environment
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies
Install the required Python packages:
```bash
cd webmlg
pip install -r requirements.txt
```

### Set Up the Database
Run the `setup.py` script to create the MongoDB database and initialize an admin user:
```bash
python setup.py
```
This will create the following collections in the `dbft` database:
- `userCollection`
- `userCredentials`
- `definitionDraftCollection`
- `definitionCollection`
- `trails`

It will also create an initial admin user:
- **Username**: `Admin`
- **Password**: `Admin`

## Running the Application
Start the Django development server:
```bash
python manage.py runserver
```
Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Folder Structure
```
Project_glossary/
|— webmlg/         
    |— appwmlg/         # Django application folder
        |— templates/           # HTML templates
        |— views.py/           
    |— setup.py             # Script to initialize the database
    |— requirements.txt     # Python dependencies
    |— manage.py            # Django management script
```

## Usage
### Admin Login
1. Use the credentials provided during setup to log in as the admin.
2. Manage users and definitions through the admin panel.

### Glossary Management
1. Add draft definitions to the `definitionDraftCollection`.
2. Approve drafts to move them to the `definitionCollection`.

### Multilingual Support
Translations are managed through local JSON files stored in the project folder. The language can be selected dynamically on the frontend.

## Contributing
Feel free to contribute to this project by:
- Forking the repository
- Creating a new branch
- Submitting a pull request

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any questions or issues, contact:
- **Email**: khalid.khalyl.12@gmail.com

