import pandas as pd


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Stats(metaclass=Singleton):
    """
    Singleton object that exists only one time in the application. The class counts basic statistics on number 
    of daily logs.
    """

    class PandasInstance:
        def __init__(self, df):
            self.__hashed_pd_objects = pd.util.hash_pandas_object(df)
            self.__hash = hash(str(self.__hashed_pd_objects))

        def __hash__(self):
            return self.__hash

        def __eq__(self, other):
            return self.__hashed_pd_objects.equals(other._PandasInstance__hashed_pd_objects) if type(self) == type(
                other) else False

    def __init__(self):
        self.__call_count = 0
        self.__total_rows_processed = 0
        self.__processed = set()
        self.__average_rows_count = 0

    def is_already_processed(self, df):
        result = False
        if df is not None:
            key = self.PandasInstance(df)
            result = key in self.__processed
            if not result:
                self.__processed.add(key)

        return result

    def process(self, df):
        result = False
        if df is not None and not self.is_already_processed(df):
            self.__call_count += 1
            self.__total_rows_processed += len(df.index)
            self.__average_rows_count = self.__total_rows_processed / self.__call_count
            result = True

        return result

    def process_all(self, list_df):
        result = 0
        if list_df is not None and len(list_df) > 0:
            for list in list_df:
                result += 1 if self.process(list) else 0

        return result

    def __str__(self):
        return f"[Total count: {self.__call_count}, Total rows processed: {self.__total_rows_processed}, Average row count: {self.__average_rows_count}"
