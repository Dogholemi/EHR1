import sqlite3

def connect_db():
    conn = sqlite3.connect('ehr_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def insert_test_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Insert test patient
    cursor.execute("INSERT INTO Patients (name, age, gender, address) VALUES (?, ?, ?, ?)", 
                   ('John Doe', 30, 'Male', '123 Main St'))

    # Insert test doctor
    cursor.execute("INSERT INTO Doctors (name, specialty) VALUES (?, ?)", 
                   ('Dr. Smith', 'Cardiology'))

    conn.commit()
    conn.close()

insert_test_data()
print("Test data inserted successfully.")
