from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
import os
from .config import Config
from app.dashboard import dashboard
from dotenv import load_dotenv

load_dotenv()

jwt = JWTManager()
db = MongoEngine()


def create_app() -> Flask:
    """
    Initialise et configure l'application Flask avec :
    - Flask-RESTful pour l'API REST.
    - JWT (JSON Web Token) pour l'authentification sécurisée.
    - Un système de gestion de bibliothèque basé sur MongoDB.

    Configuration utilisée :
    - `SECRET_KEY`: Clé secrète utilisée pour Flask.
    - `JWT_SECRET_KEY`: Clé utilisée pour sécuriser les tokens JWT.

    Endpoints exposés :
    - **Authentification** :
        - `POST /register` : Inscription d'un nouvel utilisateur.
        - `POST /login` : Connexion et génération du token JWT.
    - **Gestion des auteurs** :
        - `GET /authors` : Récupérer tous les auteurs.
        - `GET /authors/<id>` : Récupérer un auteur spécifique.
        - `POST /authors` : Ajouter un nouvel auteur (JWT requis).
        - `DELETE /authors/<id>` : Supprimer un auteur.
    - **Gestion des livres** :
        - `GET /books` : Récupérer tous les livres.
        - `GET /books/<id>` : Récupérer un livre spécifique.
        - `POST /books` : Ajouter un livre.
        - `DELETE /books/<id>` : Supprimer un livre.
        - `GET /search/books` : Rechercher des livres par titre.
    - **Gestion des emprunts** :
        - `GET /borrow` : Récupérer tous les emprunts.
        - `GET /borrow/<id>` : Récupérer un emprunt spécifique.
        - `POST /borrow` : Enregistrer un nouvel emprunt.
        - `DELETE /borrow/<id>` : Supprimer un emprunt.
    - **Tableau de bord** :
        - `GET /dashboard` : Accéder à une interface web pour suivre les logs.

    Returns:
        Flask: Une instance de l'application Flask configurée.
    """
    app = Flask(__name__)

    # Configuration de l'application
    print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
    print(f"JWT_SECRET_KEY: {os.getenv('JWT_SECRET_KEY')}")
    print(f"MONGODB_URI: {os.getenv('MONGODB_URI')}")
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["MONGODB_SETTINGS"] = {"host": Config.MONGODB_URI}
    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)

    # Initialisation de l'API RESTful
    api = Api(app)

    # Importation des ressources API
    from .resources import AuthorResource, BookResource, BorrowResource, BookSearchResource
    from .auth import UserRegister, UserLogin

    # Ajout des endpoints à l'API
    api.add_resource(UserRegister, "/register")
    api.add_resource(UserLogin, "/login")
    api.add_resource(AuthorResource, "/authors", "/authors/<string:id>")
    api.add_resource(BookResource, "/books", "/books/<string:id>")
    api.add_resource(BorrowResource, "/borrow", "/borrow/<string:id>")
    api.add_resource(BookSearchResource, "/search/books") #search/books?titre=Les Misérables

    # Enregistrement du Blueprint pour le tableau de bord
    app.register_blueprint(dashboard, url_prefix="/dashboard")

    return app
