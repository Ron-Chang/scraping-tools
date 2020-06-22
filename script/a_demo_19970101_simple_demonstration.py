

class Patch19970101Demo:

    @staticmethod
    def _do_something():
        print(f'\x1b[1;44m[{"DEMO":^34}]\x1b[0m '
              f'\x1b[1;43m[ * THIS IS A SIMPLE DEMONSTRATION!]\x1b[0m')

    @classmethod
    def run(cls):
        cls._do_something()


Patch19970101Demo.run()