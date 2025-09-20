import time
import sqlite3 
import functools

def with_db_connection(func):
    """ your code goes here""" 
    #wrapper
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn,*args,**kwargs)
        finally:
            conn.close()
    return wrapper


query_cache = {}

def cache_query(func):
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        if query is None:
            query = args[0]
        if query in query_cache:
            return query_cache[query]
        else:
            query_cache[query] = func(*args, **kwargs)
        return query_cache[query]
    return wrapper
   

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")