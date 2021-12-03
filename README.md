# Secure Database Model
As a part of my Database Security class, I worked with two other students to design an application that demonstrates the different methods that you can use to create a secure database for a web application. The result is this project, a fully responsive, full-stack web application that connects to a SQLite3 Database. The application itself allows the user to signup, login, and visualize the differences in the database after password hashing, salting, and data anonymization

### Installation
This project requires several installations before it is accessable to the user. The easiest way to do this is to install pip which can be done by running the command:
```
python3 -m pip install --user --upgrade pip
```
The user must then setup and navigate to a folder the project to be cloned to. You then must setup a local environment to install the proper packages by running:
```
python3 -m pip install --user virtualenv
python3 -m venv env
```
Following this, the user must navigate to the env file in the terminal and then activate the virtual environment by running the following command:
```
env\Scripts\activate
```

Finally the user must run the following pip commands:
```
pip install Flask
pip install Flask-SQLAlchemy
```
The user can then, in the terminal, navigate to the location of the 'env' folder, clone the repository, and run the following command to launch the application.
```
python3 app.py
```

### Usage
The web application has 5 main features. A sign-up page, a login page, a population route, a password-hashing route, and a anonymization route. 

When first running the app, the user is directed to a login page where if the user can click on the sign-up button at the bottom to sign-up. 

The user then enters their Full Name, Username, Address, Age, Salary, Job Title, and Password. The app then stores this in an SQLite3 database, redirects the user to the login page where they can then login with their account.

Once logged in, the user is show a webpage which dynamically shows the data stored in the database, simulating the view of the "hacker". The user then can select one of three options by clicking on the hamburger icon on the navbar, "Populate", "Hash and Salt", "Anonymize".

#### Populate
When clicking on the Populate route, the app reads a text file called "dummy.txt" and fills the database with 49 other random users with dummy data. It then updates the table that the user sees so the user now is able to read 50 users information.

#### Hash and Salt
When clicking on the Hash and Salt route, the app loops through the entire database and hashes and salts the password attribute in the table. It then updates this value from plain text to the hash/salted value and essentially hides it from the user, demonstrating the effectiveness of password hashing/salting.

#### Anonymize
When clicking on the Anonymize route, the app anonymizes the table with respect to l-diversity and k-anonymity. This is executed by replacing every name with an asterick, hiding the username and password attributes, replacing the entire address with the first three numbers of their zip code, and by replacing their salary and age with a value of either 'less than or equal to 45' or 'greater than 45', depending on their values. The table is then updated to show the newly secured data.

***Please Note*** 
If the user selects the "Hash and Salt" attribute, they will have to go to app.py and in the login route comment out line 90 and uncomment line 91. If not, the user will not be able to login after they signout, as the hashed value of a password does not equal the original password.

### Conclusion
The result of this is a fully protected database that can provide the company with a great sense of security. Should a hacker or someone who should not have access to this database gain access, the data is protected and the users information is secure.
