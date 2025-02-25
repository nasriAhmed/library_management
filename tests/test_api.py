import pytest
from flask_jwt_extended import create_access_token
from app.app import create_app
from app.models import User, Author, Book, Borrow
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture
def client():
    """ Initialise l'application Flask pour les tests avec un contexte propre """
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        User.objects.delete()
        Author.objects.delete()
        Book.objects.delete()
        Borrow.objects.delete()

        with app.test_client() as client:
            yield client


def test_register_user(client):
    """ Test d'inscription d'un utilisateur """
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass",
        "email": "admin@example.com"
    })
    assert response.status_code == 201
    assert "Inscription réussie" in response.json["message"]


def test_login_user(client):
    """ Test de connexion d'un utilisateur """
    client.post("/register", json={
        "username": "testuser",
        "password": "testpass",
        "email": "admin@example.com"
    })
    
    response = client.post("/login", json={
        "username": "testuser",
        "password": "testpass",
        "email": "admin@example.com"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json


# GESTION DES AUTEURS
def test_create_author(client):
    """ Test d'ajout d'un auteur """
    access_token = create_access_token(identity="any")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/authors", json={
        "nom": "Victor",
        "prenom": "Hugo"
    }, headers=headers)
    
    assert response.status_code == 201
    assert "Auteur ajouté" in response.json["message"]


def test_get_authors(client):
    """ Test de récupération des auteurs """
    response = client.get("/authors")
    assert response.status_code == 200
    assert isinstance(response.json, list)


#  GESTION DES LIVRES
def test_create_book(client):
    """ Test d'ajout d'un livre """
    access_token = create_access_token(identity="any")
    headers = {"Authorization": f"Bearer {access_token}"}
    author = Author(nom="J.K.", prenom="Rowling").save()

    response = client.post("/books", json={
        "titre": "Harry Potter",
        "auteur_id": str(author.id),
        "stock": 5
    }, headers=headers)
    
    assert response.status_code == 201
    assert "Livre ajouté" in response.json["message"]


def test_get_books(client):
    """ Test de récupération des livres """
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json, list)


#  RECHERCHE DE LIVRES
def test_search_books(client):
    """ Test de recherche d'un livre """
    response = client.get("/search/books?titre=Harry")
    assert response.status_code in [200, 404]


#  GESTION DES EMPRUNTS
def test_create_borrow(client):
    """ Test d'ajout d'un emprunt """
    user = User(username="test_user", email="test@example.com", password="password").save()
    author = Author(nom="Victor", prenom="Hugo").save()
    book = Book(titre="Les Misérables", auteur=author, stock=5).save()

    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/borrow", json={
        "email": "test@example.com",
        "book_id": str(book.id)
    }, headers=headers)

    assert response.status_code == 201
    assert "Emprunt enregistré avec succès" in response.json["message"]


def test_return_borrow(client):
    """ Test du retour d'un emprunt """

    # Création d'un utilisateur si nécessaire
    user = User.objects.first()
    if not user:
        user = User(username="testuser", email="test@example.com", password="password").save()

    # Création d'un auteur si nécessaire
    auteur = Author.objects.first()
    if not auteur:
        auteur = Author(nom="Auteur", prenom="Test").save()

    # Création d'un livre avec un auteur
    book = Book.objects.first()
    if not book:
        book = Book(titre="Livre Test", auteur=auteur, stock=5).save()

    # Création de l'emprunt
    borrow = Borrow(user=user, book=book).save()
    assert borrow.id is not None, "L'emprunt n'a pas été enregistré"


# TABLEAU DE BORD (LOGS)
def test_get_dashboard_logs(client):
    """ Test de récupération des logs """
    response = client.get("/dashboard/logs")
    assert response.status_code == 200
    assert "logs" in response.json



def test_protected_route_without_token(client):
    """ Vérifie qu'un accès non authentifié échoue """
    response = client.post("/authors", json={"nom": "J.K. Rowling"})
    assert response.status_code == 401


def test_protected_route_with_token(client):
    """ Vérifie qu'un accès authentifié réussit """
    access_token = create_access_token(identity="any")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.post("/authors", json={
        "nom": "J.K. Rowling",
        "prenom": "Hugo"
    }, headers=headers)
    
    assert response.status_code == 201
