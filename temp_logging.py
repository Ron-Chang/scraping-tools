import os
from datetime import datetime


class TempLogging:

    def __init__(self, name='temp', path='log/temp_log'):
        self.path = path
        self.filename = f'{name}_{datetime.now().strftime("%Y-%m-%dT%H:%M")}.txt'
        self.pathname = os.path.join(self.path, self.filename)
        self._make_dirs()
        self._create_file()

    def _get_now(self, format_='%Y-%m-%dT%H:%M:%S,%f', datetime_=datetime.now()):
        return datetime_.strftime(format_)

    def _make_dirs(self):
        os.makedirs(self.path, exist_ok=True)

    def _create_file(self):
        with open(self.pathname, 'w') as fw:
            print(f'[{self._get_now()[:-3]}] [{"INFO":8}] [ * Start logging {self.filename}!]')

    def add(self, log, display=False):
        if display:
            print(f'[{self._get_now()[:-3]}] [{"INFO":8}] [ * {log[:40]}]')
        with open(self.pathname, 'a') as fw:
            fw.write(f'{log}\n')


