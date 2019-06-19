from flask import Flask
from config import Config
import os
import click
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin


app= Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect()
csrf.init_app(app)

def reregister_bp():
    from app.blueprint.auth import auth_bp
    from app.blueprint.student import student_bp
    from app.blueprint.manage import manage_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(manage_bp)

reregister_bp()

from . import cmd


