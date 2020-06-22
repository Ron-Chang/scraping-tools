import os
from datetime import datetime


class PPrint:
    try:
        _SCREEN_WIDTH = os.get_terminal_size(0)[0]
    except Exception as e:
        print(e)
        _SCREEN_WIDTH = 76

    _TAG_RESET = '\x1b[0m'
    _TAG_TEXT_RED= '\x1b[5;31m'
    _TAG_TEXT_YELLOW = '\x1b[5;33m'
    _TAG_TEXT_BLUE = '\x1b[5;34m'
    _TAG_BG_RED = '\x1b[7;31m'

    _FORMAT_LENGTH = len('\r[YYYY-mm-dd HH:MM:SS,fff] [12345678] [ * ]')

    def __init__(self, log=None, tag=None, dye=True):
        self.log = log
        self.tag = tag
        self.dye = dye
        self._run()

    @staticmethod
    def _format_now(format_='%Y-%m-%d %H:%M:%S,%f', datetime_=None):
        if not datetime_:
            return datetime.now().strftime(format_)
        return datetime_.strftime(format_)

    @staticmethod
    def _format_tag(tag):
        tag = tag or 'info'
        return f'{tag[:8].upper():<8}'

    def _dye(self, line):
        if not (self.tag and self.dye):
            return line
        if self.tag.lower() in ['critical', 'danger']:
            return f'{self._TAG_BG_RED}{line}{self._TAG_RESET}'
        elif self.tag.lower() in ['error']:
            return f'{self._TAG_TEXT_RED}{line}{self._TAG_RESET}'
        elif self.tag.lower() in ['warning']:
            return f'{self._TAG_TEXT_YELLOW}{line}{self._TAG_RESET}'
        else:
            return f'{self._TAG_TEXT_BLUE}{line}{self._TAG_RESET}'

    def _run(self):
        now = self._format_now()[:-3]
        if self.log is None:
            print(f'[{now}]')
            return None
        if not isinstance(self.log, str):
            self.log = str(self.log)
        log_limit = self._SCREEN_WIDTH - self._FORMAT_LENGTH
        if log_limit <= 0:
            print(self.log)
        tag = self._format_tag(tag=self.tag)
        log = f'{self.log[:log_limit - 3]}...' if len(self.log) > log_limit else self.log
        line = f'[{now}] [{tag}] [ * {log}]'
        print(self._dye(line=line))


if __name__ == '__main__':

    PPrint(f'{" SET with tag ":▼^24}')
    PPrint('This is a Demonstration!', tag='critical')
    PPrint('This is a Demonstration!', tag='error')
    PPrint('This is a Demonstration!', tag='warning')
    PPrint('This is a Demonstration!', tag='info')
    PPrint(f'{" SET with tag ":▲^24}')

    PPrint(f'{" SET without tag ":▼^24}')
    PPrint('This is a Demonstration!')
    PPrint(f'{" SET without tag ":▲^24}')

    PPrint(f'{" SET dye=False ":▼^24}')
    PPrint('This is a Demonstration!', tag='critical', dye=False)
    PPrint(f'{" SET dye=False ":▲^24}')

    PPrint(f'{" PUT nothing ":▼^24}')
    PPrint()
    PPrint(f'{" PUT nothing ":▲^24}')

    PPrint(f'{" PUT int ":▼^24}')
    PPrint(log=12)
    PPrint(f'{" PUT int ":▲^24}')

    PPrint(f'{" PUT comprehension ":▼^24}')
    PPrint(log={str(i): chr(i) for i in range(65, 97 + 1)})
    PPrint(f'{" PUT comprehension ":▲^24}')
