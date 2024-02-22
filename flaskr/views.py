from flask import Blueprint, render_template, redirect, flash, url_for, session, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

bp = Blueprint('bp',__name__,url_prefix="/")

from .db import db, Cadastrou

@bp.context_processor
def processor():

    usuario = Cadastrou.query.filter_by(token= f'{session.get('token')}',id = session.get('user_id')).first()
    usur = Cadastrou.query.filter_by(token= f'{session.get('token')}',id = session.get('user_id'))
    print(usuario,usur)
    return dict(usuario=usuario) if usuario else dict(usuario=None)

@bp.app_errorhandler(404)
def not_found(e):
    if request.query_string and b'url=' in request.query_string:
        return redirect(f'/{request.args.get('url')}')
        
    return render_template('error404.html')
    
#Inicio
@bp.route('/', methods=["GET","POST"])
def home():

    return render_template('index.html')
    
#Fim do Inicio
#Login Route

@bp.route('/login', methods=["GET","POST"])
def login():

    resp = make_response(redirect(url_for('bp.home')))
    
    if request.method == 'POST' and request.content_type == "application/x-www-form-urlencoded":
        #Cadastro

        if request.form.get('nome'):

            print('tem')

            email = Cadastrou.query.filter_by(email=f'{request.form['email']}').first()
            username = Cadastrou.query.filter_by(email=f'{request.form['username']}').first()

            if email:
                flash('Email já cadastrado')
            elif username:
                flash('Username já cadastrado')
            else:
                while True:
                    token = secrets.token_hex(16)
                    token_verify = Cadastrou.query.filter_by(token = f'{token}').first()
                    if token_verify:
                        continue
                    else:
                        break

                usuario = Cadastrou(nome = f'{request.form["nome"]}',sobrenome = f'{request.form['sobrenome']}',bio = f'{request.form['bio']}',email = f'{request.form['email']}',senha = f'{generate_password_hash(request.form['senha'])}',token = token,username = request.form['username'])
                db.session.add(usuario)
                db.session.commit()

                session.clear()
                session['user_id']=usuario.id
                session['token']=token

            return resp
        
        #Login AUTENTICATION
        else:

            usuario = Cadastrou.query.filter_by(email = f'{request.form['email']}').first()
            if usuario and check_password_hash(usuario.senha,request.form['senha']):

                while True:
                    token = secrets.token_hex(16)
                    token_verify = Cadastrou.query.filter_by(token = f'{token}').first()
                    if token_verify:
                        continue
                    else:
                        break

                usuario.token = token
                db.session.commit()

                session.clear()
                session['user_id'] = usuario.id
                session['token'] = usuario.token
                
                return resp
            else:
                flash("Email ou senha incorretos")
    
    return render_template('login.html')

#Página pra fazer login

#LOGOUT
@bp.route('/logout', methods=["GET"])
def logout():

    resp = make_response(redirect(url_for('bp.home')))

    if request:
        session.clear()
        return resp

#MENU
@bp.route("/menu.html")
def menu_load():

    resp = make_response(render_template('menu.html'))
    resp.headers['X-Frame-Options']="SAMEORIGIN"

    return resp

#Users
@bp.route('/users/<user>')
def perfil(user):

    useri = Cadastrou.query.filter_by(username = user).first()
    if useri:
        print(useri)
        return render_template('user.html',user=useri)
    else: return render_template('user.html')

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



    return render_template('configs.html')