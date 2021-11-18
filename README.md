# Database-Security-Model
All files relating to my Database Security Final Project. The goal of this course was to familiarize myself with basic concepts of security and privacy in applications and in the industry. Additionally, the course addresses the security and privacy issues in legacy systems and studies security and privacy policies and legislations. As a part of my final project, I worked with two other students to design an application that demonstrates the different methods that you can use to create a secure database for a full stack, responsive web application.

### The Project
For our project, we created a Flask application that is connected a SQLite3 database that stores an id, fullname, username, address, age, salary, job title, and password for each user. You are then able to use your created username and password to login and access a webpage that dynamically displays all of the attributes stored in the database. From there, the user is given the ability to populate the database, hash and salt the password variable, anonymize the table, reset the table, or sign out.

### Populating
When the user selects "Populate", from the navbar the application is directed to the "/populate" route and proceeds to reads "dummy.txt", a text file storing information on 49 dummy users. It then adds these users to the database and updates the homepage accordingly. 

### Hashing and Salting
Hashing and salting is a method used in software development to protect user data. When hashing and salting a variable, you are appending a string of random characters to an attribute and then storing the hashed value of that new string in the database. The result is a string of seemingly random characters that is only accessable to a potential hacker if he access has the hashing method you used, as well as the "salt" added to the password. When the user clicks on "Hash and Salt" from the navbar, the application is directed to the "/hash" route and procceeds to hash and salt all the passwords in the database to secure each users account. 

***Note*** 
If the user selects the "Hash and Salt" attribute, they will have to go to server.py and in the login route comment out line 90 and uncomment line 91, as the hashed value of a password does not equal the original password.

### Anonymization 
Anonymization is another method used in software development to protect user data. When anonymizing data, the developer is essentially making reducing the granularity of a value. For example, in our project, when the user selects "Anonymize" the application is then directed to the "/anonymize" route where the username and password values are hidden from the viewer, the fullname is replaced by an asterisk, the address is replaced by the first three characters of their zip code, the age is replaced by either <= 45 or > 45, and the salary is replaced by either <= 45k or > 45K. 

### Conclusion
The result of this is a fully protected database that can provide the company with a great sense of security. Should a hacker or someone who should not have access to this database gain access, the data is protected and the users information is secure.
