from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()
db_name = "database1.db"


def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'chislkfads'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    db.init_app(app)

    from .models import Candidat, Recruteur
    from .views import views 
    from .auth import auth 


    with app.app_context():
        db.create_all()


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        candidat = Candidat.query.get(id)
        if candidat:
            return candidat
        else:
            return Recruteur.query.get(id)


    return app



