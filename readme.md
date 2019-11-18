# Install python.

Install python3 per your OS instructions.

# Setup virtual environment with venv

```
python -m venv venv
source venv/bin/activate
```

# Install django and other requirements.

`pip install -r requirements.txt`

# Run server

`python manage.py runserver`


# Create a user account.

Run the create super user command and follow terminal insctructions.

`python manage.py createsuperuser`


# Create some content

Navigate to the admin page, login with your new account, and create a few blog posts.
http://localhost:8000/admin

# Navigate to main page and browse around

http://localhost:8000

# Run tests by using Django Test on the module folders

`python manage.py test module1`
