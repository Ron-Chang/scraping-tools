import sys, inspect, importlib, random
from datetime import datetime
from flask_apscheduler import APScheduler


class DatabasePacemaker:
    """
    Pacemaker: 心律起博器
    """
    @staticmethod
    def _get_models_list(modules):
        models = list()
        for module in modules:
            importlib.import_module(module)
            models.append(sys.modules[module])
        return models

    @staticmethod
    def _get_db_binds(config):
        db_binds = getattr(config, 'SQLALCHEMY_BINDS', dict())
        return set(db_binds.keys()) if db_binds else dict()

    @staticmethod
    def _is_table(obj, db_binds):
        if not obj.__class__.__name__ is 'DefaultMeta':
            return False
        if not obj.__bind_key__ in db_binds:
            return False
        return True

    @classmethod
    def _get_all_tables_by_db(cls, db_binds, models_list):
        db_tables = dict()
        for models in models_list:
            for name, obj in inspect.getmembers(models):
                if not cls._is_table(obj=obj, db_binds=db_binds):
                    continue
                if obj.__bind_key__ not in db_tables:
                    db_tables.update({obj.__bind_key__: list()})
                db_tables[obj.__bind_key__].append(obj)
        return db_tables

    @staticmethod
    def _random_pick(tables):
        return tables[random.randint(0, len(tables) - 1)]

    @classmethod
    def _get_random_tables(cls, db_binds, models_list):
        tables_by_db = cls._get_all_tables_by_db(db_binds, models_list)
        if not tables_by_db:
            return None
        return {db: cls._random_pick(tables) for db, tables in tables_by_db.items()}

    @staticmethod
    def _poke(db, table):
        table.query.first()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{"CONNECT":10}]| [{now}]| {db.upper():15} - {table.__name__}')

    @classmethod
    def awake(cls, config, modules):
        """透過query每個db 亂數取一的table，以保持db連線狀態。
        :params config: flask config
        :type config: <class 'config.Config'>

        :params modules: db models pathname, it supposed to split by '.'
        :type modules: list['modelspath_1.models', 'modelspath_2.models']

        :return: keep db connection
        """
        db_binds = cls._get_db_binds(config)
        models_list = cls._get_models_list(modules)
        for db, table in cls._get_random_tables(db_binds, models_list).items():
            cls._poke(db=db, table=table)

    @staticmethod
    def _launch_scheduler(app, scheduler, task):
        """
        若 scheduler 不為空
            - 暫停scheduler
            - 插入任務
            - 重啟scheduler
        否則
            - 建立實體
            - 重啟app
            - 啟動scheduler
        """
        if scheduler:
            scheduler.pause()
            scheduler.add_job(**task)
            scheduler.resume()
        else:
            scheduler = APScheduler()
            scheduler.add_job(**task)
            scheduler.init_app(app)
            scheduler.start()

    @classmethod
    def run(cls, app, config, modules, seconds, submodule=None, scheduler=None):
        """檢查載入scheduler, 插入喚醒db任務
        :params app: flask app
        :type app: <class 'flask.app.Flask'>

        :params config: flask config
        :type config: <class 'config.Config'>

        :params modules: db models pathname, it supposed to split by '.'
        :type modules: list, ['models_path_1.models', 'models_path_2.models']

        :params seconds: awake task interval
        :type seconds: int

        :params submodule: this file path from entry, it supposed to split by '.'
        :type submodule: str

        :params scheduler: flask_apscheduler
        :type scheduler: <class 'flask_apscheduler.scheduler.APScheduler'>
        """
        function = 'db_pacemaker:DatabasePacemaker.awake'

        task = {
            'id': 'keep_db_connection',
            'func': f'{submodule}.{function}' if submodule else function,
            'kwargs': {'config': config, 'modules': modules},
            'trigger': 'interval',
            'seconds': seconds
        }

        cls._launch_scheduler(app=app, scheduler=scheduler, task=task)
