import pytest
from pydantic import ValidationError
from app.schemas import UserSchema, AuthorSchema, BookSchema, BorrowSchema

# ✅ TESTS POUR UserSchema
def test_valid_user_schema():
    """ Teste un utilisateur valide """
    user = UserSchema(username="testuser", password="SecurePass123", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_invalid_user_schema():
    """ Vérifie qu'un email invalide lève une erreur """
    with pytest.raises(ValidationError):
        UserSchema(username="testuser", password="SecurePass123", email="invalid-email")

# ✅ TESTS POUR AuthorSchema
def test_valid_author_schema():
    """ Teste un auteur valide """
    author = AuthorSchema(nom="Victor", prenom="Hugo")
    assert author.nom == "Victor"
    assert author.prenom == "Hugo"

def test_invalid_author_schema():
    """ Vérifie qu'un auteur sans nom ou prénom lève une erreur """
    with pytest.raises(ValidationError):
        AuthorSchema(nom="Victor")  # Manque 'prenom'

# ✅ TESTS POUR BookSchema
def test_valid_book_schema():
    """ Teste un livre valide """
    book = BookSchema(titre="Les Misérables", auteur_id="60d5f9f9e13b3f001c5d9e01", stock=10)
    assert book.titre == "Les Misérables"
    assert book.stock == 10

def test_invalid_book_schema():
    """ Vérifie qu'un stock négatif lève une erreur """
    with pytest.raises(ValidationError):
        BookSchema(titre="Les Misérables", auteur_id="60d5f9f9e13b3f001c5d9e01", stock=-1)  # ✅ Va lever une erreur

# ✅ TESTS POUR BorrowSchema
def test_valid_borrow_schema():
    """ Teste un emprunt valide """
    borrow = BorrowSchema(user_id="60d5f9f9e13b3f001c5d9e02", book_id="60d5f9f9e13b3f001c5d9e03", date_emprunt="2025-03-01")
    assert borrow.user_id == "60d5f9f9e13b3f001c5d9e02"

def test_invalid_borrow_schema():
    """ Vérifie qu'un emprunt sans date_emprunt lève une erreur """
    with pytest.raises(ValidationError):
        BorrowSchema(user_id="60d5f9f9e13b3f001c5d9e02", book_id="60d5f9f9e13b3f001c5d9e03")
