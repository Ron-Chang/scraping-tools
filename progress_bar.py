import os


class ProgressBar:
    """
        :info: only display the first 10 letters.
        :description: only display the first 20 letters.
    """
    RESERVED_ROOM = 10

    def __init__(self,
            count, amount,
            info=None, description=None,
            bar_fg_unit='#', bar_bg_unit='_'
        ):
        self.count = count
        self.amount = amount
        self.info = info
        self.description = description
        self.bar_fg_unit = bar_fg_unit
        self.bar_bg_unit = bar_bg_unit

        self.validate()

        self.proceed_percentage = self._get_proceed_percentage()
        self.display_info = self._get_display_info()
        self.progress_bar_length = self._get_progress_bar_length()
        self._run()

    def validate(self):
        if not isinstance(self.count, int):
            raise Exception(
                f'[ERROR     ]| Invalid type of "count": {self.count} {type(self.count)}')
        if not isinstance(self.amount, int):
            raise Exception(
                f'[ERROR     ]| Invalid type of "amount": {self.amount} {type(self.amount)}')
        if self.count > self.amount:
            raise Exception(
                f'[ERROR     ]| "count" is greater than "amount": {self.count} > {self.amount}')

    @staticmethod
    def _get_console_width():
        try:
            console_width = os.get_terminal_size(0)[0]
        except:
            console_width = 76
        return console_width

    def _get_progress_bar_length(self):
        return self._get_console_width() - len(self.display_info) - self.RESERVED_ROOM

    def _get_proceed_percentage(self):
        return self.count / self.amount * 100

    def _get_progress_bar(self):
        fg_length = int(self.progress_bar_length * self.proceed_percentage / 100)
        bg_length = self.progress_bar_length - fg_length
        bar_fg = self.bar_fg_unit * fg_length
        bar_bg = self.bar_bg_unit * bg_length
        return bar_fg + bar_bg

    def _get_formated_info(self):
        if self.info is None:
            info = 'INFO'
        else:
            info = self.info[:10]
        return f'[{info:<10}]| '

    def _get_formated_description(self):
        if self.description is None:
            return f'{self.count:,} of {self.amount:,} | '
        else:
            return f'[{self.description[:20]:<20}]| '

    def _get_formated_proceed_percentage(self):
        return f'[{self.proceed_percentage:>6,.2f}%] '

    def _get_display_info(self):
        info = self._get_formated_info()
        description = self._get_formated_description()
        proceed_percentage = self._get_formated_proceed_percentage()
        return info + description + proceed_percentage

    def _run(self):
        progress_bar = self._get_progress_bar()
        if not self.proceed_percentage == 100:
            print(f'{self.display_info}|{progress_bar}|', end='\r', flush=True)
        else:
            print(f'{self.display_info}|{progress_bar}|' + ' DONE!')

if __name__ == '__main__':
    import time
    print('[Example]\n')
    for i in range(1,123+1):
        ProgressBar(count=i, amount=123)
        time.sleep(0.2)
