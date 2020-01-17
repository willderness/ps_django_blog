
# Create Model class

Create the blog post model by adding a new class into `mainapp/models.py`. Name the class `BlogPost` and make it extend `models.Model`. In the class body, add a field called `title` and set it to `models.CharField()`. Pass it a `max_length` of `200`.

```python
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
```

# Add author foreign key

To add the foreign key, we need to know which user model is in use. This is stored in the Django setting called `AUTH_USER_MODEL`. Lets first import those settings.

Add `from django.conf import settings` to the top of the file. Then in the body of our `BlogPost` class, add a new field called `author` with type of `models.ForeignKey()`. Pass the following parameters to `ForeignKey()`: `settings.AUTH_USER_MODEL`, `related_name="posts"`, and `on_delete=models.CASCADE`.
    
```python
author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name="posts",
    on_delete=models.CASCADE,
)
```

# Add body field

Add another field to `BlogPost` called `body` with type `models.TextField()`

# Add a date field to each post

Add a field called `postdate` of type `models.DateTimeField()` with parameters `auto_now_add` set to `True`, and `blank` set to `True`.

`postdate = models.DateTimeField(auto_now_add=True, blank=True)`

# Add string method
Adding a `__str__()` method to the class will simplify rendering in admin view and our templates. In the `BlogPost` class, create a method called `__str__` that takes a parameter called `self`. Have the method return `self.title`. 

```python
def __str__(self):
	return self.title
```

# Add url reverser.

Having a `get_absolute_url` function lets Django determine the canonical URL for a given model. This will come in handy in our views. First we need to import the `reverse` helper function from `django.urls` at the top of the file. Next add a method in the class called `get_absolute_url` that takes the `self` parameter. The method should contain the following line: `return reverse('post', args=[str(self.id)])`

```python
def get_absolute_url(self):
	return reverse('post', args=[str(self.id)])
```

# Register new model on admin site

In `mainapp/admin.py`, import the new `BlogPost` model from `.models`. Then at the bottom of the file, call `admin.site.register()` with `BlogPost` as the only parameter.

```python
from .models import BlogPost

admin.site.register(BlogPost)
```

# Update index view to use model

Now we need to update `mainapp/views.py` to include our new `BlogPost` model. First let's import the `BlogPost` model from `.models`. Also import the `get_object_or_404` method from `django.shortcuts`.

Next in the `index` method, set the `posts` variable to `BlogPost.objects.all()` instead of `ALL_POSTS`.

# Include model in post view

In the `post` method, we can take advantage of the django shortcut `get_object_or_404()` to do all the exception handling instead of having to rewrite it often. Replace the entire try/accept block with a line that sets the `post` variable to the BlogPost returned by `get_object_or_404(BlogPost, pk=id)` . 
The `return` line can stay just as it is.


# Migrate to new schema

Now that we’ve added our `BlogPost` model, we need to run migrations again. From the command line, inside the root of the project, run the following commands:

`python manage.py makemigrations`
`python manage.my migrate`

Once created, add the newly created migrations from `mainapp/migrations/` to the git repo and commit them.

Note: Make sure your `venv` is activated with `source venv/bin/activate`
 
