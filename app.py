from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from io import BytesIO
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/event_database'
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)

class events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    data = db.Column(db.LargeBinary , nullable=False)
    date = db.Column(db.String , nullable=False)
    e_name = db.Column(db.String , nullable=False)
    organizer = db.Column(db.String , nullable=False)
    phone = db.Column(db.String , nullable=False)
    school = db.Column(db.String , nullable=False)
    department = db.Column(db.String , nullable=False)
    email = db.Column(db.String , nullable=False)
    user = db.Column(db.String , nullable=False)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    session.clear()
    sort_date = request.form.get('sort')
    search_query = request.form.get('search')
    if search_query:
        date_range = 999
    else:
        date_range = 90
    today = datetime.now().date()
    next_dates = [today + timedelta(days=i) for i in range(date_range)]
    events_by_date = {}


    if sort_date:
        sort_date = datetime.strptime(sort_date, '%Y-%m-%d').date()
        next_dates = [sort_date]
    else:
        for date in next_dates:
            if search_query:
                events_to_show = events.query.filter(
                    (events.date == date.strftime('%Y-%m-%d')) &
                    ((events.e_name.ilike(f"%{search_query}%")) |
                     (events.school.ilike(f"%{search_query}%")) |
                     (events.department.ilike(f"%{search_query}%")))
                ).all()
            else:
                events_to_show = events.query.filter(events.date == date.strftime('%Y-%m-%d')).all()
            events_by_date[date] = events_to_show

    if sort_date:
        if search_query:
            events_to_show = events.query.filter(
                (events.date == sort_date.strftime('%Y-%m-%d')) &
                ((events.e_name.ilike(f"%{search_query}%")) |
                 (events.school.ilike(f"%{search_query}%")) |
                 (events.department.ilike(f"%{search_query}%")))
            ).all()
        else:
            events_to_show = events.query.filter(events.date == sort_date.strftime('%Y-%m-%d')).all()
        events_by_date[sort_date] = events_to_show

    return render_template('index.html', events_by_date=events_by_date, next_dates=next_dates)



@app.route('/image/<int:event_id>')
def image(event_id):
    event = events.query.get(event_id)
    if event and event.data:
        return send_file(BytesIO(event.data), mimetype='image/jpeg')
    return 'Image not found', 404

@app.route('/SOET', methods=['GET', 'POST'])
def SOET():
    return school_page('SOET')

@app.route('/SOBAS', methods=['GET', 'POST'])
def SOBAS():
    return school_page('SOBAS')

@app.route('/SOLACS', methods=['GET', 'POST'])
def SOLACS():
    return school_page('SOLACS')

@app.route('/SOBE', methods=['GET', 'POST'])
def SOBE():
    return school_page('SOBE')

@app.route('/SOLJ', methods=['GET', 'POST'])
def SOLJ():
    return school_page('SOLJ')

@app.route('/SOMC', methods=['GET', 'POST'])
def SOMC():
    return school_page('SOMC')

@app.route('/SOE', methods=['GET', 'POST'])
def SOE():
    return school_page('SOE')

@app.route('/SOLSBT', methods=['GET', 'POST'])
def SOLSBT():
    return school_page('SOLSBT')

@app.route('/SOMS', methods=['GET', 'POST'])
def SOMS():
    return school_page('SOMS')

@app.route('/SOSAG', methods=['GET', 'POST'])
def SOSAG():
    return school_page('SOSAG')

def school_page(school_name):
    session.clear()
    sort_date = request.form.get('sort')
    search_query = request.form.get('search')
    
    if search_query:
        date_range = 999
    else:
        date_range = 90
    
    today = datetime.now().date()
    next_dates = [today + timedelta(days=i) for i in range(date_range)]
    events_by_date = {}

    if sort_date:
        sort_date = datetime.strptime(sort_date, '%Y-%m-%d').date()
        next_dates = [sort_date]
        if search_query:
            events_to_show = events.query.filter(
                (events.date == sort_date.strftime('%Y-%m-%d')) &
                (events.school.ilike(school_name)) &
                ((events.e_name.ilike(f"%{search_query}%")) |
                 (events.department.ilike(f"%{search_query}%")))
            ).all()
        else:
            events_to_show = events.query.filter(
                (events.date == sort_date.strftime('%Y-%m-%d')) &
                (events.school.ilike(school_name))
            ).all()
        events_by_date[sort_date] = events_to_show
    else:
        for date in next_dates:
            if search_query:
                events_to_show = events.query.filter(
                    (events.date == date.strftime('%Y-%m-%d')) &
                    (events.school.ilike(school_name)) &
                    ((events.e_name.ilike(f"%{search_query}%")) |
                     (events.department.ilike(f"%{search_query}%")))
                ).all()
            else:
                events_to_show = events.query.filter(
                    (events.date == date.strftime('%Y-%m-%d')) &
                    (events.school.ilike(school_name))
                ).all()
            events_by_date[date] = events_to_show

    return render_template(f'{school_name}.html', events_by_date=events_by_date, next_dates=next_dates)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' not in session:
        return redirect(url_for('verification'))  # Redirect to verification if not authenticated

    user = session['user']
    sort_date = request.form.get('sort')
    search_query = request.form.get('search')
    
    today = datetime.now().date()

    if sort_date:
        sort_date = datetime.strptime(sort_date, '%Y-%m-%d').date()
        date_range = [sort_date]
    else:
        date_range = [today + timedelta(days=i) for i in range(90)]

    events_by_date = {}

    for date in date_range:
        query = events.query.filter(events.date == date.strftime('%Y-%m-%d'), events.user == user)
        
        if search_query:
            query = query.filter(
                (events.e_name.ilike(f"%{search_query}%")) |
                (events.school.ilike(f"%{search_query}%")) |
                (events.department.ilike(f"%{search_query}%"))
            )
        
        events_to_show = query.all()
        events_by_date[date] = events_to_show

    return render_template('admin.html', events_by_date=events_by_date, next_dates=date_range)



@app.route('/admin_upload_event', methods=['GET', 'POST'])
def admin_upload_event():
    if 'user' not in session:
        return redirect(url_for('verification'))  # Redirect to verification if not authenticated

    user = session['user']
    
    if request.method == 'POST':
        image = request.files.get('image')
        if not image:
            return redirect(url_for('admin'))

        name = secure_filename(image.filename)
        image_data = image.read()
        date = request.form.get('date')
        e_name = request.form.get('e_name')
        organizer = request.form.get('organizer')
        phone = request.form.get('phone')
        school = request.form.get('school')
        department = request.form.get('department')
        email = request.form.get('email')

        # Create and save the new event
        upload = events(name=name, data=image_data, date=date, e_name=e_name, organizer=organizer,
                        phone=phone, school=school, department=department, email=email, user=user)
        db.session.add(upload)
        db.session.commit()

        return redirect('admin')

    return render_template('admin_upload_event.html')


@app.route('/verification', methods=['GET', 'POST'])
def verification():
    if 'user' in session:
        return redirect('admin')
    
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        if username == 'bhabna.de@faculty.adamasuniversity.ac.in' and password == 'sexymadam':
            session['user'] = username
            return redirect('admin')
        else:
            return render_template('verification.html', error='Invalid credentials')
    return render_template('verification.html')


if __name__ == '__main__':
    app.run(debug=True)
