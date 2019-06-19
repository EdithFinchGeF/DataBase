# coding=utf-8
import sqlite3
from flask import g,session,request
import os
import click
from collections import namedtuple
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import math
from app import app
from app.unity import is_sa

DATABASE = app.config["DATABASE"]
PAGESIZE = app.config["PAGESIZE"]
SQL_search_from_grade = """
        select S.Sno,Sname,C.Cname,G.Score
        from Student S,Grade G,Course C
        where S.Sno = G.Sno
        and   G.Cno = C.Cno
        and   S.sno like ?
        and   S.sname like ?
        and   C.Cname like ?
"""

SQL_search_from_student="""
    select S.sno,S.sname,S.Sex,S.sage,D.dname,S.dormno
    from Student S,Department D
    where S.dno = D.dno
    and S.sno like ? 
    and S.sname like ?
    and Sex like ?
    and D.dname like ?
    and S.dormno like ?
"""


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

def add_wild_card(card):
    """
    添加通配符，用于模糊搜索
    """
    return '%'+str(card)+'%'

def table_format(table):
    """
    将数据简单格式化
    输入为表格数据
    """
    table=[ [i for i in row ]  for row in table]
    return table



@app.teardown_request
def close_db(* args):
    '''
    用户退出后自动关闭数据库连接
    '''
    db = g.pop('db', None)
    if db is not None:
        db.close()



def search(SQL:str,*args) -> list:
    """
    执行SQL语句查询的基础功能函数，
    第一个参数为SQL语句,第二个参数为SQL语句需要填充的变量
    """
    db = get_db()
    cur = db.cursor()
    cur.execute(SQL,args)
    table = table_format(cur.fetchall())
    return table

def search_from_grade(sno='' , sname='' , cname='') ->(list,int):
    """
    查询成绩，当某一参数为空时，表示该条件不受限
    返回值为table和页数
    """
    table = None
    if is_sa(): ## 判断是否为管理员（老师），保证学生只能查到自己的成绩
        sno = add_wild_card(sno)
    else:
        sno = session['id']
    sname = add_wild_card(sname)
    cname = add_wild_card(cname)
    table = search(SQL_search_from_grade,sno , sname,cname)
    pages = math.ceil(len(table) / PAGESIZE)
    return table,pages

def search_from_student(sno='',sname='',sex='',dname='',dormno=''):
    """
    查询学生信息，当某一参数为空时，表示该条件不受限
    返回值为table和页数
    """
    table = None
    if is_sa(): ## 判断是否为管理员，保证学生只能查到自己的信息
        sno = add_wild_card(sno)
    else:
        sno = session['id']
    sname = add_wild_card(sname)
    sex = add_wild_card(sex)
    dname = add_wild_card(dname)
    dormno = add_wild_card(dormno)

    table = search(SQL_search_from_student,sno , sname,sex,dname,dormno)
    pages = math.ceil(len(table) / PAGESIZE)
    return table,pages



def test():
    """
    用于测试，测试后遗留
    """
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        select S.Sno,Sname,C.Cname,G.Score
        from Student S,Grade G,Course C
        where S.Sno = G.Sno
        and   G.Cno = C.Cno
        and   S.Sno like ?
    ''',['%9%',])

    table=table_format(cur.fetchall())
    return table

raw_checked_sql = '''
        select passwd,sname
        from %s
        where %s = ?
    '''

def check_passwd(id,passwd_raw):
    """
    检测密码是否正确
    返回值为bool
    """
    if len(id)<=4: 
        sql=raw_checked_sql%('admins','id')
    else:
        sql=raw_checked_sql%('student','sno')
    db = get_db()
    cur = db.cursor()
    cur.execute(sql,(id,))
    res = cur.fetchone()
    if res is None:
        return False ## 用户id错误
    passwd_hashed,name = res ##注意fetchone返回值为list
    session["username"] = name
    print(session)
    return check_password_hash(passwd_hashed,passwd_raw)

raw_set_passwd = '''
        update %s
        set passwd = ?
        where %s = ?
    '''
def set_passwd(id,passwd):
    """
    设置密码
    id参数为用户id，passwd为新密码
    """
    db = get_db()
    cur = db.cursor()
    passwd_hashed = generate_password_hash(passwd)
    if len(id) <=4:
        sql = raw_set_passwd%('admins','id')
    else:
        sql = raw_set_passwd%('student','sno')
    cur.execute('''
        update student
        set passwd = ?
        where sno = ?
    ''',(passwd_hashed,id,))
    db.commit()

def execute_sql(SQL,*args) -> None:
    db = get_db()
    cur = db.cursor()
    res = True
    try:
        cur.execute(SQL,args)
    except:
        res = False
    finally:
        db.commit()
        return res

def delete_grade(sno,cname):
    del_grade_sql = """
        delete
        from grade
        where sno = ?
        and   cno = (
            select cno
            from course
            where cname = ?
        )
    """
    execute_sql(del_grade_sql,sno,cname)

def update_grade(sno,cname,score):
    update_grade_sql = """
        update
        grade 
        set score = ?
        where sno = ?
        and   cno = (
            select cno
            from course
            where cname = ?
        )
    """
    score = int(score)
    return execute_sql(update_grade_sql,score,sno,cname)

def search_from_course(cno):
    search_course_sql = """
        select *
        from course
        where cname = ?
    """
    table = search(search_course_sql,cno)
    pages = math.ceil(len(table) / PAGESIZE)
    return table,pages

def add_grade(sno,cname,score):
    add_grade_sql="""
        insert into
        grade(sno,cno,score)
        values(?,(
            select cno
            from course
            where cname = ?
        ),?)
    """
    return execute_sql(add_grade_sql,sno,cname,score)