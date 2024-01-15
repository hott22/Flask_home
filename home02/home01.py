from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/authorization/')
def authorization():
    response = make_response(render_template('hello.html', name=request.form.get('user_name')))
    response.set_cookie('name', request.form.get('user_name'))
    response.set_cookie('email', request.form.get('user_email'))
    return response


@app.post('/del_cookie/')
def del_cookie():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('name')
    response.delete_cookie('email')
    return response


@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
