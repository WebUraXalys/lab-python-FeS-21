import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        db = sqlite3.connect('myDB.sqlite')
        return db
    except Error:
        print(Error)


def create_table(con):
    try:
        cur = con.cursor()
        cur.execute('''CREATE TABLE student(
        id INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        position TEXT,
        date TEXT);''')
        con.commit()
        print('The table is created successfully')
    except Error:
        print(Error)


def insert_data(con, entities):
    query = """INSERT INTO student (id, name, surname, position,
            date) VALUES(?,?,?,?,?)"""

    try:
        cur = con.cursor()
        cur.execute(query, entities)
        con.commit()
        print("The record added successfully")
    except Error:
        print(Error)


def add_data(con):
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO student VALUES(2, 'David', 'Anderson', 'Dev', '2020-06-01')")
        cur.execute("INSERT INTO student VALUES(3, 'Tom', 'Roger', 'Frontend', '2018-03-02')")
        cur.execute("INSERT INTO student VALUES(4, 'Alan', 'Meyer', 'DevOps', '2019-04-15')")
        con.commit()
        print("The records added successfully")
    except Error:
        print(Error)


def select_all(con):
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM student')
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Error:
        print(Error)


def update_data(con, position, id):
    try:
        cur = con.cursor()
        cur.execute("UPDATE student SET position = ?  WHERE id = ?", (position,
                                                                      id))
        con.commit()
        print("The record updated successfully")
    except Error:
        print(Error)


def delate_record(con, surname):
    query = "DELETE FROM student WHERE surname = ?;"
    try:
        cur = con.cursor()
        cur.execute(query, (surname,))
        con.commit()
        print("The record delated successfully")
    except Error:
        print(Error)


def main():
    con = sql_connection()
    create_table(con)
    entities = (1, 'Yura', 'Khalus', 'Dev', '2020-02-09')
    insert_data(con, entities)
    add_data(con)
    select_all(con)
    update_data(con, 'C++', 1)
    delate_record(con, "Roger")
    con.close()


if __name__ == "__main__":
    main()