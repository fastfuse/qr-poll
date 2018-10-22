from app import app
from flask import render_template, session, request, make_response, redirect, url_for


@app.route('/')
@app.route('/index')
def index():

    addrs = session.setdefault('addrs', [])
    polls = session.setdefault('polls', 0)

    return render_template('index.html', polls=polls, addrs=addrs)



@app.route('/vote')
def vote():

    addrs = session.setdefault('addrs', [])

    # if request.cookies.get('voted') == 'True':
    if request.remote_addr in addrs:
        return render_template('voted.html', voted=True)

    if 'polls' not in session.keys():
        session['polls'] = 1
    else:
        session['polls'] += 1

    addrs.append(request.remote_addr)
    session['addrs'] = addrs

    resp = make_response(render_template('voted.html'))

    resp.set_cookie('voted', 'True')

    return resp


@app.route('/pop')
def pop():

    resp = make_response(redirect(url_for('index')))

    resp.set_cookie('voted', 'False')

    addrs = session.setdefault('addrs', [])
    addrs.remove(request.remote_addr)
    session['addrs'] = addrs

    return resp
