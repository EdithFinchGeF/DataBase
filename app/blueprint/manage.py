from flask import render_template,flash,redirect,request,session,url_for,jsonify,Blueprint
from app.db import (search_from_grade,check_passwd,set_passwd,
                    test,search_from_student,delete_grade,update_grade,search_from_course,add_grade,add_student,
                    update_student,delete_student,add_course,delete_course,update_course)
from app.unity import table_slice, required_login

manage_bp = Blueprint('manage',__name__)

@manage_bp.route("/manage")
@manage_bp.route("/",methods=["GET","POST"])
@required_login
def index():
    return render_template("manage/index.html")

@manage_bp.route("/searchGrade",methods = ["POST","GET"])
@required_login
def search_grade():
    if request.method == "POST":
        data = request.get_json()
        sno = data.get("sno",'')
        sname = data.get("sname",'') 
        cname = data.get("cname",'')
        page  = data.get("page",'')
        table,pages = search_from_grade(sno,sname,cname)
        table = table_slice(table,page,pages)
        if not table:
            message,_type = "查询结果不存在","warning"
        else:
            message,_type = "查询成功","success"
        return jsonify(html=render_template("_table.html",table=table),
                       pages = pages,message=message,_type=_type)
    else:
        return render_template("search_grade.html")

@manage_bp.route('/search_student',methods = ["POST","GET"])
@required_login
def search_student():
    if request.method == "POST":
        data = request.get_json()
        sno,sname,sex,dname,dormno,page = (data.get("sno",""),data.get("sname",""),
                                           data.get("sex",""),data.get("dname",""),
                                           data.get("dormno",""),data.get("page",""))
        if sex == "male":
            sex = "男"
        elif sex =="female":
            sex = "女"
        else:
            sex = ""
        table,pages= search_from_student(sno,sname,sex,dname,dormno)
        table = table_slice(table,page,pages)
        if not table:
            message,_type = "查询结果不存在","warning"
        else:
            message,_type = "查询成功","success"
        html = render_template("_table.html",table=table)
        return jsonify(html=html,message=message,_type=_type,pages=pages)
                 
    return render_template('manage/search_student.html')

'''
上面为已完成部分
表格查询结果请使用 render_template('manage/_manage_table.html',table=table)方式渲染
其中table为二维数据

学籍管理的子页面为路径 manage/manage_student.html
成绩管理的子页面的路径 manage/manage_grade.html
成绩管理的子页面的路径 manage/manage_course.html
'''


@manage_bp.route("/manage_student",methods=["POST","GET","DELETE","PUT","UPDATE"])
@required_login
def roll_management():
    data = request.get_json()
    table,_ = search_from_student()
    if request.method == 'POST':
        sno,sname,sex,dname,dormno = (data.get("sno",""),data.get("sname",""),
                                           data.get("sex",""),data.get("dname",""),
                                           data.get("dormno",""))
        if sex == "male":
            sex = "男"
        elif sex =="female":
            sex = "女"
        else:
            sex = ""
        table,pages= search_from_student(sno,sname,sex,dname,dormno)
        if not table:
            message,_type = "查询结果不存在","warning"
        else:
            message,_type = "查询成功","success"
        html = render_template("manage/_manage_table.html",table=table)
        return jsonify(html=html,message=message,_type=_type,pages=pages)
    elif request.method == 'PUT':
        sno,sname,sex,age,dname,dormno=(
            data.get("sno",""),data.get("sname",""),
            data.get("sex",""),data.get("age",""),
            data.get("dname",""),data.get("dormno","")
        )
        if sex == "male":
            sex = "男"
        elif sex == 'female':
            sex = "女"
        else :
            sex = ""
        if add_student(sno=sno,sname=sname,sex=sex,sage=age,dname=dname,dormno=dormno):
            message,_type = "成功添加","success"
        else :
            message,_type = "添加失败","warning"
        return jsonify(message = message,_type = _type)
    elif request.method == 'UPDATE':
        sno,sname,sex,age,dname,dormno = (
                                    data.get("sno",""),data.get("sname",""),
                                    data.get("sex",""),data.get("age",""),
                                    data.get("dname",""),data.get("dormno","")
                                    )
        if sex == "male":
            sex = "男"
        elif sex =="female":
            sex = "女"
        else:
            sex = ""

        if update_student(sno = sno,sname = sname,sex = sex,sage = age,dname = dname,dormno = dormno):
            message,_type = "修改成功","success"
        else :
            message,_type = "修改失败","warning"
       
        return jsonify(message = message,_type = _type) 
    elif request.method == 'DELETE':
        sno = data["sno"]
        table,_ = search_from_student(sno=sno)
        if not table:
            message,_type = "删除失败","warning"
        else:
            delete_student(sno=sno)
            message,_type = "删除成功","success"
        return jsonify(message=message,_type=_type)
        
    return render_template("manage/manage_student.html",table=table)




