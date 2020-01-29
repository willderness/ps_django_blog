
# Add Tag model

We want to be able to add tags to each post in order to organize them better by topic.  To do that we'll create a new `Tag` model.  Create the `Tag` model by adding a new class into `mainapp/models.py`. Name the class `Tag` and make it extend `models.Model`. In the class body, add a field called `name` and set it to `models.CharField()`. Pass it a `max_length` of `50`.
```python
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
```

# Add method to sanitize tag input

We want all of the tags to be lowercase. To the `Tag` class, add a class method named `clean` that will set `self.name` to a lowercase version of itself.

```python
    def clean(self):
        self.name = self.name.lower()
```

# Add a string method to make Tag objects readable

To the `Tag` class, add a `__str__` method that returns `self.name`.

```python
    def __str__(self):
        return self.name
```

# Add many to many relationship to BlogPost model for Tags

Since we want tags to categorize posts by topic, we want to create a relationship between the `Tag` model and the `BlogPost` model.  In the `BlogPost` class, add `tags` as a field and set it equal to calling `models.ManyToManyField()` with `'Tag'` and `related_name='posts'` as arguments.
```python
    tags = models.ManyToManyField('Tag', related_name='posts')
```

# Add view to show all posts with a given tag

We would like to display a Tag page that displays all of the posts with that Tag.  In order to do that, we need to create a view that will generate that page.  In `mainapp/views.py`, create a function `tag_posts(request, name)`.  In that method, simply return `render(request, 'mainapp/filtered_post_list.html')`.


```python
def tag_posts(request, name):
    return render(request, 'mainapp/filtered_post_list.html')
```

# Pass title to template

Continuing in the `tag_posts` method, we want to pass a title for the `Tag` page to the template.  Before the `return` line, clean the incoming `name` parameter by setting it equal to a lowercase version of itself (e.g. `name.lower()` ).  Then, also before the `return`,  create a `title` variable and set it equal to `"Posts about {}".format(name)`. To pass the `title` to the template, add a dictionary as another argument to the end of the `render()` call. In the dictionary, set `'title'` to the new `title` variable. 

```python
def tag_posts(request, name):
    name = name.lower()
    title = "Posts about {}".format(name)

    return render(request, 'mainapp/filtered_post_list.html', {'title':title})
```

# Find posts and pass to template

Since we want to display all of the posts with the name tag, let's first find the Tag object.  Right after the `title` line, call `get_object_or_404(Tag, name=name)` and set that equal to a variable named `tag`.  Then, get all of the posts with that tag by calling `BlogPost.objects.filter(tags=tag)` and setting the result equal to a variable named `posts`. Finally, pass the `posts` list to the template by adding `'posts':posts` to the dict in the `render()` call, `{'posts':posts, 'title':title}`.

```python
def tag_posts(request, name):
    name = name.lower()
    title = "Posts about {}".format(name)
    
    tag = get_object_or_404(Tag, name=name)
    posts = BlogPost.objects.filter(tags=tag)

    return render(request, 'mainapp/filtered_post_list.html', {'posts':posts, 'title':title})
```

# Add tag path and new view to routes

In `mainapp/urls.py` add a new `path` entry into the `urlpatterns` list. Pass ``'tag/<str:name>'`` as the URL, ``'views.tag_posts'`` as the view, and set `name` to `'tag_posts'`.

```python
    path('tag/<str:name>', views.tag_posts, name='tag_posts'),
```

# Add url reverser to Tag model

To generate a url for the specified tag page, we can use `django.urls` `reverse()` function to generate the url from the view. Back in the `Tag` class, in `mainapp/models.py`, create a method `get_absolute_url(self)` that returns `reverse('tag_posts', args=[str(self.name)])`. Where `tag_posts` is the name of the URL we just named. 
```python
    def get_absolute_url(self):
        return reverse('tag_posts', args=[str(self.name)])
```

# Uncomment tag section of index and post templates

Remove `{% comment %}` and `{% endcomment %}` tags from both `mainapp/templates/mainapp/snippet_post_list.html` and `mainapp/templates/mainapp/post.html`.

# Add tags to the admin site

Register tags on the admin site by first importing `Tag` from `.models` in `mainapp/admin.py`. Then call `admin.site.register` on the `Tag` model.


```python
from .models import BlogPost, Tag
admin.site.register(Tag)
```

# Make migrations and migrate

Now that we’ve added our last model, `Tag`, we're ready for our final migration. From the command line, inside the root of the project, run the following commands:

```python
python manage.py makemigrations
python manage.my migrate
```

Once created, add the newly created migrations from `mainapp/migrations/` to the git repo and commit them.

Note: Make sure your `venv` is activated with `source venv/bin/activate`.
 
