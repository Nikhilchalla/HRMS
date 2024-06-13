from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for flashing messages

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'task1'

mysql = MySQL(app)

def create_database():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(app.config['MYSQL_DB']))
        cur.execute("USE {}".format(app.config['MYSQL_DB']))
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                username VARCHAR(20) PRIMARY KEY,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)
        mysql.connection.commit()
        cur.close()

# Ensure the database and table are created when the app starts
create_database()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payroll')
def payroll():
    if request.method == 'GET':

            cur = mysql.connection.cursor()

            cur.execute("SELECT id,name,days,salary_perday,days*salary_perday,mobile_number FROM attendence")
            
            user = cur.fetchall()
            cur.close()

            return render_template("payroll.html", user=user)
    return render_template('payroll.html')

@app.route('/partners')
def partners():
    return render_template('partners.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/attendance')
def attendance():
   
   if request.method == 'GET':

            cur = mysql.connection.cursor()

            cur.execute("SELECT * FROM attendence")

            user = cur.fetchall()
            cur.close()

            return render_template("attendance.html", user=user)
   return render_template("attendance.html")


@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if request.method == 'POST':
        user_id = request.form['user_id']
        today = datetime.now().date()
        # Here, you'll write logic to update the attendance record in the database
        # For simplicity, let's assume you're just marking the user as present for the current date
        cur = mysql.connection.cursor()
        cur.execute("SELECT last_updated FROM attendence WHERE id = %s", (user_id,))
        result = cur.fetchone()

        if result:
            last_updated = result[0]
            if last_updated < today:
        
        # Example SQL (ensure you have an appropriate table structure)
                query = "update attendence set days=days+1, last_updated=%s where id=%s"
                cur.execute(query, (today,user_id,))
        
                mysql.connection.commit()
                cur.close()
        
                flash('Attendance marked successfully!', 'success')
            else:
                flash('Attendance already marked', 'error')

        return redirect(url_for('attendance'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/calender')
def calender():
    return render_template('calender.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        username = userDetails['username']
        email = userDetails['email']
        password = userDetails['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Check if email already exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash('Email already exists. Please use a different email.', 'error')
            return redirect(url_for('registration'))
        else:
            cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (username, email, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Registration Successful! You can now sign in.', 'success')  # Flash success message

        return redirect(url_for('index'))

    return render_template('registration.html')

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))

        # Fetch user
        user = cur.fetchone()

        if user:
            flash('User signed in successfully!', 'success')  # Flash success message
            return redirect(url_for('main'))
        else:
            flash('Incorrect email or password. Please try again.', 'error')  # Flash error message

        # Close connection
        cur.close()

    return render_template('sign.html')

if __name__ == '__main__':
    app.run(debug=True)

