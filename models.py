from excts import db
from datetime import datetime
from markdown import markdown
import bleach


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(20),nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now())
    email = db.Column(db.String(100))
    avatar = db.Column(db.String(200), default="/static/images/arcsign.png")


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text)
    # 如果用DateTime.now()返回服务器第一次运行的时间，而now返回每次提交数据库的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('questions'))

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em',
                        'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'img']
        target.content_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags,
                                                          strip=True))


db.event.listen(Question.content, 'set', Question.on_changed_content)


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    question = db.relationship('Question', backref=db.backref('answers', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))
