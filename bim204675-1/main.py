from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('ehr_db.sqlite')  # SQLite file should be created
    conn.row_factory = sqlite3.Row           # Enables dictionary-like access to rows
    return conn

# Create tables (run this only once or add a check to ensure tables are not recreated)
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Creating the Patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            address TEXT
        )
    ''')
    print("Patients table created successfully or already exists.")

    # Creating the Doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            specialty TEXT
        )
    ''')
    print("Doctors table created successfully or already exists.")

    # Creating the Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            appointment_date TEXT,
            description TEXT,
            FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
        )
    ''')
    print("Appointments table created successfully or already exists.")

    conn.commit()
    conn.close()

# Home Route
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the Patients table exists before querying
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Patients'")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Error: Patients table does not exist!")
        return "Error: Patients table does not exist!"  # Return an error message instead of failing silently

    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('index.html', patients=patients)

# View Doctors
@app.route('/doctors')
def doctors():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctors")
    doctors = cursor.fetchall()
    conn.close()
    return render_template('doctors.html', doctors=doctors)

# View Appointments
@app.route('/appointments')
def appointments():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT A.appointment_id, P.name AS patient_name, D.name AS doctor_name,
                      A.appointment_date, A.description
                      FROM Appointments A
                      JOIN Patients P ON A.patient_id = P.patient_id
                      JOIN Doctors D ON A.doctor_id = D.doctor_id''')
    appointments = cursor.fetchall()
    conn.close()
    return render_template('appointments.html', appointments=appointments)

# Add new patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Patients (name, age, gender, address) VALUES (?, ?, ?, ?)",
                       (name, age, gender, address))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_patient.html')

# Add new appointment
@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        description = request.form['description']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Appointments (patient_id, doctor_id, appointment_date, description)
                          VALUES (?, ?, ?, ?)''', (patient_id, doctor_id, appointment_date, description))
        conn.commit()
        conn.close()
        return redirect(url_for('appointments'))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()
    cursor.execute("SELECT * FROM Doctors")
    doctors = cursor.fetchall()
    conn.close()
    return render_template('add_appointment.html', patients=patients, doctors=doctors)

if __name__ == '__main__':
    print("Starting application...")
    create_tables()  # Create tables when the app starts
    app.run(host='0.0.0.0', port=8080)

