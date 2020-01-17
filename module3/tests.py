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
            self.settings_import_found = False
            self.author_field_found = False
            self.author_user_model_found = False
            self.author_on_delete_found = False
            self.author_related_name_found = False
            self.body_field_found = False
            self.postdate_field_found = False
            self.postdate_auto_now_found = False
            self.postdata_blank_found = False
            self.str_method_found = False
            self.get_abs_url_found = False

            self.check_model_file()

    def check_model_file(self):
        try:
            for x in self.load_ast_tree('mainapp/models.py').body:
                if isinstance(x, ast.ImportFrom):
                    if x.module == 'django.conf' and x.names[0].name == 'settings':
                        self.settings_import_found = True

                if isinstance(x, ast.ClassDef):
                    if x.name == 'BlogPost':
                        self.class_found = True
                        if (len(x.bases) > 0 and
                            x.bases[0].value.id == 'models' and
                            x.bases[0].attr == 'Model'):
                            self.base_class_found = True
                        for y in x.body:
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'title' and
                                    y.value.func.value.id == 'models' and
                                    y.value.func.attr == 'CharField'):
                                self.title_found = True
                                if (y.value.keywords[0].arg == 'max_length' and
                                        getattr(y.value.keywords[0].value, self.value_num) == 200):
                                    self.max_length_found = True
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'author' and
                                    y.value.func.value.id == 'models' and 
                                    y.value.func.attr == 'ForeignKey'):
                                self.author_field_found = True
                                if (y.value.args[0].value.id == 'settings' and
                                    y.value.args[0].attr == 'AUTH_USER_MODEL'):
                                    self.author_user_model_found = True
                                for keyword in y.value.keywords:
                                    if (keyword.arg == 'related_name' and 
                                        getattr(keyword.value, self.value) == 'posts'):
                                        self.author_related_name_found = True
                                    if (keyword.arg == 'on_delete' and 
                                        keyword.value.value.id == 'models' and 
                                        keyword.value.attr == 'CASCADE'):
                                        self.author_on_delete_found = True
                                    if (keyword.arg == 'model' and
                                        keyword.value.value.id == 'settings' and 
                                        keyword.value.attr == 'AUTH_USER_MODEL'):
                                        self.author_user_model_found = True
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'body' and
                                    y.value.func.value.id == 'models' and
                                    y.value.func.attr == 'TextField'):
                                self.body_field_found = True
                            if (isinstance(y, ast.Assign) and 
                                    y.targets[0].id == 'postdate' and
                                    y.value.func.value.id == 'models' and 
                                    y.value.func.attr == 'DateTimeField'):
                                self.postdate_field_found = True
                                for keyword in y.value.keywords:
                                    if (self.check_keyword(keyword, 'auto_now_add', True)):
                                        self.postdate_auto_now_found = True
                                    if (self.check_keyword(keyword, 'blank', True)):
                                        self.postdata_blank_found = True
                            if (isinstance(y, ast.FunctionDef) and
                                    y.name == '__str__' and
                                    y.args.args[0].arg == 'self'):
                                for z in y.body:
                                    if (isinstance(z, ast.Return) and
                                        z.value.value.id == 'self' and
                                        z.value.attr == 'title'):
                                        self.str_method_found = True
                            if (isinstance(y, ast.FunctionDef) and
                                    y.name == 'get_absolute_url' and
                                    y.args.args[0].arg == 'self'):
                                self.get_abs_url_found = self.check_get_abs_url(y.body)

        except:
            pass

    def check_get_abs_url(self, body):
        for z in body:
            if (isinstance(z, ast.Return) and 
                z.value.func.id == 'reverse' and 
                getattr(z.value.args[0], self.value) == 'post' and
                z.value.keywords[0].value.elts[0].args[0].value.id == 'self' and
                z.value.keywords[0].value.elts[0].args[0].attr == 'id'):
                return True


    def test_task1_post_model_exists(self):    
        """class BlogPost(models.Model):
            title = models.CharField(max_length=200)"""
        
        self.assertTrue(self.class_found, msg="Did you create the `BlogPost` class?")
        self.assertTrue(self.base_class_found, msg="Make sure you added `models.Model` as the base class of `BlogPost`.")
        self.assertTrue(self.title_found, msg="Did you add the `title` field?")
        self.assertTrue(self.max_length_found, msg="Did you set `max_length` in the `CharField`?")
        
    def test_task2_author_exists(self):
        """author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        on_delete=models.CASCADE,
        )"""
        
        self.assertTrue(self.settings_import_found, msg="Did you import `django.conf`'s `settings`")
        self.assertTrue(self.author_field_found, msg="Did you add the author field?")
        self.assertTrue(self.author_user_model_found, msg="Did you pass `AUTH_USER_MODEL` to `ForeignKey`?")
        self.assertTrue(self.author_related_name_found, msg="Did you set the `related_name` field in `ForeignKey`?")
        self.assertTrue(self.author_on_delete_found, msg="Did you set the `on_delete` field in `ForeignKey`?")

    def test_task3_body_exists(self):
        """ Add another field to `BlogPost` called `body` with type
        `models.TextField()`"""

        self.assertTrue(self.body_field_found, msg="Did you add the `body` field?")

    def test_task4_postdate_exists(self):
        """`postdate = models.DateTimeField(auto_now_add=True, blank=True)`"""
        self.assertTrue(self.postdate_field_found, msg="Did you add the `postdate` field and parameters?")
        self.assertTrue(self.postdate_auto_now_found, msg="Did you add `auto_now_add` to the `postdate` field?")
        self.assertTrue(self.postdata_blank_found, msg="Did you add the `blank` parameter to the `postdate` field?")

    def test_task5_str_exists(self):
        self.assertTrue(self.str_method_found, msg="Did you implement the `__str__` method in the `post` model class?")
    
    def test_task6_get_abs_url_exists(self):
        self.assertTrue(self.get_abs_url_found, msg="Did you implement the `get_absolute_url` method?")

    def test_task7_register_model_in_admin(self):
        import_BlogPost_found = False
        admin_site_register_found = False

        try:
            for x in self.load_ast_tree('mainapp/admin.py').body:
                if type(x) is ast.ImportFrom:
                    if x.module == 'models' and x.names[0].name == 'BlogPost':
                        import_BlogPost_found = True
                elif type(x) is ast.Expr:   
                    if (x.value.func.value.value.id == 'admin' and 
                        x.value.func.value.attr == 'site' and
                        x.value.func.attr == 'register'):
                        if (x.value.args[0].id == 'BlogPost'):
                            admin_site_register_found = True
        except:
            # Catch any bad things that happened above and fail the test.
            pass
        
        self.assertTrue(import_BlogPost_found, msg="Did you import `BlogPost`?")
        self.assertTrue(admin_site_register_found, msg="Did you remember to register the model to the admin site?")

    def test_task8_update_views_with_BlogPost(self):
        # Now we need to update `mainapp/views.py` to include our new `BlogPost` model. 
        # First let's import the `BlogPost` model from `.models`. 
        # Also import the `get_object_or_404` method from `django.shortcuts`.
        # Next in the `index` method, set the `posts` variable to `BlogPost.objects.all()` 
        # instead of `ALL_POSTS`.    

        import_BlogPost_found = False
        import_404_found = False
        set_posts = False

        try:
            for x in self.load_ast_tree('mainapp/views.py').body:
                if type(x) is ast.ImportFrom:
                    if x.module == 'models' and x.names[0].name == 'BlogPost':
                        import_BlogPost_found = True
                    elif x.module == 'django.shortcuts':
                        import_404_found = next((True for y in x.names if y.name == 'get_object_or_404'), False) or import_404_found
                elif type(x) is ast.FunctionDef:   
                    if (x.name == 'index'):
                        for y in x.body:
                            if type(y) is ast.Assign:
                                if (y.value.func.value.value.id == 'BlogPost' 
                                and y.value.func.value.attr == 'objects'
                                and y.value.func.attr == 'all'):
                                    set_posts = True
        except:
            # Catch any bad things that happened above and fail the test.
            pass
        
        self.assertTrue(import_BlogPost_found, msg="Did you import `BlogPost`?")
        self.assertTrue(import_404_found, msg="Did you import `get_object_or_404`?")
        self.assertTrue(set_posts, msg="Did you set `posts` equal to `BlogPost.objects.all()`?")


    def test_task9_update_post_view_with_BlogPost(self):
        try_catch_found = False
        set_posts_found = False
        get_objects_params_found = False

        try:
            for x in self.load_ast_tree('mainapp/views.py').body:
                if type(x) is ast.FunctionDef and x.name == 'post':
                    for y in x.body:
                        if type(y) is ast.Try:
                            try_catch_found = True
                        if type(y) is ast.Assign:
                            if (y.targets[0].id == 'post' and
                                y.value.func.id == 'get_object_or_404'):
                                set_posts_found = True
                                if (y.value.args[0].id == 'BlogPost' and 
                                    y.value.keywords[0].arg == 'pk' and
                                    y.value.keywords[0].value.id == 'id'):
                                    get_objects_params_found = True
        except:
            # Catch any bad things that happened above and fail the test.
            pass
        
        self.assertTrue(try_catch_found == False, msg="Did you remove the `try/catch` block?")
        self.assertTrue(set_posts_found, msg="Did you set `post` equal to `get_object_or_404`?")
        self.assertTrue(get_objects_params_found, msg="Check the parameters to `get_object_or_404`.")

    def test_task10_make_migrations(self):
        msg = "Did you use `manage.py makemigrations` to create the `BlogPost` migrations file? Don't forget to `add` it to the git repo."
        self.assertTrue(os.path.isdir('mainapp/migrations/'), msg=msg)
        self.assertTrue(self.check_migration('mainapp/migrations/', 'BlogPost'), msg=msg)
