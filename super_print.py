import os


class SuperPrint:
    """
        Aiming to print test result easier as posible with mark and divider,
        It will make targets be observed obviously.
        How to use:
        SuperPrint(
            target          [Necessary]
            target_name     [Default: None]
            divider_symbol  [Default: '-']
            mark_symbol     [Default: 'None']
        )
        instance:
            test = [1, 2, 3, 4, 5, 6]
            SuperPrint(
                target=test,
                target_name='test',
                mark_symbol='*'
            )
        result:
            note: the divider as long as your current terminal width
            |-------------------------------------------------------|
            |* test: [1, 2, 3, 4, 5, 6]                             |
            |-------------------------------------------------------|
    """
    def __init__(self, target, target_name=None, divider_symbol='-', mark_symbol=None):
        self.target = target
        self.target_name = target_name
        self.divider_symbol = divider_symbol
        self.mark_symbol = mark_symbol
        self.terminal_size = self._get_console_width()
        self._run()

    @staticmethod
    def _get_console_width():
        try:
            console_width = os.get_terminal_size(0)[0]
        except:
            console_width = 76
        return console_width

    def _target_info(self):
        if self.mark_symbol and self.target_name:
            return f'{self.mark_symbol} {self.target_name}: {self.target}'
        elif self.target_name:
            return f'{self.target_name}: {self.target}'
        elif self.mark_symbol:
            return f'{self.mark_symbol} {self.target}'
        else:
            return f'{self.target}'

    def _print_divider(self):
        if self.divider_symbol:
            print(self.divider_symbol * self.terminal_size)

    def _print_target(self):
        print(self._target_info())

    def _run(self):
        self._print_divider()
        self._print_target()
