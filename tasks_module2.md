# Create user app

We’re going to create a separate user app within our project.  Run the following command to do that:  
`python manage.py startapp users`

# Include the new app into the project

Inside of `settings.py` (located in `blogproj/`), find the `INSTALLED_APPS` list and after `'mainapp'`, add `'users'`.

# Add login template

We went ahead and created a basic login template for you to copy.  First, create a folder inside the `users/` directory called `templates`. Then, from the `support/` directory, move the `login.html` file into the `users/templates/` directory.

# Create custom user model

Now we want to create our User model in `users/models.py`.  To create a User class that derives from AbstractUser do the following:
Add an import of `AbstractUser` from `django.contrib.auth.models` in the import section.
Create the class `User` and derive from `AbstractUser` like so -- 
`class User(AbstractUser):`
Leave the class definition empty with `pass`, the base class has all we need for now.

# Add user model to the admin site

In order to have access to this model in the admin, we need to register it in `admin.py`.  Let’s do the following:
In the import section, add an import of `UserAdmin` from `django.contrib.auth.admin` and import `User` from `.models`.
Call `admin.site.register()` with `User` and `UserAdmin` as parameters.

# Set user settings in the main project

We need to specify the login URLs and the User model to use for authentication in `settings.py`.  At the bottom of `settings.py` in the `blogproj/` directory, add three global variables. First add `LOGIN_URL` and set it to `'login'`. Next, add `LOGIN_REDIRECT_URL` and set it to `'index'`. Lastly, add `AUTH_USER_MODEL` with the value of  `'users.User'`

# Add routes to the user app

Next, we need to setup routes for the user project. Like in the main app, we’ll create a dedicated `urls.py` file inside of the `users` directory.   We’re going to use `LoginView.as_view()` and `LogoutView.as_view()` to provide built-in login and logout functionality.  In the newly created `urls.py` file, import `views` as `auth_views`from `from django.contrib.auth`, import `path` from `django.urls`, and import `views` from `.` (the current folder). Then copy and paste the following URL patterns at the bottom of the file:
```
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index' ), name='logout'),
]
```

# Redirect user related routes to the user project

In `blogproj/urls.py`, add `path('accounts/', include('users.urls')),` as the first entry in the `urlpatterns` array.

# Add login/logout to site templates

In the `templates/base.html` template, uncomment the `Login` and `Logout` list items by removing the `{% comment %}` and `{% uncomment %}` tags inside the `navbar-nav` div.

# Run initial migrations

Now that we’ve added our User model we need to run migrations. From the command line, inside the root of the project, run the following commands:
`python manage.py makemigrations`
`python manage.my migrate`

Once created, add the newly created migrations to the git repo and commit them.

**Note:** Make sure your `venv` is activated with `source venv/bin/activate`
**Note:** If you made migrations before adding the user model, you’ll want to remove them because it will cause errors. You can do this by deleting all files in the `mainapp/migrations` folder, `users/migrations` folder, and the `db.sqlite3` file.

# Create an admin user

Create a superuser by running the following command from the command line: `python manage.py createsuperuser`.

At this point we can login and logout with our superuser.  Let’s test this out by running `python manage.py runserver`, then visit `http://localhost:8000`.  Click on the Login link, then login with your superuser credentials.  You can also login to the admin at `http://localhost:8000/admin`.  Congratulations!  You successfully implemented a custom User model with authentication.
