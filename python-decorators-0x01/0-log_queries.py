import sqlite3
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # YOUR CODE: log the query here
        # Getting queries from the  args or kwargs
        query = kwargs.get('query')
        if query is None and args:
            query = args.get[0]
        print(f"Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")