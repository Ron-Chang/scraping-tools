import os
import time
from datetime import datetime, timedelta


class SnapTimer:

    try:
        terminal_size = os.get_terminal_size(0)[0]
    except:
        terminal_size = 76

    def __init__(self, snap_interval, start=None, **kwargs):
        self.snap_interval = snap_interval
        self.start = start
        self.extra_info_dict = kwargs
        self._run()

    def _print_divider(self):
        print('=' * self.terminal_size)

    def _sleep(self):
        now = datetime.now()
        snap_interval = self.snap_interval
        snap_interval_hr = round(snap_interval/3600, 2)
        next_round = (now + timedelta(seconds=snap_interval)).strftime('%Y-%m-%d %H:%M')
        print(f'[{"INFO":10}]| SLEEP FOR : {snap_interval_hr} hrs.')
        print(f'[{"INFO":10}]| THE NEXT ROUND STARTING AT : {next_round} ')
        time.sleep(snap_interval)

    def _consume(self):
        if self.start is not None:
            print(f' = CONSUME : {round(time.time() - self.start, 2)} sec.')
        return None

    def _extra_info(self):
        if self.extra_info_dict:
            print('[EXTRA_INFO]| ')
            for extra_info_key, extra_info_value in self.extra_info_dict.items():
                print(f'[{extra_info_key.upper()[:10]:10}]| {extra_info_value}')
            print('-' * self.terminal_size)
        return None

    def _run(self):
        self._print_divider()
        self._extra_info()
        self._consume()
        self._sleep()
        self._print_divider()
