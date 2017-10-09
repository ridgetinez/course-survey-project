import csv
import sqlite3

def insert_user(conn, user_type, identifier, password):
    if user_type == "staff":
        user_type = "STAFF"
    if user_type == "student":
        user_type = "STUDENTS"
    sql = "INSERT INTO {} (ID, PASSWORD) VALUES (\'{}\', \'{}\');".format(user_type, identifier, password)
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)

with open("../static/passwords.csv", newline='') as userfile:
    reader = csv.reader(userfile)
    conn = sqlite3.connect('../users.db')
    for row in reader:
        insert_user(conn, row[2], row[0], row[1])
    conn.commit()
