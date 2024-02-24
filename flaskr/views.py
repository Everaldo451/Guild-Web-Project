from flask import Blueprint, render_template, redirect, flash, url_for, session, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import Authorization
import secrets
from functools import wraps

bp = Blueprint('bp',__name__,url_prefix="/")

from .db import db, Cadastrou

@bp.before_app_request
def reque():
    
    if request.form and (str(request.url_rule) == "/login" or str(request.url_rule) == "/cadastro"):
        request.authorization=Authorization('digest',request.form,secrets.token_hex(16))

#AFTER REQUEST -> Acrescenta cabeçalhos
@bp.after_app_request
def resp(response):
    if response.mimetype == "text/html":
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Content-Security-Policy"] = "connect src 'self'"
    return response

#Acrescenta o usuário ao JINJA
@bp.context_processor
def processor():

    usuario = Cadastrou.query.filter_by(token= f'{session.get('token')}',id = session.get('user_id')).first()
    
    return dict(usuario=usuario) if usuario else dict(usuario=None)


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
    
#Página pra fazer login

@bp.route('/auth', methods=["GET","POST"])
def auth():
    
    return make_response(render_template('login.html'))

#LOGIN
@bp.route('/login',methods=["POST"])
def login():

    if request.authorization:
        form = request.authorization.parameters
        

    resp = make_response(redirect(url_for("bp.home")))

    usuario = Cadastrou.query.filter_by(email = f'{form['email']}').first()
    if usuario and check_password_hash(usuario.senha,form['senha']):
        
        token = secrets.token_hex(16)

        usuario.token = token
        db.session.commit()

        session.clear()
        session['user_id'] = usuario.id
        session['token'] = usuario.token
                
        return resp
    else:
        flash("Email ou senha incorretos")


#CADASTRO
@bp.route('/cadastro',methods=["POST"])
def cadastro():

    email = Cadastrou.query.filter_by(email=f'{request.form['email']}').first()
    username = Cadastrou.query.filter_by(email=f'{request.form['username']}').first()

    if email:
        flash('Email já cadastrado')
    elif username:
        flash('Username já cadastrado')
    else:
        token = secrets.token_hex(16)

        usuario = Cadastrou(nome = f'{request.form["nome"]}',sobrenome = f'{request.form['sobrenome']}',bio = f'{request.form['bio']}',email = f'{request.form['email']}',senha = f'{generate_password_hash(request.form['senha'])}',token = token,username = request.form['username'])
        db.session.add(usuario)
        db.session.commit()

        session.clear()
        session['user_id']=usuario.id
        session['token']=token

        return make_response(redirect(url_for('bp.home')))

#LOGOUT
@bp.route('/logout', methods=["GET"])
def logout():

    if request:
        session.clear()
        return make_response(redirect(url_for('bp.home')))

#MENU
@bp.route("/menu.html")
def menu_load():

    return make_response(render_template('menu.html'))

#Users
@bp.route('/users/<user>')

def perfil(user):

    useri = Cadastrou.query.filter_by(username = user).first()

    if useri:
        return make_response(render_template('user.html',user=useri))
    else:  
        return make_response(render_template('user.html'))

#User configs
@bp.route('/configs',methods=["GET","POST"])
def configs():

    if request.method=="POST" and request.content_type == "application/x-www-form-urlencoded":
        user = Cadastrou.query.filter_by(token=session.get('token'),id=session.get('user_id')).first()
        user.nome = request.form.get('nome')
        user.sobrenome = request.form.get('sobrenome')
        username = Cadastrou.query.filter_by(username=request.form.get('username')).first()
        if not username:
            user.username = request.form.get('username')
        if request.form.get('senha'):
            user.senha = generate_password_hash(request.form.get('senha'))      
        db.session.commit()
        return redirect(url_for('bp.home'))

    return make_response(render_template('configs.html'))