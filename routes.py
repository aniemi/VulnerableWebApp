from flask import session, redirect, request, url_for, render_template
from data import get_all, get_user_pastes, get_paste, user_credentials, save_paste_to_db

def index(): 
    if 'user' in session: 
        user = session['user']
        return render_template("index.html", pastes=get_all(), user_pastes=get_user_pastes(user), user=user)
    else:
        user = 'Not logged in'
    
    return render_template("index.html", pastes=get_all(), user=user)

def form(): 
    text = request.args.get('text')
    is_private = request.args.get('private') != None
    if 'user' in session:
        user = session['user']
    else: 
        user = 'Not logged in'

    query = "INSERT INTO pastes (body, private_paste, user) VALUES ('" + text + "', '" + str(is_private) + "', '" + user + "');"
    print(query)
    try: 
        save_paste_to_db(query)
    except: 
        print("Error.")
    return redirect(url_for('index'))

def paste():
    id = request.args.get('paste')
    if 'user' in session: 
        user = session['user']
        paste = get_paste(id, user)
        return render_template("index.html", paste=paste, pastes=get_all(), user_pastes=get_user_pastes(session['user']), user=session['user'])
    else: 
        user = "Not logged in"
    paste = get_paste(id)
    return render_template("index.html", paste=paste, pastes=get_all(), user=user)


def login(): 
    user = str(request.form.get('user'))
    pw = str(request.form.get('pw'))
    credentials = user_credentials(user)
    error = "None"

    if not user: 
        error = 'Username is empty.'
    elif not pw: 
        error = 'Password is empty.'

    if credentials:
        credentials = credentials[0]
        login_user = credentials[0]
        login_pw = credentials[1]
        if 'user' not in session:
            if user == login_user and pw == login_pw:
                session['user'] = user
                return render_template("index.html", pastes=get_all(), user_pastes=get_user_pastes(user), user=login_user)
            else: 
                return redirect(url_for('index'))
                
        else: 
            return render_template("index.html", pastes=get_all(), user_pastes=get_user_pastes(user), user='Not logged in')


def logout(): 
    session.pop('user', None)
    return redirect(url_for('index'))