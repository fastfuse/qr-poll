from app import app
from flask import render_template, session, request, make_response, redirect, url_for

POLL = [
    {'id': 1, 'name': 'Option 1'},
    {'id': 2, 'name': 'Option 2'},
    {'id': 3, 'name': 'Option 3'},
]


@app.route('/')
@app.route('/index')
def index():
    addrs = session.setdefault('addrs', [])
    voted = request.remote_addr in addrs

    return render_template('index.html', addrs=addrs, voted=voted, poll=POLL)


@app.route('/vote/<id>')
def vote(id):
    addrs = session.setdefault('addrs', [])

    if request.remote_addr in addrs:
        return render_template('voted.html', voted=True)

    if 'polls' not in session.keys():
        session['polls'] = 1
    else:
        session['polls'] += 1

    addrs.append(request.remote_addr)
    session['addrs'] = addrs

    return make_response(render_template('voted.html'))


@app.route('/pop')
def pop():
    resp = make_response(redirect(url_for('index')))

    addrs = session.setdefault('addrs', [])
    addrs.remove(request.remote_addr)
    session['addrs'] = addrs

    return resp
