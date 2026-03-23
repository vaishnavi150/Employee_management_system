# import csv, io
# from flask import Flask, render_template, request, redirect, session, flash, Response
# import sqlite3
# # import mysql.connector
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer

# app = Flask(__name__)
# app.secret_key = "ems_secret_2026"

# # ── DATABASE ──────────────────────────────────────────────────────────────────
# # mydb = mysql.connector.connect(
# #     host="localhost",
# #     user="root",
# #     password="Root",
# #     database="company"
# # )

# def get_db_connection():
#     conn = sqlite3.connect("company.db")
#     conn.row_factory = sqlite3.Row
#     return conn
# # cursor = mydb.cursor()
# conn = get_db_connection()
# cursor=conn.cursor()

# # ── MAIL ──────────────────────────────────────────────────────────────────────
# app.config['MAIL_SERVER']   = 'smtp.gmail.com'
# app.config['MAIL_PORT']     = 587
# app.config['MAIL_USE_TLS']  = True
# app.config['MAIL_USERNAME'] = 'vaishnavisunkara126@gmail.com'
# app.config['MAIL_PASSWORD'] = 'mton ahrh ffqr etzr'
# mail       = Mail(app)
# serializer = URLSafeTimedSerializer(app.secret_key)


# # ── HELPER: redirect logged-in users away from auth pages ────────────────────
# def logged_in():
#     return session.get('username') is not None


# # ══════════════════════════════════════════════════════════════════════════════
# # PUBLIC PAGES
# # ══════════════════════════════════════════════════════════════════════════════

# @app.route('/')
# def index():
#     if logged_in():
#         return redirect('/dashboard')
#     return render_template('index.html')


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         name    = request.form['name'].strip()
#         email   = request.form['email'].strip()
#         message = request.form['message'].strip()
#         try:
#             msg = Message(
#                 subject=f"EMS Contact Form — Message from {name}",
#                 sender=app.config['MAIL_USERNAME'],
#                 recipients=[app.config['MAIL_USERNAME']]
#             )
#             msg.body = (
#                 f"You have a new message from the EMS Contact Form.\n\n"
#                 f"Name    : {name}\n"
#                 f"Email   : {email}\n"
#                 f"Message :\n{message}\n\n"
#                 f"— EMS Contact Form"
#             )
#             # Confirmation email to the sender
#             confirm = Message(
#                 subject="EMS — We received your message!",
#                 sender=app.config['MAIL_USERNAME'],
#                 recipients=[email]
#             )
#             confirm.body = (
#                 f"Hi {name},\n\n"
#                 f"Thank you for reaching out! We have received your message and will get back to you shortly.\n\n"
#                 f"Your message:\n\"{message}\"\n\n"
#                 f"— EMS Team"
#             )
#             mail.send(msg)
#             mail.send(confirm)
#             flash("Your message has been sent! A confirmation email has been sent to you.", "success")
#         except Exception as e:
#             flash(f"Failed to send message. Please try again later.", "danger")
#         return redirect('/contact')
#     return render_template('contact.html')


# # ══════════════════════════════════════════════════════════════════════════════
# # AUTHENTICATION
# # ══════════════════════════════════════════════════════════════════════════════

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if logged_in():
#         return redirect('/dashboard')
#     if request.method == 'POST':
#         email  = request.form['email'].strip()
#         uname  = request.form['username'].strip()
#         pwd    = request.form['password']
#         cpwd   = request.form['cpassword']
#         role   = request.form.get('role', 'emp')
#         if pwd != cpwd:
#             flash("Passwords do not match. Please try again.", "danger")
#             return redirect('/register')
#         # Check if username already exists
#         cursor.execute("SELECT id FROM users WHERE username=%s", (uname,))
#         if cursor.fetchone():
#             flash("Username already taken. Please choose another.", "warning")
#             return redirect('/register')
#         cursor.execute(
#             "INSERT INTO users(email, username, password, role) VALUES(%s,%s,%s,%s)",
#             (email, uname, pwd, role)
#         )
#         mydb.commit()
#         flash("Registration successful! Please log in.", "success")
#         return redirect('/login')
#     return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if logged_in():
#         return redirect('/dashboard')
#     if request.method == 'POST':
#         uname = request.form['username'].strip()
#         pwd   = request.form['password']
#         cursor.execute(
#             "SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd)
#         )
#         user = cursor.fetchone()
#         if user:
#             session['username'] = user[2]
#             session['role']     = user[4]
#             flash(f"Welcome back, {user[2]}!", "success")
#             return redirect('/dashboard')
#         flash("Invalid username or password. Please try again.", "danger")
#         return redirect('/login')
#     return render_template('login.html')


# @app.route('/logout')
# def logout():
#     name = session.get('username', '')
#     session.clear()
#     flash(f"You have been logged out successfully, {name}.", "info")
#     return redirect('/login')


# # ══════════════════════════════════════════════════════════════════════════════
# # DASHBOARD
# # ══════════════════════════════════════════════════════════════════════════════

# @app.route('/dashboard')
# def dashboard():
#     if not logged_in():
#         flash("Please log in to continue.", "warning")
#         return redirect('/login')
#     if session.get('role') == 'admin':
#         cursor.execute("SELECT COUNT(*) FROM employee")
#         total_emp = cursor.fetchone()[0]
#         cursor.execute("SELECT COUNT(DISTINCT edept) FROM employee")
#         total_dept = cursor.fetchone()[0]
#         cursor.execute("SELECT COUNT(*) FROM users")
#         total_users = cursor.fetchone()[0]
#         cursor.execute("SELECT * FROM employee ORDER BY eid DESC LIMIT 5")
#         recent = cursor.fetchall()
#         return render_template('dashboard.html',
#                                total_emp=total_emp,
#                                total_dept=total_dept,
#                                total_users=total_users,
#                                recent=recent)
#     return redirect('/emp_dashboard')


