from flask import session, redirect, request, url_for, render_template
from data import get_all, get_user_pastes, get_paste, user_credentials, save_paste_to_db

def get_user_in_session(): 
    if 'user' in session: 
        user = session['user']
    else: 
        user = None
    return user

def is_logged_in():
    if 'user' in session:
        return True
    else: 
        return False

def index(): 
    user = get_user_in_session()
    if is_logged_in(): 
        return render_template('logged_in.html', pastes=get_all(), user=user, user_pastes=get_user_pastes(user))
    
    return render_template('index.html', pastes=get_all())

def form(): 
    text = request.args.get('text')
    is_private = request.args.get('private') != None
    if is_logged_in(): 
        user = get_user_in_session()
    else: 
        user = 'Not logged in'

    try: 
        save_paste_to_db(text, is_private, user)
    except: 
        print("Error.")

    return index()

def paste():
    id = request.args.get('paste')
    if is_logged_in(): 
        user = get_user_in_session()
        paste = get_paste(id, user)
        return render_template("logged_in.html", paste=paste, pastes=get_all(), user_pastes=get_user_pastes(session['user']), user=session['user'])

    paste = get_paste(id)
    return render_template("index.html", paste=paste, pastes=get_all())

def login(): 
    user = str(request.form.get('user'))
    pw = str(request.form.get('pw'))
    error = "None"

    if not user or not pw: 
        error = 'Fill username and password.'

    if is_logged_in() is False:
        user_verified = verify_credentials(user, pw)

    if user_verified:
        session['user'] = user

    return index()

def verify_credentials(user, pw): 
    credentials = user_credentials(user)

    if credentials:
        credentials = credentials[0]
        login_user = credentials[0]
        login_pw = credentials[1]

        if user == login_user and pw == login_pw: 
            return True
        else: 
            return False


def logout(): 
    session.pop('user', None)
    return redirect(url_for('index'))