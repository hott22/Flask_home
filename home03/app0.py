from flask import Flask, render_template, request, flash, redirect, url_for
from home03.models import db, User
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from home03.form import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../instance/users.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = b'5074d1ef2b45308417ab3d3c56aed767016ebe600380b25a2fede09f2bfbb780'
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/')
def index():
    return "Hi"


@app.route('/data/')
def data():
    return 'data'


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('ok')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        name = form.user_name.data
        email = form.user_email.data
        password = form.user_password.data
        hash_ = generate_password_hash(password)
        if User.query.filter_by(email=email).first():
            flash(f'Пользователь с email: {email} уже существует', 'danger')
            return redirect(url_for('login'))
        else:
            flash(f'Пользовтель {name} успешно добавлен!', 'success')
            user = User(name=name, email=email, birthday=form.user_birthday.data, password=hash_,
                        approval=form.approval.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
