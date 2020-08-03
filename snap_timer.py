import os
import time
from datetime import datetime, timedelta


class SnapTimer:

    try:
        terminal_size = os.get_terminal_size(0)[0]
    except:
        terminal_size = 76

    def __init__(self, snap_interval, start=None, name=None, **kwargs):
        self.snap_interval = snap_interval
        self.start = start
        self.extra_info_dict = kwargs
        self.name = name
        self._run()

    def _print_divider(self):
        print('=' * self.terminal_size)

    @staticmethod
    def _fmt_datetime(timedelta_=None, datetime_=None):
        format_ = '%Y-%m-%d %H:%M:%S,%f'
        if datetime_ and timedelta_:
            return (datetime_ + timedelta_).strftime(format_)[:-3]
        if datetime_:
            return datetime_.strftime(format_)[:-3]
        if timedelta_:
            return (datetime.now() + timedelta_).strftime(format_)[:-3]
        return datetime.now().strftime(format_)[:-3]

    @staticmethod
    def _fmt_interval(seconds):
        if seconds >= 60 * 60 * 24:
            return f'{round(seconds / (60 * 60 * 24), 2)} days.'
        if seconds >= 60 * 60:
            return f'{round(seconds / (60 * 60), 2)} hours.'
        if seconds >= 60:
            return f'{round(seconds / 60, 2)} minutes.'
        return f'{round(seconds, 2)} seconds.'

    def _sleep(self):
        fmt_interval = self._fmt_interval(self.snap_interval)
        timedelta_ = timedelta(seconds=self.snap_interval)
        next_round = self._fmt_datetime(timedelta_=timedelta_)
        if self.name is not None:
            print(f'[{self._fmt_datetime()}] [{"INFO":8}] [ * FINISH ✅ : {self.name}]')
        print(f'[{self._fmt_datetime()}] [{"INFO":8}] [ * SLEEP : {fmt_interval}]')
        print(f'[{self._fmt_datetime()}] [{"INFO":8}] [ * NEXT ROUND : {next_round}]')
        self._print_divider()
        time.sleep(self.snap_interval)

    def _consume(self):
        if self.start is not None:
            print(f'[{self._fmt_datetime()}] [{"CONSUME":8}] [ * {round(time.time() - self.start, 2)} sec.]')
        return None

    def _extra_info(self):
        if self.extra_info_dict:
            print(' * Extra infomation')
            for extra_info_key, extra_info_value in self.extra_info_dict.items():
                print(f'[{self._fmt_datetime()}] [{extra_info_key.upper()[:8]:8}] [ * {extra_info_value}]')
        return None

    def _run(self):
        self._print_divider()
        self._extra_info()
        self._consume()
        self._sleep()
