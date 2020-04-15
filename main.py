from flask import Flask, render_template, redirect
from data.loginform import LoginForm
from data import db_session
from flask_login import login_user, current_user, login_required
from data.users import User
from data.registerform import RegisterForm
from data.jobsform import JobsForm
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")  # Направляем на страницу с отображением списка работ
        #  Если ввели неверный логин или пароль
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        print(None)
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/jobs',  methods=['GET', 'POST'])
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        jobs = Jobs()
        jobs.job_title = form.job_title.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        jobs.team_leader_id = form.team_leader_id.data
        db_session.global_init("db/test.sqlite")
        session = db_session.create_session()
        session.add(jobs)
        session.commit()
        return redirect('/jobs')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