# @app.route('/emp_dashboard')
# def emp_dashboard():
#     if not logged_in():
#         flash("Please log in to continue.", "warning")
#         return redirect('/login')
#     uname = session['username']
#     cursor.execute("SELECT * FROM employee WHERE username=%s", (uname,))
#     emp = cursor.fetchone()
#     return render_template('emp_dashboard.html', emp=emp)


# # ══════════════════════════════════════════════════════════════════════════════
# # EMPLOYEE MANAGEMENT (Admin only)
# # ══════════════════════════════════════════════════════════════════════════════

# def admin_required():
#     if not logged_in():
#         flash("Please log in to continue.", "warning")
#         return redirect('/login')
#     if session.get('role') != 'admin':
#         flash("Access denied. Admins only.", "danger")
#         return redirect('/dashboard')
#     return None


# @app.route('/add_employee', methods=['GET', 'POST'])
# def add_employee():
#     block = admin_required()
#     if block: return block
#     if request.method == 'POST':
#         name   = request.form['ename'].strip()
#         dept   = request.form['edept'].strip()
#         salary = request.form['esalary']
#         phone  = request.form['ephone'].strip()
#         uname  = request.form['username'].strip()
#         cursor.execute(
#             "INSERT INTO employee(ename, edept, esalary, ephone, username) VALUES(%s,%s,%s,%s,%s)",
#             (name, dept, salary, phone, uname)
#         )
#         mydb.commit()
#         flash(f"Employee '{name}' added successfully!", "success")
#         return redirect('/view_employee')
#     return render_template('add_employee.html')


# @app.route('/view_employee')
# def view_employee():
#     block = admin_required()
#     if block: return block
#     cursor.execute("SELECT * FROM employee ORDER BY eid DESC")
#     employees = cursor.fetchall()
#     return render_template('view_employee.html', employees=employees)


# @app.route('/edit/<int:eid>', methods=['GET', 'POST'])
# def edit_employee(eid):
#     block = admin_required()
#     if block: return block
#     if request.method == 'POST':
#         name   = request.form['ename'].strip()
#         dept   = request.form['edept'].strip()
#         salary = request.form['esalary']
#         phone  = request.form['ephone'].strip()
#         cursor.execute(
#             "UPDATE employee SET ename=%s, edept=%s, esalary=%s, ephone=%s WHERE eid=%s",
#             (name, dept, salary, phone, eid)
#         )
#         mydb.commit()
#         flash(f"Employee '{name}' updated successfully!", "success")
#         return redirect('/view_employee')
#     cursor.execute("SELECT * FROM employee WHERE eid=%s", (eid,))
#     emp = cursor.fetchone()
#     if not emp:
#         flash("Employee not found.", "danger")
#         return redirect('/view_employee')
#     return render_template('edit_employee.html', emp=emp)


# @app.route('/delete/<int:eid>')
# def delete_employee(eid):
#     block = admin_required()
#     if block: return block
#     cursor.execute("SELECT ename FROM employee WHERE eid=%s", (eid,))
#     emp = cursor.fetchone()
#     if emp:
#         cursor.execute("DELETE FROM employee WHERE eid=%s", (eid,))
#         mydb.commit()
#         flash(f"Employee '{emp[0]}' deleted successfully.", "success")
#     else:
#         flash("Employee not found.", "danger")
#     return redirect('/view_employee')


# @app.route('/search')
# def search():
#     block = admin_required()
#     if block: return block
#     q = request.args.get('q', '').strip()
#     if not q:
#         flash("Please enter a search term.", "warning")
#         return redirect('/view_employee')
#     term = f"%{q}%"
#     cursor.execute(
#         "SELECT * FROM employee WHERE ename LIKE %s OR edept LIKE %s OR ephone LIKE %s OR username LIKE %s",
#         (term, term, term, term)
#     )
#     results = cursor.fetchall()
#     return render_template('search_results.html', results=results, q=q)


# # ══════════════════════════════════════════════════════════════════════════════
# # PASSWORD RESET
# # ══════════════════════════════════════════════════════════════════════════════

# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form['email'].strip()
#         cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
#         user = cursor.fetchone()
#         if user:
#             token      = serializer.dumps(email, salt='reset-password')
#             reset_link = f"http://127.0.0.1:5000/reset_password/{token}"
#             msg        = Message(
#                 "EMS — Password Reset Request",
#                 sender=app.config['MAIL_USERNAME'],
#                 recipients=[email]
#             )
#             msg.body = (
#                 f"Hello {user[2]},\n\n"
#                 f"You requested a password reset for your EMS account.\n\n"
#                 f"Click the link below to reset your password (valid for 10 minutes):\n{reset_link}\n\n"
#                 f"If you did not request this, please ignore this email.\n\n"
#                 f"— EMS Team"
#             )
#             mail.send(msg)
#             flash("Password reset link sent to your email!", "success")
#             return redirect('/forgot_password')
#         flash("No account found with that email address.", "danger")
#         return redirect('/forgot_password')
#     return render_template('forgot_password.html')


# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     try:
#         email = serializer.loads(token, salt='reset-password', max_age=600)
#     except Exception:
#         flash("This reset link is invalid or has expired. Please request a new one.", "danger")
#         return redirect('/forgot_password')
#     if request.method == 'POST':
#         pwd  = request.form['password']
#         cpwd = request.form['cpassword']
#         if pwd != cpwd:
#             flash("Passwords do not match.", "danger")
#             return redirect(request.url)
#         cursor.execute("UPDATE users SET password=%s WHERE email=%s", (pwd, email))
#         mydb.commit()
#         flash("Password reset successful! Please log in with your new password.", "success")
#         return redirect('/login')
#     return render_template('reset_password.html', token=token)



