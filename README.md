# VulnerableWebApp
## Course Project I for Cyber Security Base

LINK: https://github.com/aniemi/VulnerableWebApp
You need to have Python (3.5 and newer, or 2.7) as well as Flask installed. You may have to ensure that your version is recent enough and includes pip. This can be done by running the commands 'python --version' and 'pip --version'. If needed, pip can be installed according to these instructions: https://pip.pypa.io/en/stable/installing/ - or you could just install the latest Python version from python.org. 

1. Make sure that a new enough version of Python as well as pip are installed. 
2. On command line, run the command `pip install Flask`
3. Download the repository contents. 
4. Navigate to the project root with command line, and run the following commands: `export FLASK_APP=main` and `flask run`. 
5. Application can be accessed on localhost:5000

More detailed instructions for installing Flask are presented on its site: https://flask.palletsprojects.com/en/1.1.x/installation/

There is a ready SQLite database with the application, so there is no need to initialize it (but it can reinitialised by importing and running the init_db() method in Python console). There are two users that can be used, admin - admin and ted - ted (username - password). 

### FLAW 1: Injection
The application uses an SQLite database. The queries to it, however, are not parameterized, so a single-line injection can be used to, for example, dump all the pastes in the database. As it is likely that a database is used, and as the paste to be displayed is requested through a simple GET request, it is easy to modify the url to contain the SQL to be injected. To display all pastes in the database, marked private or not, we can use the following query: `4' OR 1=1; --`. With the OR operator we add a condition that applies to any row. Then we end the statement and comment out the rest of the query to be executed from the application source code. The statement can be edited into the URL like this: `http://<url>/paste/?paste=4%27+OR+1%3D1%3B+--`

The flaw is easy to fix by parameterizing the query. As an example, the method get_paste() can be modified like this: 
```
query = "SELECT * FROM pastes WHERE id = ?;"
cur = get_db().execute(query,(id,))
```
After which the injection no longer works. As there are several SQL queries in the application, they all need to parameterised like this.

Use of ready modules like Flask-SQLAlchemy and its ORM functionality is often recommended, as they provide functionality that deals with basic vulnerabilities like this out of box. 

### FLAW 2: Broken Authentication 
The application has a badly designed login system, which among others things stores passwords as plaintext and does not use SSL. There are also no requirements for password length or checks against user/password brute forcing attempts. 

The most important fix is to hash the passwords and use SSL. Use of modules like Flask-Login is also recommended often, as it is easy to set up and deals with vulnerabilities like this out of box. I wasn't able to complete this assignment by using these ready libraries, as they would not allow most of the OWASP Top 10 vulnerabilities to exist.

It is a bit difficult to provide complete instructions to fix this kind of flaw, as the fixing requires some redesigning of the application, and the instructions depend on those design choices. For a simple implementation of password hashing, we can use functionality from Werkzeug, included with Flask. 
```
from werkzeug.security import generate_password_hash, check_password_hash
```
To the add_user() method, we would add the generate_password_hash() method for the user inputted password, passing the resulting hash to the SQL query. Then, when user tries to log in, we would check that the password matches that hash by adding lines like this --

```
hash = check_password_hash(login_pw, pw)
if user == login_user and hash is True:
```
-- and so on. 

### FLAW 3: Sensitive Data Exposure
See above. Given that a random pastebin site is unlikely to contain the most private secrets of anyone (of course, you never know), the most dangerous flaw is that passwords are stored and transmitted non-encrypted. Users could have used the same password elsewhere and could end up having their other login credentials compromised. Obviously, pastes marked as 'private' are only private in terms of the user interface not providing a link to access them for others than the owner; it is easy to snoop on the contents with HTTPS not in use.

One way to use SSL with Flask is to install a dependency called pyopenssl - `pip install pyopenssl` - and run the application with `flask run --cert=adhoc`. This, however, requires addition of a certificate, otherwise the browser will warn about it every time. Best way to deal with this would be to get a free certificate from Let's Encrypt and install it on the server that the application is deployed to. Services like Heroku offer easy-to-deploy solutions for certificates as well. It is a good idea to enforce SSL as well - by redirecting all HTTP requests to HTTPS, for example. Note that on a production server enabling SSL is a bit different; look for instructions on depending on the solution being used.

### FLAW 4: Broken Access Control 
Pastes stored in the database are automatically assigned a predictable integer id, even if they are private. There is also no check in place for the identity of the user who is trying to access a paste, as the 'developer' has trusted that users will only try to access resources through the interface they have designed. Thus, private pastes are can be trivially accessed by merely modifying the url, going through all numeric possibilities: http://localhost:5000/paste/?paste=2 allows you to access that paste, even though it is marked as private.

The most important thing to fix is to check that the user really is the owner of the paste. The 'developer' should consider redesigning the entire login system, but a quick band-aid-like fix would be to add a simple check for the id of the user against the one in the database. To check that a user cannot request private pastes not owned by them, the SQL query could be modified as follows.
```
"SELECT * FROM pastes WHERE id = ? AND (user = ? OR private_paste = 'False');"
```

### FLAW 5: XSS
On line 42, user input to be displayed in the browser has been marked as `|safe`. This allows user input to inject persistent XSS, being rendered in the browser of everyone it is shown to. This is demonstrated in paste number #6. The flaw could compromise cookies or other sensitive information, or rewrite the html code that is rendered to the user viewing the paste. 

This is easily fixed by removing `|safe` in line 42 from template "index.html", right after `element[1]`.

### FLAW 6: Insufficient Logging & Monitoring

As this is an application with users, content and database interactions, detailed logs from which suspicious login attempts and such can be detected and investigated should be available. The application should record detailed logs about what happened and when. Security flaws from the above classes could then often be spotted at least before they will go on for years.
