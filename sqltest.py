import sqlite3


def checkUser(username):
    records = []
    try:
        sqliteConnection = sqlite3.connect('trending.db')
        cursor = sqliteConnection.cursor()
        sql_select_query = """select * from users where username = ?"""
        cursor.execute(sql_select_query, (username,))
        rows = cursor.fetchall()
        for row in rows:
            dictentry = {'userID': row[0], 'username': row[1], 'hash': row[2]}
            records.append(dictentry)

        for record in records:
            print(record)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into user table", error)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("closed")
        return records


records = checkUser('George')
