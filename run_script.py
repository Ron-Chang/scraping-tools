import os
import sys
from importlib import import_module
from pprint import PPrint
from super_print import SuperPrint


class Patch:
    """
    \x1b[5;36m目的 Aim To\x1b[0m

        統一由 src 作為 source directory, 避免 產生 import 問題,
        關閉 k8s probe, 同時減少 src 入口執行緒複雜。

        The main purpose is maintain all scripts by a single
        entry point to keep src folder tidy, and handler the
        import issues if the script is not start at src.
        The Program collecting scripts into the same direct-
        -ory and capable to list scripts orderly.

    \x1b[5;36m檔案格式 Format\x1b[0m

        \x1b[5;33m- PREFIX\x1b[0m for sorting.
            * init
            * patch
            * script

        \x1b[5;33m- DATE\x1b[0m add it after prefix for ordering.
            * format = '%Y%m%d'

        \x1b[5;33m- 放入 'src/script' 資料夾下, 並且以底線分隔單字.\x1b[0m

        \x1b[5;33m- 須於腳本內執行呼叫入口.\x1b[0m

        \x1b[5;33m- format\x1b[0m - f'src/script/{\x1b[5;33mPREFIX\x1b[0m}_{\x1b[5;33mDATE\x1b[0m}_{short_description}.py'
            * src/script/a_demo_19970101_simple_demonstration.py
    """

    _TAG_TEXT_GREEN = '\x1b[5;32m'
    _TAG_TEXT_WHITE = '\x1b[5;37m'
    _TAG_BG_CYAN = '\x1b[7;36m'
    _TAG_RESET = '\x1b[0m'

    SCRIPT_DIR = 'script'
    IS_CLI = True

    @classmethod
    def help(cls):
        SuperPrint(cls.__doc__)

    @classmethod
    def get_script_info(cls):
        files = os.listdir(cls.SCRIPT_DIR)
        scripts = [_.replace('.py', '') for _ in files if _.endswith('.py')]
        script_info = {str(k): v for k, v in enumerate(sorted(scripts))}
        if not script_info:
            cls.help()
            PPrint('No script!', tag='warning')
            exit()
        return script_info

    @classmethod
    def show_menu(cls):
        script_info = cls.get_script_info()
        script_menu = '\n'.join(f' - {cls._TAG_TEXT_GREEN}[{k}]{cls._TAG_RESET}: {v}' for k, v in script_info.items())
        if cls.IS_CLI:
            func_info = {
                f'{cls._TAG_TEXT_GREEN}-h,{" --help":8}{cls._TAG_RESET}': 'Documentation',
                f'{cls._TAG_TEXT_GREEN}-l,{" --list":8}{cls._TAG_RESET}': 'List scripts',
                f'{cls._TAG_TEXT_GREEN}-f,{" --force":8}{cls._TAG_RESET}': 'Execute without confirm.',
                f'{cls._TAG_TEXT_GREEN}-e,{"":8}{cls._TAG_RESET}': ('Execute scripts\n'
                                                                    '\t\t$python run_script.py -e 0\n'
                                                                    '\t\t$python run_script.py -e 0,1,2'),
            }
            func_menu = '\n'.join(f' {k}: {v}' for k, v in func_info.items())
        else:
            func_info = {
                'h': 'help',
                'q': 'exit',
            }
            func_menu = '\n'.join(f' - {cls._TAG_TEXT_GREEN}[{k}]{cls._TAG_RESET}: {v}' for k, v in func_info.items())
        SuperPrint(f'{script_menu}\n\n{func_menu}')

    @classmethod
    def _dynamic_import(cls, module_path, class_name=None):
        module = import_module(module_path)
        if not class_name:
            return None
        return getattr(module, class_name)

    @classmethod
    def launch(cls, option):
        script_info = cls.get_script_info()
        script = script_info.get(option)
        cls._dynamic_import(module_path=f'{cls.SCRIPT_DIR}.{script}')

    @classmethod
    def confirm(cls, option):
        script_info = cls.get_script_info()
        script = script_info.get(option)
        print(f'Launch script < {cls._TAG_TEXT_WHITE}{script}{cls._TAG_RESET} >, moving on? (y/n)')
        result = True if input('>>> ').lower() in ['y', 'yes'] else False
        if not result:
            PPrint(f'Script < {script} > has been skipped.', tag='warning')
        return result

    @classmethod
    def run(cls):
        cls.IS_CLI = False
        print(f'\n{cls._TAG_BG_CYAN} Script Operator {cls._TAG_RESET}')
        while True:
            cls.show_menu()
            option = input('>>> ')
            if option.lower() in ['quit', 'exit', 'q']:
                PPrint('Program has been terminated!', 'info')
                exit()
            if option.lower() in ['help', 'h']:
                cls.help()
                continue
            if option in cls.get_script_info():
                if cls.confirm(option=option):
                    cls.launch(option=option)
                    break
                continue
            PPrint(f'Invalid Input! < {option} >', tag='error')
        exit()


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        Patch.run()
    if '-h' in args or '--help' in args:
        Patch.help()
        exit()
    if '-l' in args or '-ls' in args or '--list' in args:
        Patch.show_menu()
        exit()
    if '-e' in args:
        force_mode = True if '-f' in args or '--force' in args else False
        param = args[args.index('-e') + 1]
        user_inputs = set(param.split(','))
        for user_input in user_inputs:
            if not user_input.isdigit() or user_input not in Patch.get_script_info():
                PPrint(f'Invalid Input! < {user_input} >', tag='error')
                continue
            if force_mode:
                Patch.launch(user_input)
                continue
            if Patch.confirm(user_input):
                Patch.launch(user_input)
        exit()
    PPrint(f'Invalid Input! < {args[1:]} >', tag='error')
