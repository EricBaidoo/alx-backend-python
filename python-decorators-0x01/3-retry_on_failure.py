import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn,*args,**kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None  # To store the last exception
            for i in range(retries):
                try:
                    return func(*args, **kwargs)  # Try to call the function
                except Exception as e:
                    last_exception = e  # Save the exception
                    time.sleep(delay)   # Wait before retrying
            raise last_exception  # If all retries fail, raise the last exception
        return wrapper
    return decorator

        


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)