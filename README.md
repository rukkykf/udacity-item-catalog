# Item Catalog
## Project Description
The item catalog project is part of the Udacity Full Stack Developer nanodegree. This project sets up a functional web application that allows users to register and perform CRUD  operations on a database. The users are able to register either by using OAuth authentication with Google accounts or by creating a password and username with the registration form. Key features of this application include:

 - Users can authenticate with their Google accounts
 - Users can register on the application with a username and password
 - Users can create, read, edit (update) and delete items from the database.
 - Users can also like (and unlike) items created by other users.

## Getting Started
To run this application follow these steps (run the code in your terminal):

 1. If you use windows, see the instructions for windows users before coming to continue with the installation process
 2. Install python (I used 2.7, but this application should work with python3 as well)
 3. Install virtualenv on your machine using
	 `pip  install virtualenv`
 4. Clone this repository and cd into it.
 5. Create a virtual environment using `virtualenv venv  `
 6. Activate your virtual environment using `source venv/bin/activate `
 7. Install the item-catalog app by running `pip install -e . `
 8. Tell flask some things about the application by running the following
	`export FLASK_APP=itemcatalog`
   `export FLASK_ENV=development`
 9. The OAuthlib library used enforces https. To run this application in development disable that using `export OAUTHLIB_INSECURE_TRANSPORT=1`
 10. Setup the database using `flask init-db  `
 11. Add the catalog data using `flask init-data`
 12. Run the application using `flask run`
 13. If you're running this application on a vagrant virtual machine and you want to be able to view the application on your host computer, use `flask run --host=0.0.0.0 `

## Instructions for Windows Users
If you're using a Windows machine, this application might not work if you try to run it on windows. To ensure it works setup a vagrant machine and configure the vagrant machine to have port forwarding. Follow these instructions:

- Use a terminal application. Download and install Git Bash from here [Download Git ](https://git-scm.com/download/win)
-   Download and install virtual box from here: [https://www.virtualbox.org/wiki/Download_Old_Builds_5_1](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).
-   Download and install vagrant from here: [https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html)
-   Open up your git bash terminal, cd into the directory you want to place the Vagrant machine in
-   Use vagrant to install bento/ubuntu-16.04 and setup port forwarding for common development ports (5000, 8080, 8000) . I won't tell you how to do that, try Google :)
- Start your vagrant machine, cd into the folder you want to create your repository in and then continue with the getting started instructions above.
-
## Modules
The various views in the application are organized into blueprints.

**__init__.py**:
This module contains the app factory. Here the app is created, configured and the various blueprints are registered.

**auth.py**:
This module contains all the views related to authenticating and authorizing the user, including the registration of new users, login of existing users, Oauth authentication with Google for users who want to connect with their Google accounts, a decorator for protecting  other views in the application.

**catalog.py**:
This module contains the views directly related to browsing the Item Catalog.

**data.py**:
This module handles putting initial application data into the application's database.

**db.py**:
This module handles setting up the database models in the database.

**dbmodels.py**:
This module contains the database models (created with flask-sqlalchemy)

**forms.py**:
This module contains the forms used in the application. Flask-WTF is used to create the forms and implement CSRF protection.

**items.py**:
This module handles views associated with performing CRUD operations on the items in the catalog.

**itemsapi.py**:
This module contains the api endpoints for the application. At the moment there's one view at /items/json/ that returns a json file containing a list of the items in the catalog.

**passwordmng.py**:
This module contains the various utility functions for password management. The project isn't complete yet, but ultimately this will include functions and classes for confirming user emails, handling password recovery.

**user.py**:
This module contains the view for the user's profile

**validate_item_ud.py**
This is a utility module created to help validating the edit and delete operations in items.py

## JSON endpoint
To view a list of all the items in the catalog in JSON format visit
http://localhost:5000/items/json/

## Suggestions to Improve the Project

 - **Enable Global CSRF protection**:  Currently only the forms are protected with CSRF. Enable CSRF for the entire application.
 - **Use Javascript**: Currently there is no javascript in this application and that means there the browser has to reload the pages on each request. To avoid this AJAX would be useful for sending requests.
 - **Find and fix security vulnerabilities**
 - **Add other OAuth providers**
 - **Improve the design of the application's interface**
