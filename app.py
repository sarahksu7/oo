from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_mail import Mail, Message

app = Flask(__name__)



# Your secret key and database connection information should be kept secure
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pddata'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        # Get form data
        user_id = request.form['id']
        password = request.form['password']

        # Initialize cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check admin table
        cursor.execute('SELECT * FROM admin WHERE id = %s AND password = %s', (user_id, password))
        admin = cursor.fetchone()
        if admin:
            session['loggedin'] = True
            session['id'] = admin['id']
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))

        # Check doctor table
        cursor.execute('SELECT * FROM doctor WHERE id = %s AND password = %s', (user_id, password))
        doctor = cursor.fetchone()
        if doctor:
            session['loggedin'] = True
            session['id'] = doctor['id']
            session['role'] = 'doctor'
            return redirect(url_for('doctor_dashboard'))

        # Check patient table
        cursor.execute('SELECT * FROM patient WHERE id = %s AND password = %s', (user_id, password))
        patient = cursor.fetchone()
        if patient:
            session['loggedin'] = True
            session['id'] = patient['id']
            session['role'] = 'patient'
            return redirect(url_for('patient_dashboard'))

        message = 'Please enter correct ID/password!'
        # Close the cursor
        cursor.close()

    # This line will render the login template whether the method is GET or POST and there was an error
    return render_template('login.html', message=message)

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('loggedin') and session.get('role') == 'admin':
        return 'Welcome to the admin dashboard.'
    return redirect(url_for('login'))

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if session.get('loggedin') and session.get('role') == 'doctor':
        return 'Welcome to the doctor dashboard.'
    return redirect(url_for('login'))

@app.route('/patient_dashboard')
def patient_dashboard():
    if session.get('loggedin') and session.get('role') == 'patient':
        return 'Welcome to the patient dashboard.'
    return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)  # Turn off debug mode when deploying to production
