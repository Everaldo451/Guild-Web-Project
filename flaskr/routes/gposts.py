from flask import Blueprint, redirect, url_for, make_response, request
from ..models.models import db,Posts,Pessoas
from sqlalchemy import desc
from flask import jsonify

gp = Blueprint('gp',__name__,url_prefix="/gp")

@gp.route('/getposts',methods=["GET"])
def getposts():
    if request.query_string:
        username = request.args.get('username')
        f = request.args.get('f')
        print(username,f)

        user = Pessoas.query.filter_by(username=username).first()
        posts = Posts.query.filter_by(user=user.id).order_by(desc(Posts.id)).offset(int(f)).limit(3).all()

        return jsonify(posts)
    
    else: return make_response(redirect(url_for('bp.home')))