# # ══════════════════════════════════════════════════════════════════════════════
# # FEATURE 1 — EXPORT EMPLOYEES TO CSV
# # ══════════════════════════════════════════════════════════════════════════════
# import csv, io
# from flask import Response

# @app.route('/export_csv')
# def export_csv():
#     block = admin_required()
#     if block: return block
#     cursor.execute("SELECT eid, ename, edept, esalary, ephone, username FROM employee ORDER BY eid")
#     rows = cursor.fetchall()
#     output = io.StringIO()
#     writer = csv.writer(output)
#     writer.writerow(['ID','Name','Department','Salary','Phone','Username'])
#     writer.writerows(rows)
#     return Response(
#         output.getvalue(),
#         mimetype='text/csv',
#         headers={'Content-Disposition': 'attachment; filename=employees.csv'}
#     )

# # ══════════════════════════════════════════════════════════════════════════════
# # FEATURE 2 — CHANGE PASSWORD (logged-in users)
# # ══════════════════════════════════════════════════════════════════════════════

# @app.route('/change_password', methods=['GET', 'POST'])
# def change_password():
#     if not logged_in():
#         flash("Please log in to continue.", "warning")
#         return redirect('/login')
#     if request.method == 'POST':
#         current = request.form['current_password']
#         new_pwd = request.form['new_password']
#         confirm = request.form['confirm_password']
#         uname   = session['username']
#         cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, current))
#         if not cursor.fetchone():
#             flash("Current password is incorrect.", "danger")
#             return redirect('/change_password')
#         if new_pwd != confirm:
#             flash("New passwords do not match.", "danger")
#             return redirect('/change_password')
#         if len(new_pwd) < 6:
#             flash("Password must be at least 6 characters.", "warning")
#             return redirect('/change_password')
#         cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_pwd, uname))
#         mydb.commit()
#         flash("Password changed successfully!", "success")
#         return redirect('/dashboard' if session.get('role') == 'admin' else '/emp_dashboard')
#     return render_template('change_password.html')

# # ══════════════════════════════════════════════════════════════════════════════
# # FEATURE 3 — SALARY SLIP (printable, per employee)
# # ══════════════════════════════════════════════════════════════════════════════

# @app.route('/salary_slip/<int:eid>')
# def salary_slip(eid):
#     block = admin_required()
#     if block: return block
#     cursor.execute("SELECT * FROM employee WHERE eid=%s", (eid,))
#     emp = cursor.fetchone()
#     if not emp:
#         flash("Employee not found.", "danger")
#         return redirect('/view_employee')
#     from datetime import date
#     month = date.today().strftime("%B %Y")
#     return render_template('salary_slip.html', emp=emp, month=month)

# # ══════════════════════════════════════════════════════════════════════════════
# # FEATURE 4 — MANAGE USERS (admin views all registered accounts)
# # ══════════════════════════════════════════════════════════════════════════════

# @app.route('/manage_users')
# def manage_users():
#     block = admin_required()
#     if block: return block
#     cursor.execute("SELECT id, email, username, role FROM users ORDER BY id DESC")
#     users = cursor.fetchall()
#     return render_template('manage_users.html', users=users)

# @app.route('/delete_user/<int:uid>')
# def delete_user(uid):
#     block = admin_required()
#     if block: return block
#     cursor.execute("SELECT username FROM users WHERE id=%s", (uid,))
#     u = cursor.fetchone()
#     if u and u[0] == session.get('username'):
#         flash("You cannot delete your own account.", "warning")
#         return redirect('/manage_users')
#     if u:
#         cursor.execute("DELETE FROM users WHERE id=%s", (uid,))
#         mydb.commit()
#         flash(f"User '{u[0]}' deleted.", "success")
#     return redirect('/manage_users')




# # ══════════════════════════════════════════════════════════════════════════════
# # ADMIN PROFILE
# # ══════════════════════════════════════════════════════════════════════════════

# import os
# from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = os.path.join('static', 'uploads')
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/admin_profile')
# def admin_profile():
#     if not logged_in() or session.get('role') != 'admin':
#         flash("Access denied.", "danger")
#         return redirect('/login')
#     cursor.execute("SELECT * FROM users WHERE username=%s", (session['username'],))
#     admin = cursor.fetchone()
#     return render_template('admin_profile.html', admin=admin)

# @app.route('/admin_profile/update_info', methods=['POST'])
# def admin_profile_update_info():
#     if not logged_in() or session.get('role') != 'admin':
#         return redirect('/login')
#     username = request.form['username'].strip()
#     email    = request.form['email'].strip()
#     cursor.execute("UPDATE users SET username=%s, email=%s WHERE username=%s",
#                    (username, email, session['username']))
#     mydb.commit()
#     session['username'] = username
#     flash("Profile updated successfully!", "success")
#     return redirect('/admin_profile')

# @app.route('/admin_profile/upload_photo', methods=['POST'])
# def admin_profile_upload_photo():
#     if not logged_in() or session.get('role') != 'admin':
#         return redirect('/login')
#     file = request.files.get('photo')
#     if file and allowed_file(file.filename):
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#         filename = secure_filename(f"{session['username']}_{file.filename}")
#         file.save(os.path.join(UPLOAD_FOLDER, filename))
#         cursor.execute("UPDATE users SET profile_pic=%s WHERE username=%s",
#                        (filename, session['username']))
#         mydb.commit()
#         session['profile_pic'] = filename
#         flash("Profile photo updated!", "success")
#     else:
#         flash("Invalid file type.", "danger")
#     return redirect('/admin_profile')

