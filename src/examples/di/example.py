import sqllite3

class MyClass:
    
    def __init__(self, path)
        self.__conn = sqllite3.connect(path)
        
    def store_data(self, data):
        cursor = self.__conn.cursor()
        cursor.execute("INSERT INTO contractors VALUES (?, ?)", (3, "Helena"))
        
        

class MyBetterClass:
    
    def __init__(self, conn)
        self.__conn = conn
        
    def store_data(self, data):
        cursor = self.__conn.cursor()
        cursor.execute("INSERT INTO contractors VALUES (?, ?)", (3, "Helena"))