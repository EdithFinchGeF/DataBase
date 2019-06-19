from flask import redirect,url_for,session
import functools
from collections import namedtuple

student_info = namedtuple("student_info",["sno","sname","sex","sage","dname","dormno"])

def table_slice(table,page,pages):
    from app import app
    PAGESIZE = app.config["PAGESIZE"]
    if page > pages or table == None:
        return None
    elif page == pages:
        return table[(page-1)*PAGESIZE:]
    else :
        return table[(page-1)*PAGESIZE:page*PAGESIZE]

def required_login(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs): 
        if 'id' not in session:
            return redirect( url_for("auth.login") )
        return func(*args,**kwargs)
    return wrapper

def is_sa():
    return len(session["id"]) <= 4

def format_student(info):
    info = student_info(*(i for i in info[0]))
    return info