# @app.route('/admin_profile/remove_photo')
# def admin_profile_remove_photo():
#     if not logged_in() or session.get('role') != 'admin':
#         return redirect('/login')
#     cursor.execute("SELECT profile_pic FROM users WHERE username=%s", (session['username'],))
#     row = cursor.fetchone()
#     if row and row[0]:
#         path = os.path.join(UPLOAD_FOLDER, row[0])
#         if os.path.exists(path):
#             os.remove(path)
#         cursor.execute("UPDATE users SET profile_pic=NULL WHERE username=%s", (session['username'],))
#         mydb.commit()
#         session.pop('profile_pic', None)
#         flash("Profile photo removed.", "info")
#     return redirect('/admin_profile')


# # ══════════════════════════════════════════════════════════════════════════════
# # FEATURE — PDF SALARY SLIP DOWNLOAD
# # ══════════════════════════════════════════════════════════════════════════════

# import io
# from datetime import date
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import mm
# from reportlab.pdfgen import canvas as rl_canvas

# def generate_salary_slip_pdf(emp, month):
#     buffer = io.BytesIO()
#     W, H = A4
#     c = rl_canvas.Canvas(buffer, pagesize=A4)

#     # Header band
#     c.setFillColor(colors.HexColor("#7c3aed"))
#     c.rect(0, H - 55*mm, W, 55*mm, fill=1, stroke=0)
#     p = c.beginPath()
#     p.moveTo(W*0.55, H); p.lineTo(W, H); p.lineTo(W, H-55*mm); p.lineTo(W*0.72, H-55*mm)
#     p.close()
#     c.setFillColor(colors.HexColor("#4f46e5"))
#     c.drawPath(p, fill=1, stroke=0)

#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 26)
#     c.drawString(18*mm, H-22*mm, "EMS")
#     c.setFont("Helvetica", 10)
#     c.setFillColor(colors.HexColor("#c4b5fd"))
#     c.drawString(18*mm, H-31*mm, "Employee Management System")
#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 18)
#     c.drawRightString(W-18*mm, H-22*mm, "SALARY SLIP")
#     c.setFont("Helvetica", 10)
#     c.setFillColor(colors.HexColor("#c4b5fd"))
#     c.drawRightString(W-18*mm, H-32*mm, month)

#     # Avatar circle
#     c.setFillColor(colors.HexColor("#ede9fe"))
#     c.circle(18*mm+14*mm, H-55*mm-22*mm, 14*mm, fill=1, stroke=0)
#     c.setFillColor(colors.HexColor("#7c3aed"))
#     c.setFont("Helvetica-Bold", 20)
#     c.drawCentredString(18*mm+14*mm, H-55*mm-26*mm, emp[1][0].upper())

#     c.setFillColor(colors.HexColor("#1e1b4b"))
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(46*mm, H-55*mm-16*mm, emp[1])
#     c.setFont("Helvetica", 10)
#     c.setFillColor(colors.HexColor("#6b7280"))
#     c.drawString(46*mm, H-55*mm-24*mm, f"{emp[2]}  |  ID: #{emp[0]}  |  {emp[4]}")

#     y_div = H-55*mm-42*mm
#     c.setStrokeColor(colors.HexColor("#e0e7ff"))
#     c.setLineWidth(1)
#     c.line(18*mm, y_div, W-18*mm, y_div)

#     def info_block(label, value, x, y):
#         c.setFont("Helvetica", 8)
#         c.setFillColor(colors.HexColor("#9ca3af"))
#         c.drawString(x, y, label.upper())
#         c.setFont("Helvetica-Bold", 11)
#         c.setFillColor(colors.HexColor("#1e1b4b"))
#         c.drawString(x, y-6*mm, value)

#     y_info = y_div-10*mm
#     info_block("Employee ID",    f"#{emp[0]}",  18*mm, y_info)
#     info_block("Full Name",      emp[1],         75*mm, y_info)
#     info_block("Department",     emp[2],         18*mm, y_info-20*mm)
#     info_block("Phone",          emp[4],         75*mm, y_info-20*mm)
#     info_block("Pay Period",     month,          18*mm, y_info-40*mm)
#     info_block("Payment Status", "Paid",         75*mm, y_info-40*mm)

#     y_table = y_info-60*mm
#     c.setFillColor(colors.HexColor("#7c3aed"))
#     c.roundRect(18*mm, y_table, W-36*mm, 10*mm, 3*mm, fill=1, stroke=0)
#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 9)
#     c.drawString(22*mm, y_table+3.2*mm, "EARNINGS & DEDUCTIONS")
#     c.drawRightString(W-22*mm, y_table+3.2*mm, "AMOUNT (INR)")

#     gross = int(emp[3])
#     hra   = round(gross*0.20); da  = round(gross*0.10)
#     basic = gross-hra-da
#     pf    = round(gross*0.04); tax = round(gross*0.05)
#     net   = gross-pf-tax

#     rows = [
#         ("Basic Salary", basic, False),
#         ("House Rent Allowance (HRA)", hra, False),
#         ("Dearness Allowance (DA)", da, False),
#         ("", None, True),
#         ("Provident Fund (PF)", -pf, False),
#         ("Income Tax (TDS)", -tax, False),
#     ]
#     row_h = 10*mm
#     y_row = y_table-row_h
#     for i, (label, amount, is_sep) in enumerate(rows):
#         if is_sep:
#             c.setStrokeColor(colors.HexColor("#e0e7ff"))
#             c.line(18*mm, y_row+row_h, W-18*mm, y_row+row_h)
#             y_row -= 3*mm; continue
#         c.setFillColor(colors.HexColor("#f8f5ff") if i%2==0 else colors.white)
#         c.rect(18*mm, y_row, W-36*mm, row_h, fill=1, stroke=0)
#         c.setFillColor(colors.HexColor("#374151"))
#         c.setFont("Helvetica", 10)
#         c.drawString(22*mm, y_row+3*mm, label)
#         c.setFillColor(colors.HexColor("#ef4444") if amount<0 else colors.HexColor("#1e1b4b"))
#         c.setFont("Helvetica-Bold", 10)
#         prefix = "-" if amount<0 else ""
#         c.drawRightString(W-22*mm, y_row+3*mm, f"{prefix}Rs. {abs(amount):,}")
#         y_row -= row_h

