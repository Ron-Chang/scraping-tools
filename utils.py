from functools import wraps
from datetime import timedelta

class DecoratorUtils:
    def snap_interval(**kwargs):
        def decorator(method):
            seconds = timedelta(**kwargs).total_seconds()
            if isinstance(seconds, float) or isinstance(seconds, int):
                snap_interval = seconds
            else:
                snap_interval = 60 * 60 * 24 * 7
            @wraps(method)
            def wrapper(*args, **kwargs):
                return method(*args, **kwargs, snap_interval=snap_interval)
            return wrapper
        return decorator


class Utils:

    @staticmethod
    def underscore_to_camel(letters, delimiter='_'):
        """
        Allow one or more letters convert into camel style.
        單、複數詞組由底線轉換駝峰
        'my_model_name' -> 'My_Model_Name' -> 'MyModelName'
        """
        if delimiter not in letters:
            return letters.title()
        return letters.title().replace(delimiter, '')

    @staticmethod
    def camel_to_underscore(letters, delimiter='_'):
        """
        Allow one or more letters convert into underscore style.
        單、複數詞組由駝峰轉換底線
        'MyModelName' -> '_my_model_name' -> 'my_model_name'
        """
        if letters.islower():
            return letters
        result = ''.join([f'{delimiter}{_.lower()}' if _.isupper() else _ for _ in letters])
        return result.lstrip(delimiter)
