from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_login import UserMixin
from flask_marshmallow import Marshmallow
ma = Marshmallow()

###  Dados de usuário
class Pessoas(UserMixin,db.Model):
    __table_args__ = {"schema":"dados_pessoais"}

    id = db.Column('ID',db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('primeiro_nome',db.String(150))
    sobrenome = db.Column('sobrenome',db.String(150))
    bio = db.Column('informacoes',db.String(150))
    email = db.Column('email',db.String(150),unique=True)
    senha = db.Column('senha',db.String(2000))
    token = db.Column('token',db.String(150),unique=True)
    username = db.Column('username',db.String(150),unique=True)

    def __init__(self,nome,sobrenome,bio,email,senha,token,username):
        self.nome=nome
        self.sobrenome=sobrenome
        self.bio=bio
        self.email=email
        self.senha=senha
        self.token=token
        self.username=username

#Usuario jsonify

class PessoasMa(ma.Schema):
    class Meta:
        fields = ('id','nome','sobrenome','bio','email','senha','token','username')

pessoas_schem = PessoasMa()
###  Posts
class Posts(db.Model):
    __table_args__ = {"schema":"dados_pessoais"}

    id = db.Column('ID',db.Integer, primary_key=True, autoincrement = True)
    user = db.Column('user_id',db.Integer,nullable=False)
    desc = db.Column('descripition',db.String(1000),nullable=False)
    conte = db.Column('content',db.LargeBinary)
    filename = db.Column('filename',db.String(100))

    def __init__(self,user,desc,conte,filename):
        self.desc=desc
        self.user=user
        self.conte=conte
        self.filename = filename

#Posts jsonify   
class PostMa(ma.Schema):
    class Meta:
        fields = ('id','user','desc','conte','filename')

post = PostMa()
posts = PostMa(many = True)


