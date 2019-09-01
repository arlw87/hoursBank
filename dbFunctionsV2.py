# functions for writing to the database
import sqlite3

# path of the database
dbPath = "hoursBank.db"

# connect to the database and if the table doesnt exist create it
def connect():
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Bank4 (ID text PRIMARY KEY, NAME text, RATE REAL, HOL_RATE REAL, BANKED_HOURS REAL, BANKED_SALARY REAL)")
    conn.commit()
    conn.close()

# take in all the parameters passed and create an employee record in the database
def addUser(ID, name, rate, hol_rate, banked_hours, banked_salary):
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.execute("INSERT INTO Bank4 VALUES(?,?,?,?,?,?)", (ID, name, rate, hol_rate, banked_hours, banked_salary))
    conn.commit()
    conn.close()

# Update the hours of the employee in the database
def addHours(ID, banked_hours, banked_salary):
    print("Quick Test Add Hours")
    print(ID)
    print(banked_hours)
    print(banked_salary)
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.execute("UPDATE Bank4 SET BANKED_HOURS = ?, BANKED_SALARY = ? WHERE ID = ?", (banked_hours, banked_salary, ID))
    conn.commit()
    conn.close()

# edit the hours of the employee in the database
def editEmployee(ID, rate, hol_rate):
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.execute("UPDATE Bank4 SET RATE = ?, HOL_RATE = ? WHERE ID = ?", (rate, hol_rate, ID))
    conn.commit()
    conn.close()

# delete the identified user form the database
def deleteUser(ID):
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    print("INSIDE DB FUNCTION:","001")
    print("DELETE FROM Bank4 WHERE ID = ?", (ID,))
    cur.execute("DELETE FROM Bank4 WHERE ID = ?", (ID,))
    # (ID,) to show its one value to be inserted
    conn.commit()
    conn.close()

# get all the employees data from the database
def getAllUsers():
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Bank4")
    rows = cur.fetchall()
    conn.close()
    return rows
