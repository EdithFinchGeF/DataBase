from flask import Blueprint,render_template,request,jsonify,session
from app.unity import table_slice,required_login,format_student
from app.db import search_from_grade, search_from_student

student_bp = Blueprint('student',__name__)

@student_bp.route("/student",methods=["GET"])
def index():
    return render_template("student/index.html")

@student_bp.route("/search_grade_student",methods=["GET","POST"])
@required_login
def search_grade():
    if request.method == "POST":
        data = request.get_json()
        cname = data["cname"]
        page = data["page"]
        table,pages = search_from_grade(cname=cname)
        table = table_slice(table,page,pages)
        html = render_template("_table.html",table=table)
        if not table:
            return jsonify(html=None,message="查询结果为空",_type="warning",pages=pages)
        return jsonify(html=html,message="查询成功",_type="success",pages=pages)
        
    return render_template("student/_grade.html")

@student_bp.route("/search_student_info",methods=["GET"])
@required_login
def search_student_info():
    id = session["id"]
    info,_ = search_from_student(sno=id)
    info = format_student(info)
    return render_template("student/_student_info.html",info=info)

