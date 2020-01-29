import ast, os
from support.SimplerTestCase import SimplerTestCase

class PostTestCase(SimplerTestCase):
    setup_run = False
    def setUp(self):
        if not self.setup_run:
            self.setup_run = True
            self.class_found = False 
            self.base_class_found = False 
            self.title_found = False 
            self.max_length_found = False 
            self.str_method_found = False
            self.clean_method_found = False
            self.clean_assign_found = False
            self.tags_field_found = False
            self.tag_many_to_many_found = False
            self.tag_view_found = False
            self.tag_view_set_title_found = False
            self.tag_view_return_params_found = False
            self.tag_view_post_dict_found = False
            self.tag_view_title_dict_found = False
            self.tag_view_get_object_found = False
            self.tag_view_blogpost_filter_found = False
            self.tag_view_name_assign_found = False

            # Task 8
            self.tag_posts_route_found = False
            self.tag_posts_view_found = False
            self.tag_posts_name_found = False

            # Task 9
            self.get_absolute_url_found = False
            self.get_absolute_url_return_found = False
            self.get_absolute_url_reverse_found = False
            self.get_absolute_url_post_found = False
            self.get_absolute_url_args_correct = False


    def check_model_file(self):
        try:
            for x in self.load_ast_tree('mainapp/models.py').body:
                if isinstance(x, ast.ClassDef):
                    if x.name == 'Tag':
                        self.class_found = True
                        if (len(x.bases) > 0 and
                            x.bases[0].value.id == 'models' and
                            x.bases[0].attr == 'Model'):
                            self.base_class_found = True
                        for y in x.body:
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'name' and
                                    y.value.func.value.id == 'models' and
                                    y.value.func.attr == 'CharField'):
                                self.title_found = True
                                if (y.value.keywords[0].arg == 'max_length' and
                                        getattr(y.value.keywords[0].value, self.value_num) == 50):
                                    self.max_length_found = True

                            if (isinstance(y, ast.FunctionDef) and
                                    y.name == '__str__' and y.args.args[0].arg == 'self'):
                                for z in y.body:
                                    if (isinstance(z, ast.Return) and
                                        z.value.value.id == 'self' and
                                        z.value.attr == 'name'):
                                        self.str_method_found = True
                                        
                            if (isinstance(y, ast.FunctionDef) and
                                    y.name == 'clean' and y.args.args[0].arg == 'self'):
                                self.clean_method_found = True
                                for z in y.body:
                                    if (isinstance(z, ast.Assign) and
                                        z.targets[0].value.id == 'self' and
                                        z.targets[0].attr == 'name' and 
                                        z.value.func.value.value.id == 'self' and
                                        z.value.func.value.attr == 'name' and
                                        z.value.func.attr == 'lower'):
                                        self.clean_assign_found = True
                            # Task 9
                            if (isinstance(y, ast.FunctionDef) and
                                y.name == 'get_absolute_url'):
                                self.get_absolute_url_found = True
                                if isinstance(y.body[0], ast.Return):
                                    self.get_absolute_url_return_found = True
                                    if y.body[0].value.func.id == 'reverse':
                                        self.get_absolute_url_reverse_found = True
                                        if getattr(y.body[0].value.args[0], self.value) == 'tag_posts':
                                            self.get_absolute_url_post_found = True
                                            if (y.body[0].value.keywords[0].arg == 'args' and
                                                y.body[0].value.keywords[0].value.elts[0].func.id == 'str' and
                                                y.body[0].value.keywords[0].value.elts[0].args[0].value.id == 'self' and
                                                y.body[0].value.keywords[0].value.elts[0].args[0].attr == 'name'):
                                                self.get_absolute_url_args_correct = True


                    elif x.name == 'BlogPost':
                        for y in x.body:
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'tags' and
                                    y.value.func.value.id == 'models' and
                                    y.value.func.attr == 'ManyToManyField'):
                                self.tags_field_found = True
                                if (len(y.value.keywords) > 0 and 
                                        y.value.keywords[0].arg == 'related_name' and
                                        getattr(y.value.keywords[0].value, self.value) == 'posts' and
                                        len(y.value.args) > 0 and
                                        getattr(y.value.args[0], self.value) == 'Tag'):
                                    self.tag_many_to_many_found = True
        except Exception as e:
            print(e)
            


    def test_task1_tag_model_exists(self):    
        """ Add Tag model to models.py
            class Tag(models.Model):
                name = models.CharField(max_length=50, unique=True) """
        self.check_model_file()

        self.assertTrue(self.class_found, msg="Did you create the `Tag` class?")
        self.assertTrue(self.base_class_found, msg="Make sure you added `models.Model` as the base class of `BlogPost`.")
        self.assertTrue(self.title_found, msg="Did you add the `name` field?")
        self.assertTrue(self.max_length_found, msg="Did you set `max_length` in the `CharField`?")

    def test_task2_clean_method_exists(self):
        """Add clean method to sanitize input."""
        self.check_model_file()

        self.assertTrue(self.clean_method_found, msg="Did you implement the `clean` method in the `Tag` model class?")
        self.assertTrue(self.clean_assign_found, msg="Did you assign to `self.name` in the `clean` method?")

    def test_task3_str_exists(self):
        self.check_model_file()
        self.assertTrue(self.str_method_found, msg="Did you implement the `__str__` method in the `Tag` model class?")

    def test_task4_many_to_many_exists(self):
        self.check_model_file()
        self.assertTrue(self.tags_field_found, msg="Did you add the `name` field?")
        self.assertTrue(self.tag_many_to_many_found, msg="Did you set `tags` equal to the `ManyToManyField`?")
   
    def check_views_file(self):
        try:
            for x in self.load_ast_tree('mainapp/views.py').body:
                if type(x) is ast.FunctionDef:   
                    if (x.name == 'tag_posts'):
                        self.tag_view_found = True
                        for y in x.body:
                            if (isinstance(y, ast.Return) and 
                                y.value.func.id == 'render' and 
                                len(y.value.args) >= 2 and 
                                y.value.args[0].id == 'request' and 
                                getattr(y.value.args[1], self.value) == 'mainapp/filtered_post_list.html'):
                                self.tag_view_return_params_found = True
                                if (len(y.value.args) >= 3 and
                                    isinstance(y.value.args[2], ast.Dict)):
                                    for z in y.value.args[2].keys:
                                        if (getattr(z, self.value) == 'title'):
                                            self.tag_view_title_dict_found = True
                                        if (getattr(z, self.value) == 'posts'):
                                            self.tag_view_post_dict_found = True
                                        
                            elif (isinstance(y, ast.Assign) and
                                  y.targets[0].id == 'title' and 
                                  getattr(y.value.func.value, self.value) == "Posts about {}" and
                                  y.value.func.attr == 'format' and
                                  len(y.value.args) > 0 and
                                  y.value.args[0].id == 'name'):
                                self.tag_view_set_title_found = True

                            elif (isinstance(y, ast.Assign) and
                                  y.targets[0].id == 'name' and
                                  y.value.func.value.id == 'name' and
                                  y.value.func.attr == 'lower'):
                                self.tag_view_name_assign_found = True

                            elif (isinstance(y, ast.Assign) and
                                  y.targets[0].id == 'tag' and 
                                  y.value.func.id == 'get_object_or_404'):
                                self.tag_view_get_object_found = True

                            elif (isinstance(y, ast.Assign) and
                                  y.targets[0].id == 'posts' and 
                                  y.value.func.value.value.id == 'BlogPost' and
                                  y.value.func.value.attr == 'objects' and 
                                  y.value.func.attr == 'filter'):
                                self.tag_view_blogpost_filter_found = True
        except Exception as e:
            print(e)
            # Catch any bad things that happened above and fail the test.
            pass
        
    def test_task5_tag_view(self):
        self.check_views_file()

        self.assertTrue(self.tag_view_found, msg="Did you create the `tag_post` function?")
        self.assertTrue(self.tag_view_return_params_found, msg="Did you return the result of the `render` function?")

    def test_task6_tag_view_title(self):
        self.check_views_file()                                    
        self.assertTrue(self.tag_view_name_assign_found, msg="Did you lowercase `name` in the `tag_post` method?")
        self.assertTrue(self.tag_view_set_title_found, msg="Did you set the `title` string in `tag_post`?")
        self.assertTrue(self.tag_view_title_dict_found, msg="Did you pass the `title` field to the `render` function?")                                
    def test_task7_tag_view_find_posts(self):
        self.check_views_file()

        self.assertTrue(self.tag_view_get_object_found, msg="Did you set `tag` to `get_object_or_404`'s result?")
        self.assertTrue(self.tag_view_blogpost_filter_found, msg="Did you set `posts` to `BlogPost.objects.filter`'s result?")
     
    def test_task8_add_tag_url(self):
        # path('tag/<str:name>', views.tag_posts, name='tag_posts')
        self.check_urls_file()
        self.assertTrue(self.tag_posts_route_found, msg="Did you add the tag path to urls.py with the route `'tag/<str:name>'`?")
        self.assertTrue(self.tag_posts_view_found, msg="Did you add the tag path to urls.py with the view `views.tag_posts`?")
        self.assertTrue(self.tag_posts_name_found, msg="Did you add the tag path to urls.py with the `name = 'tag_posts'`?")

    def check_urls_file(self):
        try:
            for x in self.load_ast_tree('mainapp/urls.py').body:
                if type(x) is ast.Assign:   
                    if (x.targets[0].id == 'urlpatterns'):
                        for y in x.value.elts:
                            if type(y) is ast.Call: 
                                if getattr(y.args[0], self.value) == 'tag/<str:name>':
                                    self.tag_posts_route_found = True
                                if (y.args[1].value.id == 'views' and 
                                    y.args[1].attr == 'tag_posts'):
                                    self.tag_posts_view_found = True
                                if (y.keywords[0].arg == 'name' and 
                                    getattr(y.keywords[0].value, self.value) == 'tag_posts'):
                                    self.tag_posts_name_found = True
        except Exception as e:
            print(e)
            # Catch any bad things that happened above and fail the test.
            pass

    def test_task9_url_reverser(self):
        # def get_absolute_url(self):
        #     return reverse('tag_posts', args=[str(self.name)])
        self.check_model_file()
        self.assertTrue(self.get_absolute_url_found, msg="The method `get_absolute_url()` does not exist in the BlogPost model.")
        self.assertTrue(self.get_absolute_url_return_found, msg="The method `get_absolute_url()` does not return anything.")
        self.assertTrue(self.get_absolute_url_reverse_found, msg="The method `get_absolute_url()` does not call `reverse()`.")
        self.assertTrue(self.get_absolute_url_post_found, msg="In `get_absolute_url()` the first argument in `reverse()` should be `'tag_posts'`.")
        self.assertTrue(self.get_absolute_url_args_correct, msg="In `get_absolute_url()` the second argument in `reverse()` should be `args=[str(self.name)]`.")

    def test_task10_uncomment_templates(self):
        # Remove `{% comment %}` and {% endcomment %} tags from 
        # `templates/mainapp/snippet_post_list.html` & `templates/mainapp/post.html`
        filenames = ['mainapp/templates/mainapp/snippet_post_list.html',
                    'mainapp/templates/mainapp/post.html']

        for filename in filenames:
            comment_found, endcomment_found = self.check_for_comments(filename)

            self.assertTrue(not comment_found, msg="There is still a `{% comment %}` tag in `" + filename + "`")
            self.assertTrue(not endcomment_found, msg="There is still an `{% endcomment %}` tag in `" + filename + "`")

    def test_task11_admin_register_tag(self):
        # from .models import BlogPost, Tag
        #   admin.site.register(Tag)
        import_Tag_found = False
        admin_site_register_found = False

        try:
            for x in self.load_ast_tree('mainapp/admin.py').body:
                if type(x) is ast.ImportFrom:
                    if x.module == 'models' and (x.names[0].name == 'Tag' or x.names[1].name == 'Tag'):
                        import_Tag_found = True
                elif type(x) is ast.Expr:   
                    if (x.value.func.value.value.id == 'admin' and 
                        x.value.func.value.attr == 'site' and
                        x.value.func.attr == 'register'):
                        if (x.value.args[0].id == 'Tag'):
                            admin_site_register_found = True
        except:
            # Catch any bad things that happened above and fail the test.
            pass
        
        self.assertTrue(import_Tag_found, msg="Did you import `Tag`?")
        self.assertTrue(admin_site_register_found, msg="Did you register the `Tag` model to the admin site?")

    def test_task12_make_migrations(self):
        msg = "Did you use `manage.py makemigrations` to create the `Tag` migrations file? Don't forget to `add` it to the git repo."
        self.assertTrue(os.path.isdir('mainapp/migrations/'), msg=msg)
        self.assertTrue(self.check_migration('mainapp/migrations/', 'Tag'), msg=msg)
    

        
        
