from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm


class PersonalForm(FlaskForm):
    # telephone = StringField('手机', validators=[DataRequired()])
    # password1 = PasswordField('密码', validators=[DataRequired()])
    # password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo(password1)])
    # avatar = FileField('选择头像')
    # submit = SubmitField('提交')
    pass
