from flask import session

def update_session(cursor, key, query):
    if key not in session:
        cursor.execute(query)
        session[key] = cursor.fetchone()