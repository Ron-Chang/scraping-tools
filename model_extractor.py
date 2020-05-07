import inspect
from flask_sqlalchemy import DefaultMeta


class ModelExtractor:
    """
    Convert table rows as a dict and collect into a list.
    將表單物件取出製作成字典,並搜集成列表.
    return [
        {
            'column_1': value_1,
            'column_2': value_2,
            ...
            'column_N': value_N,
        },
        {
            'column_1': value_1,
            'column_2': value_2,
            ...
            'column_N': value_N,
        },
        ...
        {
            'column_1': value_1,
            'column_2': value_2,
            ...
            'column_N': value_N,
        }
    ]
    """

    def __init__(self, table, slice_num=2000, split_by=0):

        self.table = table
        self.slice_num = slice_num
        self.split_by = split_by

        self.objects = None
        self.columns = list()
        self.data = list()

        self._run()

        self.quantity = len(self.objects)

    @staticmethod
    def get_tables(models):
        """
        = = = = = = = = = = = = = = = = = =
        =  =  =  =  =  未使用  =  =  =  =  =
        = = = = = = = = = = = = = = = = = =

        Parse all import object and get "flask_sqlalchemy.model.DefaultMeta" instance.
        過濾所有匯入物件,取得 flask_sqlalchemy 預設型別"物件名稱"與"實例化物件",回傳字典.
        return {
            ModelName1: <class 'ModelName1'>,
            ModelName2: <class 'ModelName2'>,
            ...
            ModelNameN: <class 'ModelNameN'>,
        }
        """
        return {_.__name__: _ for name, _ in inspect.getmembers(models) if isinstance(_, DefaultMeta)}

    def _get_columns(self):
        """
        Parse keys of the table and get all column's names.
        取得全部"表單物件"鍵值,排除非"欄位名稱",回傳列表.
        return ['column_1', 'column_2', ..., 'column_N']
        """
        results = list()
        for key, value in self.table.__dict__.items():
            if key.startswith('_'):
                continue
            comparator = value.__dict__.get('comparator')
            if comparator is None:
                continue
            data_type = comparator.__dict__.get('type')
            if data_type is None:
                continue
            python_data_type = getattr(data_type, 'python_type')
            if python_data_type:
                results.append(key)
        return results

    def _slice_query(self):
        """
        Slice query for entire table,
        It will just return the same result as query.all() but safely for memory cache.
        回傳值等同 query.all(), 但能確保在低記憶體主機上安全執行.
        """
        count = 0
        results = list()
        while True:
            start = self.slice_num * count
            end = self.slice_num * (count + 1)
            slice_cache = self.table.query.slice(start, end).all()
            if slice_cache:
                results.extend(slice_cache)
            if len(slice_cache) < self.slice_num:
                break
            count += 1
        return results

    def _split_objects(self):
        """
        |                                                 |
        | | [obj] [obj] | | [obj] [obj] | | [obj] [obj] | |
        | |___bucket____| |___bucket____| |___bucket____| |
        |_____________________container___________________|
        """
        container = list()
        bucket = list()
        for index, obj in enumerate(self.objects, start=1):
            result = {column: getattr(obj, column) for column in self.columns}
            bucket.append(result)
            if index % self.split_by == 0 and bucket:
                container.append(bucket)
                bucket = list()
        if bucket:
            container.append(bucket)
        return container

    def _get_data(self):
        if split_by > 1:
            self._split_objects()
        return [{column: getattr(obj, column) for column in self.columns} for obj in self.objects]

    @classmethod
    def _run(self):
        self.columns = self._get_columns()
        self.objects = self._slice_query()
        self.data = self._get_data()
