import click
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
import os

@app.cli.command()
def init_db():
    from .db import get_db
    with app.app_context():
        db = get_db()
        with open(os.path.join(app.root_path,"schema.sql"),encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()
    click.echo("init successfully")

@app.cli.command()
def init_passwd():
    from app.db import get_db
    default_passwd = '888888'
    passwd_hashed = generate_password_hash(default_passwd)
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        alter table student
        add column passwd varchar(50)
    ''')
    cur.execute('''
        update student 
        set passwd = ?
    ''',(passwd_hashed,))
    db.commit()

@app.cli.command()
def init_sa():
    from app.db import get_db
    default_passwd = '123456'
    passwd_hashed = generate_password_hash(default_passwd)
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        create table admins(
            id char(10) primary key,
            sname char(15),
            passwd char(256)
        )
    """)
    cur.execute('''
        insert into admins
        values('0001','张三',?)
    ''',(passwd_hashed,))
    db.commit()
    click.echo("init-sa successful")