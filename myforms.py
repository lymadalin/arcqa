from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from excts import photos
from flask_pagedown.fields import PageDownField


class PersonalForm(FlaskForm):
    # telephone = StringField('手机', validators=[DataRequired()])
    # password1 = PasswordField('密码', validators=[DataRequired()])
    # password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo(password1)])
    # avatar = FileField('选择头像')
    # submit = SubmitField('提交')
    pass


class QuestionForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    body = PageDownField("内容", validators=[DataRequired()])
    submit = SubmitField('提交')


class UploadForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片！'),
        FileRequired(u'请选择一个头像吧！')], label='选择文件')
    submit = SubmitField(u'确认上传', render_kw={"class": "btn btn-primary"})
