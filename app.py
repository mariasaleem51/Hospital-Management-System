from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config, db
import bcrypt
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# ---------------------------------------------------------
# MAIN OVERVIEW NODE
# ---------------------------------------------------------
@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html', current_view='login')

    stats = {
        "doctors": db.users.count_documents({"role": "Doctor"}),
        "patients": db.appointments.count_documents({}), # Direct appointments count as patient encounters
        "appointments": db.appointments.count_documents({})
    }
    
    current_view = request.args.get('view', 'dashboard')
    role = session.get('role')
    doctors_list = list(db.users.find({"role": "Doctor"}))
    appointments = []

    if role == 'Doctor':
        appointments = list(db.appointments.find({"doctor_id": session.get('user_id')}))
    elif role == 'Admin':
        appointments = list(db.appointments.find({}))

    return render_template(
        'index.html', 
        stats=stats, 
        doctors_list=doctors_list, 
        appointments=appointments, 
        current_view=current_view
    )

# ---------------------------------------------------------
# ACTION: SECURE SIGN-IN ENGINE
# ---------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    
    user = db.users.find_one({"email": email})
    
    # Password verification using safe decoding checks
    if user and user.get('password') and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']):
        session['user_id'] = str(user['_id'])
        session['name'] = user['name']
        session['role'] = user['role']
        flash(f"Welcome, {user['name']}. Terminal session authenticated.", "success")
    else:
        flash("Access Denied: Invalid medical staff credentials.", "danger")
        
    return redirect(url_for('index'))

# ---------------------------------------------------------
# ACTION: COMMIT NEW DOCTOR REGISTRY (ADMIN STRATAGEM)
# ---------------------------------------------------------
@app.route('/admin/add-doctor', methods=['POST'])
def add_doctor():
    if session.get('role') != 'Admin':
        flash("Unauthorized terminal override blocked.", "danger")
        return redirect(url_for('index'))

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    department = request.form.get('department', 'General Medicine').strip()

    if not name or not email or not password:
        flash("Provisioning Failed: All system fields are mandatory.", "danger")
        return redirect(url_for('index', view='roster'))

    if db.users.find_one({"email": email}):
        flash("Data Identity Conflict: Email already assigned to active node.", "danger")
        return redirect(url_for('index', view='roster'))

    try:
        # Advanced Hashing Engine deployment
        salt = bcrypt.gensalt()
        # CRITICAL FIX: Hash ko .decode('utf-8') kiya taake MongoDB me string format me save ho ske
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_pw,
            "role": "Doctor",
            "department": department
        })
        
        flash(f"Success: {name} provisioned into the operational database.", "success")
    except Exception as e:
        print(f"Database Insertion Error: {str(e)}")
        flash(f"Database error occurred: {str(e)}", "danger")

    return redirect(url_for('index', view='roster'))

# ---------------------------------------------------------
# ACTION: COMMIT OUTPATIENT LOG (DIAGNOSTIC PIPELINE)
# ---------------------------------------------------------
@app.route('/doctor/add-patient', methods=['POST'])
def add_patient():
    if session.get('role') != 'Doctor' and session.get('role') != 'Admin':
        flash("Privilege Level Insufficient for Patient Entry.", "danger")
        return redirect(url_for('index'))

    patient_name = request.form.get('patient_name', '').strip()
    time = request.form.get('time', '').strip()
    reason = request.form.get('reason', '').strip()

    if not patient_name or not time or not reason:
        flash("Failed: Encounter details cannot be empty.", "danger")
        return redirect(url_for('index'))

    # Injecting complete database entry point
    db.appointments.insert_one({
        "doctor_id": session.get('user_id'),
        "patient_name": patient_name,
        "time": time,
        "reason": reason,
        "created_at": datetime.utcnow()
    })

    flash(f"Patient chart successfully registered for {patient_name}.", "success")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Session decoupled successfully.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)