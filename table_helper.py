import os, sys, json, time

def append_parent_path(gen=None):
    """
    將父層納入索引
    :params gen: generation, default is 1.
    :type gen: int
    
    :rtype: None
    :return: Add root path into system source path list
    """
    gen = gen or 1
    path_folder = os.path.abspath(__file__).split('/')
    go_up = -(1 + gen)
    path = '/'.join(path_folder[:go_up])
    sys.path.append(path)
    print(f'[INFO    ] | Append path: "{sys.path[-1]}"')
append_parent_path(gen=1)

from app import db, create_app
from spyder_common import models

class TableHelper:

    def create_tables(app, db, models):
        """
        :params app: flask app
        :type app: obj
        :params db: flask db
        :type db: obj
        :params models: a list contain SALAlchemy orm.
        :type models: list

        :rtype: None
        :return: None
        """
        for model in models:
            bind = db.get_engine(app, bind=getattr(model, '__bind_key__'))
            getattr(model, '__table__').create(bind=bind, checkfirst=True)
            print(f'Create table {model.__name__}')

    def drop_tables(app, db, models):
        """
        :params app: flask app
        :type app: obj
        :params db: flask db
        :type db: obj
        :params models: a list contain SALAlchemy orm.
        :type models: list

        :rtype: None
        :return: None
        """
        for model in models:
            bind = db.get_engine(app, bind=getattr(model, '__bind_key__'))
            getattr(model, '__table__').drop(bind=bind, checkfirst=True)
            print(f'Create table {model.__name__}')

    def create_table(app, db, model):
        """
        :params app: flask app
        :type app: obj
        :params db: flask db
        :type db: obj
        :params model: SALAlchemy orm.
        :type models: object 

        :rtype: None
        :return: None
        """
        bind = db.get_engine(app, bind=getattr(model, '__bind_key__'))
        getattr(model, '__table__').create(bind=bind, checkfirst=True)
        print('--------------------------------------------------------------------------------')
        print(f'[{"Create":8}] [ * table {model.__name__}]')
        print('--------------------------------------------------------------------------------')

    def drop_table(app, db, model):
        """
        :params app: flask app
        :type app: obj
        :params db: flask db
        :type db: obj
        :params model: SALAlchemy orm.
        :type models: object 

        :rtype: None
        :return: None
        """
        bind = db.get_engine(app, bind=getattr(model, '__bind_key__'))
        getattr(model, '__table__').drop(bind=bind, checkfirst=True)
        print('--------------------------------------------------------------------------------')
        print(f'[{"Drop":8}] [ * table {model.__name__}]')
        print('--------------------------------------------------------------------------------')

if __name__ == '__main__':
    app = create_app()
    args = sys.argv
    if len(args) == 1 or not ('-c' in args or '-d' in args or '-r' in args):
        exit("""
        Input flags and table_name to \"create\", \"drop\" or \"rebuild\" table

        - c : create  table
        - d : drop    table
        - r : rebuild table

        Table name have to follow either one flag. 

        Noet: Drop table will be execute first.
        """)
    params = args[1:]
    
    if '-r' in params:
        flag_index = params.index('-r')
        try:
            model_name = params[flag_index + 1]
            model = getattr(models, model_name)
            time.sleep(0.25)
            confirm = input(f'Rebuild table \"{model_name}\"(y/n)?\n>>> ')
            if confirm.lower() in ['yes', 'y']:
                TableHelper.drop_table(app, db, model)
                TableHelper.create_table(app, db, model)
                exit('DONE!')
            else:
                exit('Process has been terminated!')
        except Exception as e:
            exit(e)

    if '-d' in params:
        flag_index = params.index('-d')
        try:
            model_name = params[flag_index + 1]
            model = getattr(models, model_name)
            time.sleep(0.25)
            confirm = input(f'Drop table \"{model_name}\"(y/n)?\n>>> ')
            if confirm.lower() in ['yes', 'y']:
                TableHelper.drop_table(app, db, model)
            else:
                exit('Process has been terminated!')
        except Exception as e:
            exit(e)

    if '-c' in params:
        flag_index = params.index('-c')
        try:
            model_name = params[flag_index + 1]
            model = getattr(models, model_name)
            TableHelper.create_table(app, db, model)
        except Exception as e:
            exit(e)

    exit('DONE!')

