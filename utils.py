from flask import session

def update_session(cursor, key, query):
    cursor.execute(query)
    session[key] = cursor.fetchone()

    # try:
    #     if session[key]["ID"] != value:
    #         cursor.execute(f'SELECT * FROM {key}s WHERE ID = {value}')
    #         session[key] = cursor.fetchone()
    # except(KeyError): 
    #     cursor.execute(f'SELECT * FROM {key}s WHERE ID = {value}')
    #     session[key] = cursor.fetchone()
