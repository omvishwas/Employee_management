from flask import *
import pyodbc
from config import DB_PORT,DB_PWD,DB_USERNAME,DB_HOST,DB_NAME

app = Flask(__name__)

def get_db_connection():
   connection = pyodbc.connect(r'DRIVER={PostgreSQL Unicode(x64)};' r'SERVER='+DB_HOST+';' r'DATABASE='+DB_NAME+';' r'UID='+DB_USERNAME+';' r'PWD='+ DB_PWD+';' r'PORT='+DB_PORT)
   return connection

@app.route('/')
def index():
   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM employees")
   employees = cursor.fetchall()
   conn.close()
   return render_template('index.html', employees=employees)


@app.route('/create', methods=['GET', 'POST'])
def create_employee():
   if request.method == 'POST':
       data = request.form
       conn = get_db_connection()
       cursor = conn.cursor()
       cursor.execute("""
           INSERT INTO employees (name, skillset, department, email, phone_number, address, date_of_joining)
           VALUES (?, ?, ?, ?, ?, ?, ?)
       """, (data['name'], data['skillset'], data.get('department'), data.get('email'), data.get('phone_number'), data.get('address'), data.get('date_of_joining')))
       conn.commit()
       conn.close()
       return redirect(url_for('index'))
   return render_template('create.html')


@app.route('/edit/<int:emp_id>', methods=['GET', 'POST'])
def edit_employee(emp_id):
   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
   employee = cursor.fetchone()
   if request.method == 'POST':
       data = request.form
       cursor.execute("""
           UPDATE employees
           SET name = ?, skillset = ?, department = ?, email = ?, phone_number = ?, address = ?, date_of_joining = ?
           WHERE emp_id = ?
       """, (data['name'], data['skillset'], data.get('department'), data.get('email'), data.get('phone_number'), data.get('address'), data.get('date_of_joining'), emp_id))
       conn.commit()
       conn.close()
       return redirect(url_for('index'))
   conn.close()
   return render_template('edit.html', employee=employee)


@app.route('/delete/<int:emp_id>', methods=['POST'])
def delete_employee(emp_id):
   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
   conn.commit()
   conn.close()
   return redirect(url_for('index'))


@app.route('/summary')
def summary():
   conn = get_db_connection()
   cursor = conn.cursor()
   cursor.execute("SELECT COUNT(*) FROM employees")
   total_employees = cursor.fetchone()[0]
   cursor.execute("SELECT skillset, COUNT(*) FROM employees GROUP BY skillset")
   skillset_summary = cursor.fetchall()
   conn.close()
   return render_template('summary.html', total_employees=total_employees, skillset_summary=skillset_summary)


if __name__ == '__main__':
    app.run (debug=True, host='localhost')