from flask import Blueprint, request, render_template, make_response, flash, url_for, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import Authorization
import secrets
from flask_login import LoginManager, login_user,logout_user
from flask import json
import base64
import hashlib

login_manager = LoginManager()
login_manager.session_protection='strong'

from ..models.models import db,Pessoas

auth = Blueprint('auth',__name__,url_prefix="/auth")

@login_manager.user_loader
def user_loader(id):
    return Pessoas.query.filter_by(id=int(id)).first()

@login_manager.unauthorized_handler
def unauthorized():
    return "não pode não"

@auth.before_app_request
def reque():
    if request.form and (str(request.url_rule) == "/auth/login" or str(request.url_rule) == "/auth/cadastro"):
        request.authorization=Authorization('digest',request.form,secrets.token_hex(16))
#AUTH
@auth.route('/', methods=["GET","POST"])
def authentication():
    
    return make_response(render_template('login.html'))
#LOGIN

@auth.route('/login',methods=["POST"])
def login():

    if request.authorization:
        form = request.authorization.parameters
        #print(base64.b64encode(str.encode(json.dumps(request.form))))
    else:
        flash("No authorization")
        return make_response(redirect(url_for('auth.authentication')))

    resp = make_response(redirect(url_for("bp.home")))

    usuario = Pessoas.query.filter_by(email = f'{form['email']}').first()
    if usuario and check_password_hash(usuario.senha,form['senha']):

        while True:
            token = secrets.token_hex(16)
            tokenverify = Pessoas.query.filter_by(token=token).first()
            if tokenverify:
                continue
            else:
                break

        usuario.token = token
        db.session.commit()

        login_user(usuario)
        #session.clear()
        #session['user_id'] = usuario.id
        #session['token'] = usuario.token
                
        return resp
    else:
        flash("Email ou senha incorretos")
        return make_response(redirect(url_for('auth.authentication')))

#CADASTRO
@auth.route('/cadastro',methods=["POST"])
def cadastro():

    if request.authorization:
        form = request.authorization.parameters
    else:
        flash("No authorization")
        return make_response(redirect(url_for('auth.authentication')))

    email = Pessoas.query.filter_by(email=f'{form['email']}').first()
    username = Pessoas.query.filter_by(email=f'{form['username']}').first()

    if email:
        flash('Email já cadastrado')
        return make_response(redirect(url_for('auth.authentication')))
    elif username:
        flash('Username já cadastrado')
        return make_response(redirect(url_for('auth.authentication')))
    else:
        while True:
            token = secrets.token_hex(16)
            tokenverify = Pessoas.query.filter_by(token=token).first()
            if tokenverify:
                continue
            else:
                break

        usuario = Pessoas(nome = f'{form["nome"]}',sobrenome = f'{form['sobrenome']}',bio = f'{form['bio']}',email = f'{form['email']}',senha = f'{generate_password_hash(form['senha'])}',token = token,username = f'{form['username']}')
        db.session.add(usuario)
        db.session.commit()

        login_user(usuario)
        #session.clear()
        #session['user_id']=usuario.id
        #session['token']=token

        return make_response(redirect(url_for('bp.home')))

#LOGOUT
@auth.route('/logout', methods=["GET"])
def logout():

    if request:
        logout_user()
        return make_response(redirect(url_for('bp.home')))




