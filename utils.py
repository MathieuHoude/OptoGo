from flask import session

def update_session(cursor, key, query):
    cursor.execute(query)
    session[key] = cursor.fetchone()