#     c.setFillColor(colors.HexColor("#1e1b4b"))
#     c.roundRect(18*mm, y_row-3*mm, W-36*mm, 12*mm, 3*mm, fill=1, stroke=0)
#     c.setFillColor(colors.white)
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(22*mm, y_row+1*mm, "NET PAY")
#     c.setFillColor(colors.HexColor("#4ade80"))
#     c.drawRightString(W-22*mm, y_row+1*mm, f"Rs. {net:,}")

#     c.setFillColor(colors.HexColor("#f0f4ff"))
#     c.rect(0, 0, W, 18*mm, fill=1, stroke=0)
#     c.setFillColor(colors.HexColor("#9ca3af"))
#     c.setFont("Helvetica", 8)
#     c.drawCentredString(W/2, 10*mm, "This is a system-generated salary slip and does not require a signature.")
#     c.drawCentredString(W/2, 5*mm,  f"Generated on {date.today().strftime('%d %B %Y')}  |  EMS — Employee Management System")

#     c.save()
#     buffer.seek(0)
#     return buffer


# @app.route('/salary_slip_pdf/<int:eid>')
# def salary_slip_pdf(eid):
#     block = admin_required()
#     if block: return block
#     cursor.execute("SELECT * FROM employee WHERE eid=%s", (eid,))
#     emp = cursor.fetchone()
#     if not emp:
#         flash("Employee not found.", "danger")
#         return redirect('/view_employee')
#     month = date.today().strftime("%B %Y")
#     pdf_buffer = generate_salary_slip_pdf(emp, month)
#     filename = f"salary_slip_{emp[1].replace(' ','_')}_{month.replace(' ','_')}.pdf"
#     return Response(
#         pdf_buffer.read(),
#         mimetype='application/pdf',
#         headers={'Content-Disposition': f'attachment; filename={filename}'}
#     )


# if __name__ == "__main__":
#     app.run(debug=False, port=5000)





import csv
import io
import os
from datetime import date
from flask import Flask, render_template, request, redirect, session, flash, Response, g
import sqlite3
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "ems_secret_2026"

# ══════════════════════════════════════════════════════════════════════════════
# SQLITE DATABASE  —  one connection per request using Flask's g object
# ══════════════════════════════════════════════════════════════════════════════
DATABASE = "company.db"


def get_db():
    """Return the database connection for the current request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row   # rows behave like dicts AND support index
    return g.db


@app.teardown_appcontext
def close_db(error):
    """Close DB connection at end of every request automatically."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def q(sql, params=(), fetch="all"):
    """
    Run any SQL query.
      fetch='all'  → list of rows  (SELECT)
      fetch='one'  → single row    (SELECT)
      fetch=None   → write op      (INSERT / UPDATE / DELETE)
    SQLite uses ? placeholders — NOT %s like MySQL.
    """
    db  = get_db()
    cur = db.execute(sql, params)
    if fetch == "one":
        return cur.fetchone()
    if fetch == "all":
        return cur.fetchall()
    db.commit()          # commit writes immediately
    return None


# ── MAIL ──────────────────────────────────────────────────────────────────────
app.config["MAIL_SERVER"]   = "smtp.gmail.com"
app.config["MAIL_PORT"]     = 587
app.config["MAIL_USE_TLS"]  = True
app.config["MAIL_USERNAME"] = "vaishnavisunkara126@gmail.com"
app.config["MAIL_PASSWORD"] = "mton ahrh ffqr etzr"
mail       = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

BASE_URL = "http://127.0.0.1:5000"   # change to your PythonAnywhere URL when deployed

# ── UPLOAD FOLDER ─────────────────────────────────────────────────────────────
UPLOAD_FOLDER      = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def logged_in():
    return session.get("username") is not None


def admin_required():
    if not logged_in():
        flash("Please log in to continue.", "warning")
        return redirect("/login")
    if session.get("role") != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect("/dashboard")
    return None


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC PAGES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    if logged_in():
        return redirect("/dashboard")
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name    = request.form["name"].strip()
        email   = request.form["email"].strip()
        message = request.form["message"].strip()
        try:
            msg = Message(
                subject=f"EMS Contact Form — Message from {name}",
                sender=app.config["MAIL_USERNAME"],
                recipients=[app.config["MAIL_USERNAME"]],
            )
            msg.body = (
                f"New message from the EMS Contact Form.\n\n"
                f"Name   : {name}\nEmail  : {email}\n\nMessage:\n{message}\n\n— EMS"
            )
            confirm = Message(
                subject="EMS — We received your message!",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email],
            )
            confirm.body = (
                f"Hi {name},\n\nThank you! We received your message and will reply soon.\n\n"
                f'Your message:\n"{message}"\n\n— EMS Team'
            )
            mail.send(msg)
            mail.send(confirm)
            flash("Your message has been sent! A confirmation has been emailed to you.", "success")
        except Exception:
            flash("Failed to send message. Please try again later.", "danger")
        return redirect("/contact")
    return render_template("contact.html")


