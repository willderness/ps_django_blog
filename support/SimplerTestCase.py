from django.test import SimpleTestCase
import sys, ast, os

class SimplerTestCase(SimpleTestCase):
    def __init__(self, *args):
        self.value = (sys.version_info >= (3, 8) and 'value') or 's'
        self.value_num = (sys.version_info >= (3, 8) and 'value') or 'n'
        super().__init__(*args)

    def assertTrue(self, expr, msg=None):
        if (not expr):
            self.fail(msg or (str(expr) + "is not True"))

    @staticmethod
    def load_ast_tree(filename):
        with open(filename) as f:
            fstr = f.read()
        return ast.parse(fstr, filename=filename)

    @staticmethod
    def check_keyword(keyword, arg, val_val=None, val_id=None, val_attr=None):
        if (keyword.arg == arg and
            ((val_val is not None and keyword.value.value == val_val) or
            ((val_id is not None and keyword.value.value.id == val_id) and 
            (val_attr is not None and keyword.value.attr == val_attr)))):
            return True
    
    def check_migration(self, migration_dir, model_name):
        print(migration_dir, model_name)
        for file in os.listdir(migration_dir):
            full_path = os.path.join(migration_dir, file)
            (path, ext) = os.path.splitext(full_path)
            if (os.path.isfile(full_path) and ext == '.py'):
                try:
                    for x in self.load_ast_tree(full_path).body:
                        if (isinstance(x, ast.ClassDef) and
                            x.name == 'Migration'):
                            for y in x.body:
                                if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'operations' and
                                    y.value.elts[0].func.attr == 'CreateModel' and
                                    y.value.elts[0].keywords[0].arg == 'name' and 
                                    getattr(y.value.elts[0].keywords[0].value, self.value) == model_name):
                                    return True
                except:
                    pass
        return False
