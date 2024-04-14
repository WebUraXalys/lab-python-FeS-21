import sqlite3

def parse(string):
    
    
    
    
    
    
    
    string = string.strip()
    string = string.split("(")[1][:-1]
    parts = string.split(",")
    res = {'id': None, 'name': None, 'note': None}
    for part in parts:
        t = part.split("=")
        key = t[0].strip()
        value = t[1].strip()
        if key in res:
            res[key] = value
    return res

 

        
    

def table_COMPANY(cursor) -> None:

    """
    This function creates a COMPANY table in the database if it doesn't exist.
    """
    
    query = """CREATE TABLE IF NOT EXISTS COMPANY(
            ID INT PRIMARY KEY NOT NULL,
            NAME CHAR(20) NOT NULL, 
            NOTE CHAR(150) )"""
    cursor.execute(query)




def control_panel() -> str:
    
    """
    This function displays a control panel menu and returns the user's choice.
    """
   
    print("Add record - 1")
    print("Change record - 2")
    print("Remove record - 3")
    print("Show all - 4")
    print("Exit - 5")
    choice = input("Make a choise")
    return choice





def add_record(connection, cursor) -> None:
    
    """
    This function adds a new record to the COMPANY table.
    """

    data = parse(input("Enter the record data: "))

    # Перевірка існуючого ID
    cursor.execute("SELECT * FROM COMPANY WHERE ID = ?", (data["id"],))
    existing_record = cursor.fetchone()
    if existing_record:
        print("ID {} already exists.".format(data["id"]))
    else :
      cursor.execute("INSERT INTO COMPANY (ID, NAME, NOTE) VALUES (?, ?, ?)", (data["id"], data["name"], data["note"]))
      
    connection.commit()

    






def change_record(connection, cursor) -> None:
   
    """
    This function updates the note of a record in the COMPANY table based on the given ID.
    """

    id = int(input("Change ID: "))
    note = input("Enter new note: ")
    connection.execute("UPDATE COMPANY SET NOTE = ? WHERE ID = ?", (note, id))
    connection.commit()






def delete_record(connection, cursor) -> None:
    
    """
    This function deletes a record from the COMPANY table based on the given ID.
    """

    id = int(input("Change ID of COMPANY: "))
    connection.execute("DELETE FROM COMPANY WHERE ID = ?", (id,))
    connection.commit()






def show_all(cursor) -> None:
    
    """
    This function retrieves and displays all records from the COMPANY table.
    """

    cursor.execute("SELECT * FROM COMPANY")
    records = cursor.fetchall()
    for record in records:
        print(record)


connection = sqlite3.connect('d:\\Lab Python\\notebook.sqlite3')
cursor = connection.cursor()

table_COMPANY(cursor)

while True:
    choice = control_panel()
    if choice == '1':
        add_record(connection, cursor)
    elif choice == '2':
        change_record(connection, cursor)
    elif choice == '3':
        delete_record(connection, cursor)
    elif choice == '4':
        show_all(cursor)
    elif choice == '5':
        break
    else:
        print("Wrong choice")

cursor = connection.execute("SELECT * FROM COMPANY")
print(cursor.fetchall())

connection.close()