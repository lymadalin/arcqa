from flask import Flask, render_template, session, request, redirect, url_for, flash
import config
from models import User, Question, Answer
from excts import db
from decorators import login_required
from flask_bootstrap import Bootstrap
from myforms import PersonalForm
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
bootstrap = Bootstrap(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)



@app.route('/')
def index():
    content = {
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**content)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 一个月内不用再次登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash("用户名或密码错误，请重新输入")
            return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        telephone = request.form.get("telephone")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # 验证手机是否已经注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return "该手机已被注册，请更换！"
        else:
            # 验证两次密码输入是否一致
            if password1 != password2:
                return "两次密码输入不一致"
            else:
                user = User(telephone= telephone, username=username, password= password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # session.pop('user_id')
    session.clear()
    return redirect('login')


@app.route('/personal', methods=['GET', 'POST'])
@login_required
def personal():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    # form = PersonalForm()
    # form.telephone.data = user.telephone
    return render_template('personal.html', user=user)


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == "GET":
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question1 = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question1.author = user
        db.session.add(question1)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>', methods=['GET'])
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question = question_model)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content= content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question1 = Question.query.filter(Question.id == question_id).first()
    answer.question = question1
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    else:
        # 即使没有登录也要返回一个空字典，否则会报错
        return {}


if __name__ == '__main__':
    app.run()
