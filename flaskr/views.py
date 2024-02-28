from flask import Blueprint, render_template, redirect, flash, url_for, session, make_response, request
from werkzeug.security import generate_password_hash
from flask_login import login_required
from sqlalchemy import desc
import re
import base64

bp = Blueprint('bp',__name__,url_prefix="/")

from .models import db, Pessoas, Posts

#AFTER REQUEST -> Acrescenta cabeçalhos
@bp.after_app_request
def resp(response):
    if response.mimetype == "text/html":
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Content-Security-Policy"] = f"script-src 'self'"
    return response

#Apesar de não estar presente, o context processor serve para colocar variáveis dentro do jinja antes da página
#ser carregada. Serve inclusive para fazer login, mas é melhor usar Flask-Login

#Erro de página não encontrada
@bp.app_errorhandler(404)
def not_found(e):
    if request.query_string and b'url=' in request.query_string:
        return redirect(f'/{request.args.get('url')}')
    
        
    return make_response(render_template('error404.html'))
    
#Inicio
@bp.route('/', methods=["GET","POST"])
def home():
    
    return make_response(render_template('index.html'))
#MENU
@bp.route("/menu.html")
def menu_load():

    return make_response(render_template('menu.html'))

#Users
@bp.route('/users/<user>',methods=["GET","POST"])
def perfil(user):

    if request.method=="POST" and request.form:

        usuario = Pessoas.query.filter_by(id=int(session.get('_user_id'))).first()
        mydesc = f'<t>{request.form.get('title')}<t><e>{request.form.get('desc')}'
        if not request.files['content']:
            print('oi')
            post = Posts(user=usuario.id,desc=mydesc,conte=None,filename=None)
        else:
            file = request.files['content'].stream
            post = Posts(user=usuario.id,desc=mydesc,conte=file.read(),filename=request.files['content'].filename)
        db.session.add(post)
        db.session.commit()
        return make_response(redirect(f'{usuario.username}'))

    useri = Pessoas.query.filter_by(username = user).first()

    if useri:
        print(str(base64.b64encode(b'oi')))
        posts = Posts.query.filter_by(user=useri.id).order_by(desc(Posts.id)).limit(3).all()
        print(posts)
        return make_response(render_template('user.html',user=useri,posts=posts,re=re,len=len,str=str,base64=base64))
    else:  
        return make_response(render_template('user.html'))

#User configs
@bp.route('/configs',methods=["GET","POST"])
@login_required
def configs():

    if request.method=="POST" and request.content_type == "application/x-www-form-urlencoded":
        user = Pessoas.query.filter_by(token=session.get('token'),id=session.get('user_id')).first()
        user.nome = request.form.get('nome')
        user.sobrenome = request.form.get('sobrenome')
        username = Pessoas.query.filter_by(username=request.form.get('username')).first()
        if not username:
            user.username = request.form.get('username')
        if request.form.get('senha'):
            user.senha = generate_password_hash(request.form.get('senha'))      
        db.session.commit()
        return redirect(url_for('bp.home'))

    return make_response(render_template('configs.html'))