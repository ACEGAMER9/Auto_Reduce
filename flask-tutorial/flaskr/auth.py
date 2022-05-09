import functools
from re import A
import requests
import pandas as pd
import random #Import for Test#
from flask import (
Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


bp = Blueprint('auth', __name__, url_prefix='/auth')

########## HOME PAGE ROUTE ##########
@bp.route("/")
def Home():
    return render_template('Home.html')

########## REGISTER ROUTE ##########
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

########## LOGIN ROUTE ##########

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
            
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.Home'))

        flash(error)

    return render_template('auth/login.html')

########## CHECK USER ID ##########

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

########## LOGOUT ROUTE ##########

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.Home'))

########## REQUEST LOGIN ##########

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

########## PROGRAM ROUTE ##########

@bp.route('/profile', methods=('GET', 'POST'))
def profile():

    return render_template('auth/profile.html')

########## PROGRAM ROUTE ##########

@bp.route('/program', methods=('GET', 'POST'))
def program():
    # https://api.openweathermap.org/data/2.5/weather?zip=94040,us&appid={API key}
    user_api = "7b9a86d2006cc3e7c4c1c2d4bc38d743"
    Zipcode = "20000" # ZIPCODE FOR SELECT LOCATION
    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?zip="+Zipcode+",th&appid="+user_api
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    temp_city = ((api_data['main']['temp']) - 273.15)
    weather_desc = api_data['weather'][0]['description']
    ftemp_city ="{:.2f}".format(float(temp_city))

    ### SECTION PREDICTMODEL ####
    data=pd.read_csv("flaskr\DataFake1_tree.csv")
    data.head()
    X = data.iloc[:, [ 1, 2, 3, 4]].values
    y = data.iloc[:, 5].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=22)
    clf = MLPClassifier(hidden_layer_sizes=(100), 
                        max_iter=300,
                        activation = 'logistic',
                        solver='adam',
                        random_state=1)
    history = clf.fit(X_train,y_train)
    ypred = clf.predict(X_test)

    def prediction(A, weather_desc, temp_city, B):
        if weather_desc.find("rain"):
            weather_desc = 1
        else:
            weather_desc = 0
        inpredict = [[A,weather_desc,temp_city,B]]
        opredict = clf.predict(inpredict)

        return opredict
    Moisture = random.randrange(50,100)
    Light = random.randrange(0,100)
    Status = prediction(Moisture, weather_desc, temp_city, Light)
    if Status == 0:
        Status = "BAD"
    else:
        Status = "GOOD"

    return render_template('auth/program.html', 
                            data={"temp":ftemp_city, 
                                  "weather":weather_desc, 
                                  "Status":Status,
                                  "Moisture":Moisture,
                                  "Light":Light})
