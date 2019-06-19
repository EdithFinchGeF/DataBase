from flask import render_template,flash,redirect,request,session,url_for,jsonify,Blueprint
from app.db import check_passwd,set_passwd,test
from app.unity import required_login,is_sa

auth_bp = Blueprint('auth', __name__)



@auth_bp.route("/changePasswd",methods=["GET",'POST'])
@required_login
def change_passwd():
    if request.method == "POST":
        data = request.get_json()
        if data["new_passwd"] !=  data["comfirmed_passwd"]:
            return jsonify(error='两次输入密码不一致')
        elif check_passwd( session["id"], data["old_passwd"] ):
            set_passwd(session["id"] , data["new_passwd"] ) 
            return jsonify(message = '密码修改成功',_type='success')
        else:
            return jsonify(message = '密码不正确',_type='warning')
    return render_template('change_passwd.html')


@auth_bp.route("/login",methods = ["GET","POST"]) 
def login():
    if 'id' in session:
        return redirect(url_for('manage.index'))
    if request.method == 'POST':
        id = request.form.get("sno",None)
        passwd = request.form.get("passwd",None)
        if not(id and passwd):
            flash("密码和学号不能为空")
        if not check_passwd(id,passwd):
            flash("密码与学号不匹配")
            return render_template("auth/signin.html")
        else:
            session['id'] = id
            if is_sa():
                return redirect(url_for('manage.index'))
            else:
                return redirect(url_for('student.index'))
        
    return render_template("auth/signin.html")

@auth_bp.route("/logout",methods=["GET","POST"])
def logout():
    if 'id' in session:
        session.pop("id")
    return redirect(url_for('auth.login'))
