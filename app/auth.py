from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User


class UserRegister(Resource):
    """
    API pour l'inscription d'un utilisateur.

    Permet aux utilisateurs de s'inscrire en fournissant un `username` unique et un `password`.
    Le mot de passe est haché avant d'être stocké dans la base de données.

    Endpoints :
    - **POST `/register`** : Inscrit un nouvel utilisateur.

    Erreurs possibles :
    - 400 : Si le `username` existe déjà.
    """

    def post(self):
        """
        Inscrit un nouvel utilisateur.

        Reçoit un `username` et un `password`, vérifie si l'utilisateur existe déjà, et stocke
        les informations après hachage du mot de passe.

        Retour :
        - 201 : Succès, utilisateur créé.
        - 400 : Utilisateur déjà existant.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, help="Le nom d'utilisateur est obligatoire")
        parser.add_argument("password", required=True, help="Le mot de passe est obligatoire")
        parser.add_argument("email", required=True, help="L'adresse e-mail est obligatoire")
        args = parser.parse_args()

        # Vérifie si l'utilisateur existe déjà
        if User.objects(username=args["username"]):
            return {"message": "Utilisateur déjà existant"}, 400

        # Crée un nouvel utilisateur avec un mot de passe haché
        user = User(username=args["username"], password=generate_password_hash(args["password"]), email=args["email"])
        user.save()
        return {"message": "Inscription réussie"}, 201


class UserLogin(Resource):
    """
    API pour l'authentification d'un utilisateur.

    Permet aux utilisateurs existants de se connecter en fournissant leur `email`, `username` et `password`.
    Retourne un **token JWT** en cas de succès.

    Endpoints :
    - **POST `/login`** : Authentifie un utilisateur et génère un JWT.

    Erreurs possibles :
    - 401 : Identifiants incorrects.
    """

    def post(self):
        """
        Authentifie un utilisateur.

        Vérifie l'`email`, le `username` et le `password`, et retourne un **JWT** si les informations sont correctes.

        Retour :
        - 200 : Succès, retourne un token JWT.
        - 401 : Identifiants invalides.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="L'adresse e-mail est obligatoire")
        parser.add_argument("username", required=True, help="Le nom d'utilisateur est requis")
        parser.add_argument("password", required=True, help="Le mot de passe est requis")
        args = parser.parse_args()

        # Recherche de l'utilisateur en fonction de l'email et du username
        user = User.objects(email=args["email"], username=args["username"]).first()

        if user and check_password_hash(user.password, args["password"]):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200

        return {"message": "Identifiants invalides"}, 401
