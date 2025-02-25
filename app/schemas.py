from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):
    """
    Schéma de validation pour un utilisateur.
    """
    username: str
    password: str
    email: EmailStr


class AuthorSchema(BaseModel):
    """
    Schéma de validation pour un auteur.
    """
    nom: str
    prenom: str


class BookSchema(BaseModel):
    """
    Schéma de validation pour un livre.
    """
    titre: str
    auteur_id: str
    stock: int


class BorrowSchema(BaseModel):
    """
    Schéma de validation pour un emprunt.
    """
    user_id: str
    book_id: str
    date_emprunt: str
    date_retour: Optional[str] = None
