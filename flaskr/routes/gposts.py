from flask import Blueprint, redirect, url_for, make_response, request, jsonify
from ..models.models import db,Posts,Pessoas,posts,post
from sqlalchemy import desc
import base64

gp = Blueprint('gp',__name__,url_prefix="/gp")

@gp.route('/getposts',methods=["GET"])
def getposts():
    if request.query_string:
        print(request)
        username = request.args.get('username')
        f = request.args.get('f')

        user = Pessoas.query.filter_by(username=username).first()
        poste = Posts.query.filter_by(user=user.id).order_by(desc(Posts.id)).offset(int(f)).limit(3).all()
        if len(poste) == 1:
            poste = Posts.query.filter_by(user=user.id).order_by(desc(Posts.id)).offset(int(f)).first()
            return jsonify({"post" : post.dump(poste) , "username": request.args.get('username'), "message" : "1"})
        elif len(poste) > 1:
            return jsonify({"post" : posts.dump(poste), "username" : request.args.get('username'), "message" : "2"})

        elif len(poste) == 0:
            return jsonify({"message":"0"})
    
    else: return make_response(redirect(url_for('bp.home')))