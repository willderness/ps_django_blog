% Module 1 -- Setup

# Install python

Install python3 per your OS instructions.
    
# Setup a virtual environment with venv

`python -m venv venv`
`source venv/bin/activate`

# Install django and other requirements

Run the following command to install the project’s required libraries: `python -m pip install -r requirements.txt`

# Run server
Verify that you can run your app by running: python manage.py runserver.  Then go to `localhost:8000`.  
**Note:** You will see the below warning that you have unapplied migrations, ignore this for now.  You do NOT want to add migrations before you add a User model.  
```
You have 19 unapplied migration(s). Your project may not work properly until you apply the migrations
for app(s): admin, auth, contenttypes, mainapp, sessions.
Run 'python manage.py migrate' to apply them.
```

# Verify Local Environment
To run tests for the first module, make sure your venv is activated, then run `python manage.py test module2/`.  Initially all of your tests should fail.  As you start to complete tasks in the project, the tests will pass.
