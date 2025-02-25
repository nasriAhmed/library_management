import os
from dotenv import load_dotenv
from mongoengine import connect


load_dotenv()


class Config:
    """Configuration de l'application"""
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secret_key")
    MONGODB_URI = os.getenv("MONGODB_URI","mongodb://localhost:27017/library")


# Connexion MongoDB
connect(host=Config.MONGODB_URI)
