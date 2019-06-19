from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SelectFieldBase,SubmitField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Length
from app import app

class BaseForm(FlaskForm):
    class Meta():
        locales = ["zh"]

class LoginForm(BaseForm):
    loginUser = StringField("用户名",validators=[DataRequired("请输入用户名")])
    passwd = PasswordField("密码",validators=[DataRequired("请输入密码")])
    login = SubmitField("登陆")

class ResearchForm(BaseForm):
    keywd_sno_or_sname = StringField("学号or姓名")
    selecte_snoor_sname = SelectField("学号",choices=[("sno","学号"),("sname","姓名")])
    keywd_classname = StringField("课程名")
    research_button = SubmitField("搜索")

class ChangePasswdForm(BaseForm):
    old_passwd = PasswordField("原密码",validators=[DataRequired()])
    new_passwd = PasswordField("新密码",validators=[DataRequired()])
    new_passwd_comfirm = PasswordField("新密码确定",validators=[DataRequired(),
                                       EqualTo('new_passwd',message="两次输入密码必须相同")])
    comfirm_button = SubmitField("确定")