# ══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/register", methods=["GET", "POST"])
def register():
    if logged_in():
        return redirect("/dashboard")
    if request.method == "POST":
        email = request.form["email"].strip()
        uname = request.form["username"].strip()
        pwd   = request.form["password"]
        cpwd  = request.form["cpassword"]
        role  = request.form.get("role", "emp")

        if pwd != cpwd:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect("/register")

        if q("SELECT id FROM users WHERE username=?", (uname,), fetch="one"):
            flash("Username already taken. Please choose another.", "warning")
            return redirect("/register")

        q("INSERT INTO users(email, username, password, role) VALUES(?,?,?,?)",
          (email, uname, pwd, role), fetch=None)
        flash("Registration successful! Please log in.", "success")
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if logged_in():
        return redirect("/dashboard")
    if request.method == "POST":
        uname = request.form["username"].strip()
        pwd   = request.form["password"]
        user  = q("SELECT * FROM users WHERE username=? AND password=?",
                   (uname, pwd), fetch="one")
        if user:
            session["username"]    = user["username"]
            session["role"]        = user["role"]
            session["profile_pic"] = user["profile_pic"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect("/dashboard")
        flash("Invalid username or password. Please try again.", "danger")
        return redirect("/login")
    return render_template("login.html")


@app.route("/logout")
def logout():
    name = session.get("username", "")
    session.clear()
    flash(f"You have been logged out successfully, {name}.", "info")
    return redirect("/login")


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/dashboard")
def dashboard():
    if not logged_in():
        flash("Please log in to continue.", "warning")
        return redirect("/login")
    if session.get("role") == "admin":
        total_emp   = q("SELECT COUNT(*) FROM employee",              fetch="one")[0]
        total_dept  = q("SELECT COUNT(DISTINCT edept) FROM employee", fetch="one")[0]
        total_users = q("SELECT COUNT(*) FROM users",                 fetch="one")[0]
        recent      = q("SELECT * FROM employee ORDER BY eid DESC LIMIT 5", fetch="all")
        return render_template("dashboard.html",
                               total_emp=total_emp,
                               total_dept=total_dept,
                               total_users=total_users,
                               recent=recent)
    return redirect("/emp_dashboard")


@app.route("/emp_dashboard")
def emp_dashboard():
    if not logged_in():
        flash("Please log in to continue.", "warning")
        return redirect("/login")
    emp = q("SELECT * FROM employee WHERE username=?",
            (session["username"],), fetch="one")
    return render_template("emp_dashboard.html", emp=emp)


# ══════════════════════════════════════════════════════════════════════════════
# EMPLOYEE MANAGEMENT  (Admin only)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    block = admin_required()
    if block: return block
    if request.method == "POST":
        name   = request.form["ename"].strip()
        dept   = request.form["edept"].strip()
        salary = request.form["esalary"]
        phone  = request.form["ephone"].strip()
        uname  = request.form["username"].strip()
        q("INSERT INTO employee(ename, edept, esalary, ephone, username) VALUES(?,?,?,?,?)",
          (name, dept, salary, phone, uname), fetch=None)
        flash(f"Employee '{name}' added successfully!", "success")
        return redirect("/view_employee")
    return render_template("add_employee.html")


@app.route("/view_employee")
def view_employee():
    block = admin_required()
    if block: return block
    employees = q("SELECT * FROM employee ORDER BY eid DESC", fetch="all")
    return render_template("view_employee.html", employees=employees)


@app.route("/edit/<int:eid>", methods=["GET", "POST"])
def edit_employee(eid):
    block = admin_required()
    if block: return block
    if request.method == "POST":
        name   = request.form["ename"].strip()
        dept   = request.form["edept"].strip()
        salary = request.form["esalary"]
        phone  = request.form["ephone"].strip()
        q("UPDATE employee SET ename=?, edept=?, esalary=?, ephone=? WHERE eid=?",
          (name, dept, salary, phone, eid), fetch=None)
        flash(f"Employee '{name}' updated successfully!", "success")
        return redirect("/view_employee")
    emp = q("SELECT * FROM employee WHERE eid=?", (eid,), fetch="one")
    if not emp:
        flash("Employee not found.", "danger")
        return redirect("/view_employee")
    return render_template("edit_employee.html", emp=emp)


@app.route("/delete/<int:eid>")
def delete_employee(eid):
    block = admin_required()
    if block: return block
    emp = q("SELECT ename FROM employee WHERE eid=?", (eid,), fetch="one")
    if emp:
        q("DELETE FROM employee WHERE eid=?", (eid,), fetch=None)
        flash(f"Employee '{emp['ename']}' deleted successfully.", "success")
    else:
        flash("Employee not found.", "danger")
    return redirect("/view_employee")


@app.route("/search")
def search():
    block = admin_required()
    if block: return block
    sq = request.args.get("q", "").strip()
    if not sq:
        flash("Please enter a search term.", "warning")
        return redirect("/view_employee")
    term    = f"%{sq}%"
    results = q(
        "SELECT * FROM employee WHERE ename LIKE ? OR edept LIKE ? OR ephone LIKE ? OR username LIKE ?",
        (term, term, term, term), fetch="all"
    )
    return render_template("search_results.html", results=results, q=sq)


# ══════════════════════════════════════════════════════════════════════════════
# PASSWORD RESET
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"].strip()
        user  = q("SELECT * FROM users WHERE email=?", (email,), fetch="one")
        if user:
            token      = serializer.dumps(email, salt="reset-password")
            reset_link = f"{BASE_URL}/reset_password/{token}"
            msg = Message(
                "EMS — Password Reset Request",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email],
            )
            msg.body = (
                f"Hello {user['username']},\n\n"
                f"Reset your EMS password here (valid for 10 minutes):\n{reset_link}\n\n"
                f"Ignore this email if you did not request it.\n\n— EMS Team"
            )
            mail.send(msg)
            flash("Password reset link sent to your email!", "success")
            return redirect("/forgot_password")
        flash("No account found with that email address.", "danger")
        return redirect("/forgot_password")
    return render_template("forgot_password.html")


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="reset-password", max_age=600)
    except Exception:
        flash("This reset link is invalid or has expired. Please request a new one.", "danger")
        return redirect("/forgot_password")
    if request.method == "POST":
        pwd  = request.form["password"]
        cpwd = request.form["cpassword"]
        if pwd != cpwd:
            flash("Passwords do not match.", "danger")
            return redirect(request.url)
        q("UPDATE users SET password=? WHERE email=?", (pwd, email), fetch=None)
        flash("Password reset successful! Please log in.", "success")
        return redirect("/login")
    return render_template("reset_password.html", token=token)


