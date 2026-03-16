from flask import Flask ,render_template,request,redirect,session 
import mysql.connector 
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import flash
app = Flask(__name__)
app.secret_key = "abc"
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root",
    database="company"
)

serializer = URLSafeTimedSerializer(app.secret_key)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vaishnavisunkara126@gmail.com'
app.config['MAIL_PASSWORD'] = 'mton ahrh ffqr etzr'

mail = Mail(app)
cursor = mydb.cursor()

@app.route('/')
def register_page():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash("Your message has been sent! We'll get back to you soon.", "success")
        return redirect('/contact')
    return render_template("contact.html")


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    email = request.form['email']
    uname = request.form['username']
    pwd = request.form['password']
    cpwd = request.form['cpassword']
    role = request.form.get('role')


    if pwd != cpwd:
            flash("Passwords do not match","danger")
            return redirect('/register')
        

    query = "insert into users(email,username,password,role) values (%s,%s,%s,%s)"
    cursor.execute(query,(email,uname,pwd,role))
    mydb.commit()
    flash("Registartion Successful","success")
    return redirect('/login')


@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/login_user', methods=['POST'])
def login():

    uname = request.form['username']
    pwd = request.form['password']

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query,(uname,pwd))
    user = cursor.fetchone()

    if user:

        session['username'] = user[2]
        session['role'] = user[4]

        return redirect('/dashboard')

    else:
        return "Invalid login"

@app.route('/forgot_password', methods=['GET','POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form['email']

        query = "SELECT * FROM users WHERE email=%s"
        cursor.execute(query,(email,))
        user = cursor.fetchone()

        if user:

            token = serializer.dumps(email, salt='reset-password')

            reset_link = f"http://127.0.0.1:5000/reset_password/{token}"

            msg = Message(
                "Password Reset Request",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )

            msg.body = f"Click this link to reset your password:\n{reset_link}"

            mail.send(msg)

            return "Reset link sent to your email"

        else:
            return "Email not found"

    return render_template("forgot_password.html")
@app.route('/dashboard')
def dashboard():

    role = session.get('role')

    if role == "admin":
        return render_template("dashboard.html")
    else:
        return redirect('/emp_dashboard')

# ---------------- DASHBOARD ----------------
@app.route('/emp_dashboard')
def emp_dashboard():

    uname = session['username']

    query = "SELECT * FROM employee WHERE username=%s"
    cursor.execute(query,(uname,))
    emp = cursor.fetchone()

    return render_template("emp_dashboard.html", emp=emp)

@app.route('/add_employee')
def add_employee():

    if session.get('role') != "admin":
        return "Access Denied"

    return render_template("add_employee.html")

@app.route('/save_employee', methods=['POST'])
def save_employee():

    if session.get('role') != "admin":
        return "Access Denied"

    name = request.form['ename']
    dept = request.form['edept']
    salary = request.form['esalary']
    phone = request.form['ephone']
    uname = request.form['username']

    query = "INSERT INTO employee(ename,edept,esalary,ephone,username) VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query,(name,dept,salary,phone,uname))
    mydb.commit()

    return redirect('/view_employee')


@app.route('/view_employee')
def view_employee():

    if session.get('role') != "admin":
        return "Access Denied"

    query = "SELECT * FROM employee"
    cursor.execute(query)
    employees = cursor.fetchall()

    return render_template("view_employee.html", employees=employees)

# ---------------- DELETE EMPLOYEE ----------------
@app.route('/delete/<id>')
def delete_employee(id):

    if session.get('role') != "admin":
        return "Access Denied"

    query = "DELETE FROM employee WHERE eid=%s"
    cursor.execute(query,(id,))
    mydb.commit()

    return redirect('/view_employee')


# ---------------- EDIT EMPLOYEE ----------------
@app.route('/edit/<id>')
def edit_employee(id):

    if session.get('role') != "admin":
        return "Access Denied"

    query = "SELECT * FROM employee WHERE eid=%s"
    cursor.execute(query,(id,))
    emp = cursor.fetchone()

    return render_template("edit_employee.html", emp=emp)

@app.route('/update_employee', methods=['POST'])
def update_employee():

    eid = request.form['eid']
    name = request.form['ename']
    dept = request.form['edept']
    salary = request.form['esalary']
    phone = request.form['ephone']

    query = """UPDATE employee 
               SET ename=%s, edept=%s, esalary=%s, ephone=%s
               WHERE eid=%s"""

    cursor.execute(query,(name,dept,salary,phone,eid))
    mydb.commit()

    return redirect('/view_employee')

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):

    try:
        email = serializer.loads(token, salt='reset-password', max_age=600)

    except:
        return "Invalid or Expired Link"

    if request.method == 'POST':

        pwd = request.form['password']
        cpwd = request.form['cpassword']

        if pwd != cpwd:
            return "Passwords do not match"

        query = "UPDATE users SET password=%s WHERE email=%s"
        cursor.execute(query,(pwd,email))
        mydb.commit()

        return redirect('/login')

    return render_template("reset_password.html")

@app.route('/logout')
def logout():

    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True, port=5000)