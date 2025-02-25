from app.app import create_app, db
from app.models import Author, Book, User, Borrow
from werkzeug.security import generate_password_hash
import mongoengine

# Création de l'application Flask
app = create_app()


# Création de données de test
def seed_database():

    # Connexion à la base MongoDB
    if db is None:
        print("ERREUR: La connexion MongoDB a échoué.")
        return
    print("Connexion à MongoDB réussie.")
    # Suppression des anciennes données
    Author.objects.delete()
    Book.objects.delete()
    User.objects.delete()
    Borrow.objects.delete()

    # Création des auteurs
    authors = [
        Author(nom="Victor", prenom="Hugo").save(),
        Author(nom="J.K.", prenom="Rowling").save(),
        Author(nom="George", prenom="Orwell").save()
    ]
    
    print(f" {len(authors)} auteurs ajoutés ")

    # Création des livres
    books = [
        Book(titre="Les Misérables", auteur=authors[0], stock=5).save(),
        Book(titre="Harry Potter", auteur=authors[1], stock=10).save(),
        Book(titre="1984", auteur=authors[2], stock=7).save()
    ]
    
    print(f"📖 {len(books)} livres ajoutés ")

    # Création des utilisateurs
    users = [
        User(username="admin_nasri", password=generate_password_hash("admin123"),email="admin@example.com").save(),
        User(username="user1_nasri", password=generate_password_hash("password"),email="user1@example.com").save()
    ]
    print(f" {len(users)} utilisateurs ajoutés ")

    print(" Base de données initialisée avec succès ! ")


# Exécution du script
if __name__ == "__main__":
    with app.app_context():
        seed_database()