# ══════════════════════════════════════════════════════════════════════════════
# EXPORT CSV
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/export_csv")
def export_csv():
    block = admin_required()
    if block: return block
    rows   = q("SELECT eid, ename, edept, esalary, ephone, username FROM employee ORDER BY eid",
               fetch="all")
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Department", "Salary", "Phone", "Username"])
    for row in rows:
        writer.writerow(list(row))
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=employees.csv"},
    )


# ══════════════════════════════════════════════════════════════════════════════
# CHANGE PASSWORD
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if not logged_in():
        flash("Please log in to continue.", "warning")
        return redirect("/login")
    if request.method == "POST":
        current = request.form["current_password"]
        new_pwd = request.form["new_password"]
        confirm = request.form["confirm_password"]
        uname   = session["username"]
        if not q("SELECT id FROM users WHERE username=? AND password=?",
                  (uname, current), fetch="one"):
            flash("Current password is incorrect.", "danger")
            return redirect("/change_password")
        if new_pwd != confirm:
            flash("New passwords do not match.", "danger")
            return redirect("/change_password")
        if len(new_pwd) < 6:
            flash("Password must be at least 6 characters.", "warning")
            return redirect("/change_password")
        q("UPDATE users SET password=? WHERE username=?", (new_pwd, uname), fetch=None)
        flash("Password changed successfully!", "success")
        return redirect("/dashboard" if session.get("role") == "admin" else "/emp_dashboard")
    return render_template("change_password.html")


# ══════════════════════════════════════════════════════════════════════════════
# SALARY SLIP  (HTML printable page)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/salary_slip/<int:eid>")
def salary_slip(eid):
    block = admin_required()
    if block: return block
    emp = q("SELECT * FROM employee WHERE eid=?", (eid,), fetch="one")
    if not emp:
        flash("Employee not found.", "danger")
        return redirect("/view_employee")
    return render_template("salary_slip.html", emp=emp,
                           month=date.today().strftime("%B %Y"))