@manage_bp.route("/manage_student_grade",methods=["POST","GET","DELETE","PUT","UPDATE"])
@required_login
def grade_management():
    table,_=search_from_grade()
    data = request.get_json()
    if request.method == "POST":
        table,_ = search_from_grade(sno=data["sno"],sname=data["sname"],cname=data["cname"])
        html = render_template('manage/_manage_table.html',table=table)
        if html:
            message,_type = "查询成功","success"
        else:
            message,_type = "查询结果失败","warning"
        return jsonify(html=html,message=message,_type=_type)
    
    if request.method == "DELETE":
        cname,sno = data["cname"],data["sno"]
        table,_ = search_from_grade(sno=sno,cname=cname)
        if not table:
            message,_type = "删除失败","warning"
        else:
            delete_grade(cname=cname,sno=sno)
            message,_type = "删除成功","success"
        return jsonify(message=message,_type=_type)

    if request.method == "UPDATE":
        sno,cname,score = data.get("sno",""),data.get("cname",""),data.get("score","")
        table,_ = search_from_grade(sno=sno,cname=cname)
        if not table or not update_grade(sno=sno,cname=cname,score=score):
            message,_type = "更新失败","warning"
        else:
            message,_type = "更新成功","success"
        return jsonify(message=message,_type=_type)

    if request.method == "PUT":
        sno,cname,score = data.get("sno",""),data.get("cname",""),data.get("score","")
        
        table= search_from_student(sno=sno)[0] and search_from_course(cname)[0] and \
                not search_from_grade(sno=sno,cname=cname)[0] 
                   
        if table and add_grade(sno=sno,cname=cname,score=score):
            message,_type = "添加成功","success"
        else :
            message,_type = "添加成绩失败，请检测输入课程，学号是否正确，或该成绩已经存在","danger"
        return jsonify(message=message,_type=_type)
    
    return render_template("manage/manage_grade.html",table=table)

@manage_bp.route("/manage_course",methods=["POST","GET","DELETE","PUT","UPDATE"])
@required_login
def course_management():
    table,_ = search_from_course()
    data = request.get_json()
    print(data)
    if request.method == "POST":
        cno,cname = data.get("cno",""),data.get("cname","")
        table,_=search_from_course(cno,cname)
        html = render_template("manage/_manage_table.html",table=table)
        if len(html):
            message,_type = "查询成功","success"
        else:
            message,_type = "查询失败","warning"
        return jsonify(html=html,message=message,_type=_type)

    if request.method == "PUT":
        cno,cname,teacher = data.get("cno",""),data.get("cname",""),data.get("teacher","")
        if add_course(cno,cname,teacher):
            message,_type = "添加成功","success"
        else :
            message,_type = "添加失败","warning"
        return jsonify(message=message,_type=_type)

    if request.method == "UPDATE":
        cno,cname,teacher = data.get("cno",""), data.get("cname",""), data.get("teacher","")
        if update_course(cno,cname,teacher):
            message,_type = "更新成功","success"
        else :
            message,_type = "更新失败","warning"
        return jsonify(message=message,_type=_type)
    
    if request.method == "DELETE":
        cno = data.get("cno")
        if delete_course(cno):
            message,_type = "删除成功","success"
        else :
            message,_type = "删除失败","warning"
        return jsonify(message=message,_type=_type)

    return render_template("manage/manage_course.html",table=table)

