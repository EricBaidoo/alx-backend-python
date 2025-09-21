import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

# Usage example for task 1
with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as cursor:
    print(cursor.fetchall())