# ══════════════════════════════════════════════════════════════════════════════
# SALARY SLIP  (PDF download via ReportLab)
# ══════════════════════════════════════════════════════════════════════════════

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas as rl_canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_salary_slip_pdf(emp, month):
    buffer = io.BytesIO()
    W, H   = A4
    c      = rl_canvas.Canvas(buffer, pagesize=A4)

    # Header band
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.rect(0, H - 55*mm, W, 55*mm, fill=1, stroke=0)
    p = c.beginPath()
    p.moveTo(W*0.55, H); p.lineTo(W, H)
    p.lineTo(W, H-55*mm); p.lineTo(W*0.72, H-55*mm)
    p.close()
    c.setFillColor(colors.HexColor("#4f46e5"))
    c.drawPath(p, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(18*mm, H-22*mm, "EMS")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#c4b5fd"))
    c.drawString(18*mm, H-31*mm, "Employee Management System")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawRightString(W-18*mm, H-22*mm, "SALARY SLIP")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#c4b5fd"))
    c.drawRightString(W-18*mm, H-32*mm, month)

    # Avatar circle
    c.setFillColor(colors.HexColor("#ede9fe"))
    c.circle(32*mm, H-78*mm, 14*mm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(32*mm, H-82*mm, emp["ename"][0].upper())

    c.setFillColor(colors.HexColor("#1e1b4b"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(52*mm, H-72*mm, emp["ename"])
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#6b7280"))
    c.drawString(52*mm, H-80*mm,
                 f"{emp['edept']}  |  ID: #{emp['eid']}  |  {emp['ephone']}")

    y_div = H-97*mm
    c.setStrokeColor(colors.HexColor("#e0e7ff"))
    c.line(18*mm, y_div, W-18*mm, y_div)

    def info_block(label, value, x, y):
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#9ca3af"))
        c.drawString(x, y, label.upper())
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor("#1e1b4b"))
        c.drawString(x, y-6*mm, value)

    yi = y_div - 10*mm
    info_block("Employee ID",    f"#{emp['eid']}",  18*mm, yi)
    info_block("Full Name",      emp["ename"],       80*mm, yi)
    info_block("Department",     emp["edept"],       18*mm, yi-20*mm)
    info_block("Phone",          emp["ephone"],      80*mm, yi-20*mm)
    info_block("Pay Period",     month,              18*mm, yi-40*mm)
    info_block("Payment Status", "Paid",             80*mm, yi-40*mm)

    yt = yi - 60*mm
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.roundRect(18*mm, yt, W-36*mm, 10*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(22*mm, yt+3.2*mm, "EARNINGS & DEDUCTIONS")
    c.drawRightString(W-22*mm, yt+3.2*mm, "AMOUNT (INR)")

    gross = int(emp["esalary"])
    hra   = round(gross * 0.20)
    da    = round(gross * 0.10)
    basic = gross - hra - da
    pf    = round(gross * 0.04)
    tax   = round(gross * 0.05)
    net   = gross - pf - tax

    row_h = 10*mm
    yr    = yt - row_h
    for i, (label, amount) in enumerate([
        ("Basic Salary",                   basic),
        ("House Rent Allowance (HRA)",      hra),
        ("Dearness Allowance (DA)",         da),
        ("Provident Fund (PF)",            -pf),
        ("Income Tax (TDS)",               -tax),
    ]):
        c.setFillColor(colors.HexColor("#f8f5ff") if i % 2 == 0 else colors.white)
        c.rect(18*mm, yr, W-36*mm, row_h, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#374151"))
        c.setFont("Helvetica", 10)
        c.drawString(22*mm, yr+3*mm, label)
        c.setFillColor(colors.HexColor("#ef4444") if amount < 0 else colors.HexColor("#1e1b4b"))
        c.setFont("Helvetica-Bold", 10)
        prefix = "-" if amount < 0 else ""
        c.drawRightString(W-22*mm, yr+3*mm, f"{prefix}Rs. {abs(amount):,}")
        yr -= row_h

    c.setFillColor(colors.HexColor("#1e1b4b"))
    c.roundRect(18*mm, yr-3*mm, W-36*mm, 12*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(22*mm, yr+1*mm, "NET PAY")
    c.setFillColor(colors.HexColor("#4ade80"))
    c.drawRightString(W-22*mm, yr+1*mm, f"Rs. {net:,}")

    c.setFillColor(colors.HexColor("#f0f4ff"))
    c.rect(0, 0, W, 18*mm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#9ca3af"))
    c.setFont("Helvetica", 8)
    c.drawCentredString(W/2, 10*mm,
        "This is a system-generated salary slip and does not require a signature.")
    c.drawCentredString(W/2, 5*mm,
        f"Generated on {date.today().strftime('%d %B %Y')}  |  EMS — Employee Management System")

    c.save()
    buffer.seek(0)
    return buffer


@app.route("/salary_slip_pdf/<int:eid>")
def salary_slip_pdf(eid):
    block = admin_required()
    if block: return block
    if not REPORTLAB_AVAILABLE:
        flash("PDF generation requires reportlab. Run: pip install reportlab", "warning")
        return redirect(f"/salary_slip/{eid}")
    emp = q("SELECT * FROM employee WHERE eid=?", (eid,), fetch="one")
    if not emp:
        flash("Employee not found.", "danger")
        return redirect("/view_employee")
    month    = date.today().strftime("%B %Y")
    pdf_buf  = generate_salary_slip_pdf(emp, month)
    filename = f"salary_slip_{emp['ename'].replace(' ','_')}_{month.replace(' ','_')}.pdf"
    return Response(
        pdf_buf.read(),
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# ══════════════════════════════════════════════════════════════════════════════
# MANAGE USERS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/manage_users")
def manage_users():
    block = admin_required()
    if block: return block
    users = q("SELECT id, email, username, role FROM users ORDER BY id DESC", fetch="all")
    return render_template("manage_users.html", users=users)


@app.route("/delete_user/<int:uid>")
def delete_user(uid):
    block = admin_required()
    if block: return block
    u = q("SELECT username FROM users WHERE id=?", (uid,), fetch="one")
    if u and u["username"] == session.get("username"):
        flash("You cannot delete your own account.", "warning")
        return redirect("/manage_users")
    if u:
        q("DELETE FROM users WHERE id=?", (uid,), fetch=None)
        flash(f"User '{u['username']}' deleted.", "success")
    return redirect("/manage_users")


# ══════════════════════════════════════════════════════════════════════════════
# ADMIN PROFILE
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/admin_profile")
def admin_profile():
    if not logged_in() or session.get("role") != "admin":
        flash("Access denied.", "danger")
        return redirect("/login")
    admin = q("SELECT * FROM users WHERE username=?",
              (session["username"],), fetch="one")
    return render_template("admin_profile.html", admin=admin)


@app.route("/admin_profile/update_info", methods=["POST"])
def admin_profile_update_info():
    if not logged_in() or session.get("role") != "admin":
        return redirect("/login")
    username = request.form["username"].strip()
    email    = request.form["email"].strip()
    q("UPDATE users SET username=?, email=? WHERE username=?",
      (username, email, session["username"]), fetch=None)
    session["username"] = username
    flash("Profile updated successfully!", "success")
    return redirect("/admin_profile")


@app.route("/admin_profile/upload_photo", methods=["POST"])
def admin_profile_upload_photo():
    if not logged_in() or session.get("role") != "admin":
        return redirect("/login")
    file = request.files.get("photo")
    if file and allowed_file(file.filename):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(f"{session['username']}_{file.filename}")
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        q("UPDATE users SET profile_pic=? WHERE username=?",
          (filename, session["username"]), fetch=None)
        session["profile_pic"] = filename
        flash("Profile photo updated!", "success")
    else:
        flash("Invalid file type. Use PNG, JPG, GIF or WEBP.", "danger")
    return redirect("/admin_profile")


@app.route("/admin_profile/remove_photo")
def admin_profile_remove_photo():
    if not logged_in() or session.get("role") != "admin":
        return redirect("/login")
    row = q("SELECT profile_pic FROM users WHERE username=?",
            (session["username"],), fetch="one")
    if row and row["profile_pic"]:
        path = os.path.join(UPLOAD_FOLDER, row["profile_pic"])
        if os.path.exists(path):
            os.remove(path)
        q("UPDATE users SET profile_pic=NULL WHERE username=?",
          (session["username"],), fetch=None)
        session.pop("profile_pic", None)
        flash("Profile photo removed.", "info")
    return redirect("/admin_profile")


# ══════════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════════
application = app   # required for PythonAnywhere WSGI

if __name__ == "__main__":
    app.run(debug=True, port=5000)