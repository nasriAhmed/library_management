from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField
from datetime import datetime


class User(Document):
    """
    Modèle représentant un utilisateur dans la base de données.

    Attributs:
    - username (str) : Nom d'utilisateur unique
    - password (str) : Mot de passe (hashé)
    - email (str) : Adresse e-mail unique
    """
    username = StringField(required=True)
    password = StringField(required=True)
    email = StringField(required=True)


class Author(Document):
    """
    Modèle représentant un auteur.

    Attributs:
    - nom (str) : Nom de l'auteur
    - prenom (str) : Prénom de l'auteur
    """
    nom = StringField(required=True)
    prenom = StringField(required=True)


class Book(Document):
    """
    Modèle représentant un livre.

    Attributs:
    - titre (str) : Titre du livre
    - auteur (ReferenceField) : Référence à un auteur
    - stock (int) : Nombre d'exemplaires disponibles
    """
    titre = StringField(required=True)
    auteur = ReferenceField(Author, required=True)
    stock = IntField(default=1)


class Borrow(Document):
    """
    Modèle représentant un emprunt de livre.

    Attributs:
    - user (ReferenceField) : Utilisateur ayant emprunté le livre
    - book (ReferenceField) : Livre emprunté
    - date_emprunt (DateTime) : Date d'emprunt (par défaut, date actuelle)
    - date_retour (DateTime) : Date de retour (facultatif)
    """
    user = ReferenceField(User, required=True)
    book = ReferenceField(Book, required=True)
    date_emprunt = DateTimeField(default=datetime.utcnow)
    date_retour = DateTimeField(null=True)
