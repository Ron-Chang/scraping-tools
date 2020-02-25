# built-in
import os, csv, inspect, time, subprocess
from datetime import datetime, timedelta
# 3rd-party
from flask_sqlalchemy import DefaultMeta
# submodule
from scraping_tools.super_print import SuperPrint
from scraping_tools.progress_bar import ProgressBar
from scraping_tools.snap_timer import SnapTimer
from scraping_tools.log_stash import LogStash
from scraping_tools.utils import Utils, DecoratorUtils
# project
from core import models
from config import Config


class BackupDatabase:

    def __init__(self, models, now, backup_dir):
        self.models = models
        self.now = now
        self.backup_dir = backup_dir
        self.models_name = Config.DB_NAME

        self._run()

    @staticmethod
    def get_column_names(table):
        table_obj = table.__dict__
        data_fields = list()
        for key, value in table_obj.items():
            if key.startswith('_'):
                continue
            value_dict = value.__dict__
            comparator = value_dict['comparator']
            comparator_dict = comparator.__dict__
            data_type = comparator_dict.get('type', None)
            python_data_type = getattr(data_type, 'python_type', None)
            if python_data_type:
                data_fields.append(key)
        return data_fields

    @classmethod
    def _slice_query(cls, table, table_name_camel, slice_length=2000):
        '''
            切片迭代資料庫
        '''
        count = 0
        data_list = list()
        while True:
            start = slice_length * count
            _slice = table.query.slice(
                start,
                slice_length + start
            ).all()
            if not _slice:
                print(f'[SLICE     ]| {table_name_camel[:20]:21}| {(count + 1):11} Times '
                f'{(slice_length * count):,} Qty.')
                break
            data_list.extend([data for data in _slice])
            if len(_slice) < slice_length:
                print(f'[SLICE     ]| {table_name_camel[:20]:21}| {(count + 1):11} Times '
                    f'{(slice_length * count + len(_slice)):,} Qty.')
                break
            count += 1
            print(f'[SLICE     ]| {table_name_camel[:20]:21}| {(count + 1):11} Times '
                f'{(slice_length * count):,} Qty.', end='\r', flush=True)
        return data_list

    @classmethod
    def _convert_table_to_list(cls, table_name_camel, table):
        column_names = cls.get_column_names(table=table)
        data_list = cls._slice_query(table=table, table_name_camel=table_name_camel, slice_length=4000)
        amount = len(data_list)
        count = 0
        results = list()
        for data in data_list:
            results.append({name: getattr(data, name) for name in column_names})
            count += 1
            ProgressBar(count=count, amount=amount, info='<< BACKUP', description=f'{table_name_camel}')
        return results

    def _get_tables(self):
        tables = dict()
        for name, table in inspect.getmembers(self.models):
            if isinstance(table, DefaultMeta):
                tables.update({table.__name__: table})
        return tables

    @staticmethod
    def _get_format_datetime(datetime_, format_='backup_%Y_%m_%dT%H_%M_%S'):
        return datetime_.strftime(format_)

    def _get_backup_path(self):
        format_datetime = self._get_format_datetime(datetime_=self.now)
        return os.path.join(self.backup_dir, format_datetime, self.models_name)

    @staticmethod
    def _make_directories(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def _export(table_name, backup_path, table_list):
        fieldnames = table_list[0].keys()
        delimiter = ','
        quotechar = '|'
        quoting = csv.QUOTE_ALL
        file_pathname = os.path.join(backup_path, f'{table_name}.csv')
        with open(file_pathname, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                f=csvfile, fieldnames=fieldnames,
                delimiter=delimiter, quotechar=quotechar, quoting=quoting)
            writer.writeheader()
            amount = len(table_list)
            count = 0
            for data in table_list:
                for key, value in data.items():
                    if value is None:
                        data.update({key: 'NULL'})
                writer.writerow(data)
                count += 1
                ProgressBar(count=count, amount=amount, info='EXPORT >>', description=f'{table_name}')

    def _exec(self):
        """
            直接備份至 submodule('spyder_initial_data/data/') 之下,
            改變備份資料,手動從指定日期資料夾取出覆蓋外部 'primary_db', 'secondary_db' and 'tertiary_db'
            資料夾格式 'backup_%Y_%m_%dT%H_%M_%S' -> 'backup_2020_02_18T17_28_54'
        """
        tables = self._get_tables()
        backup_path = self._get_backup_path()
        self._make_directories(path=backup_path)

        for table_name_camel, table in tables.items():
            table_list = self._convert_table_to_list(table_name_camel=table_name_camel, table=table)
            if not table_list:
                continue
            table_name = Utils.camel_to_underscore(letters=table_name_camel)
            self._export(table_name=table_name, backup_path=backup_path, table_list=table_list)

    @DecoratorUtils.snap_interval(days=14)
    def _run(self, snap_interval):
            while True:
                start = time.time()
                try:
                    self._exec()
                except Exception as e:
                    LogStash.error(e)
                SnapTimer(snap_interval=snap_interval, start=start)
