import sqlite3
from sqlite3 import Error
from datetime import datetime


def sql_connection():
    try:
        db = sqlite3.connect('mytest.sqlite')
        return db
    except Error:
        print(Error)


def create_table(con):
    """ Create the table with given columns
    """
    try:
        cur = con.cursor()
        cur.execute('''CREATE TABLE employees(
        id INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        department TEXT,
        position TEXT,
        salary REAL,
        date TEXT);''')
        con.commit()
        print('The table is created successfully')
    except Error:
        print(Error)


def insert_data(con, entities):
    """  Insert records into the table
    """
    query = """INSERT INTO employees (id, name, surname, department, position,
            salary, date) VALUES(?,?,?,?,?,?,?)"""

    try:
        cur = con.cursor()
        cur.execute(query, entities)
        con.commit()
        print("The record added successfully")
    except Error:
        print(Error)


def add_data(con):
    """ The second method to add records into the table"""
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO employees VALUES(2, 'David', 'Anderson', 'IT', 'Dev', 3000, '2020-06-01')")
        cur.execute("INSERT INTO employees VALUES(3, 'Tom', 'Roger', 'IT', 'Manager', 3000, '2018-03-02')")
        cur.execute("INSERT INTO employees VALUES(4, 'Alan', 'Meyer', 'IT', 'Dev', 5000, '2019-04-15')")
        con.commit()
        print("The records added successfully")
    except Error:
        print(Error)


def select_all(con):
    """Selects all rows from the table to display
    """
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM employees')
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Error:
        print(Error)


def update_data(con, salary, id):
    """ Update the table with given new values"""
    try:
        cur = con.cursor()
        cur.execute("UPDATE employees SET salary = ?  WHERE id = ?", (salary,
                                                                      id))
        con.commit()
        print("The record updated successfully")
    except Error:
        print(Error)


def delate_record(con, surname):
    """ Delete the given record
    """
    query = "DELETE FROM employees WHERE surname = ?;"
    try:
        cur = con.cursor()
        cur.execute(query, (surname,))
        con.commit()
        print("The record delated successfully")
    except Error:
        print(Error)


def parse_input_string(input_string):
    # Розділити вхідну стрічку за комами та видалити зайві пробіли
    data = [x.strip() for x in input_string.split(',')]
    
    if len(data) != 7:
        return None, "Некоректна кількість даних"
    
    try:
        data[0] = int(data[0])  
        data[5] = int(data[5])
        
        data[6] = datetime.strptime(data[6], "%d-%m-%Y").date()
    except ValueError:
        return None, "Некоректні дані числового або дати"
    
    return data, None




def main():
    con = sql_connection()
    create_table(con)
    entities = (1, 'Anna', 'Smith', 'IT', 'Dev', 2000, '20-02-2022')
    insert_data(con, entities)
    
    input_str = input("Введіть дані в форматі: id, first_name, last_name, department, position, salary, date (розділені комами): ")
    parsed_data, error = parse_input_string(input_str)
    
    if parsed_data:
        insert_data(con, parsed_data)
        print("Дані успішно додано до бази даних.")
    else:
        print("Помилка:", error)

    add_data(con)
    select_all(con)
    update_data(con, 3000, 1)
    delate_record(con, "Roger")
    
    con.close()

if __name__ == "__main__":
    main()



