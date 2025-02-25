# 📚 Système de Gestion de Bibliothèque avec Flask

## 🚀 Description

Ce projet est une API RESTful permettant de gérer une bibliothèque avec :

- **Gestion des auteurs** : Ajouter, modifier et supprimer des auteurs
- **Gestion des livres** : Ajouter, modifier et supprimer des livres
- **Gestion des emprunts** : Permettre aux utilisateurs d'emprunter des livres et de gérer le stock
- **Authentification JWT** : Sécurisation des accès avec JSON Web Token
- **Recherche de livres** : Endpoint permettant de retrouver un livre par son titre
- **Déploiement avec Docker & MongoDB**

---

## 📂 Structure du Projet

```
library_management/
│── app/
│   ├── app.py             # Initialisation de Flask
│   ├── models.py          # Modèles MongoEngine
│   ├── resources.py       # Endpoints API
│   ├── auth.py            # Authentification JWT
│   ├── config.py          # Connexion MongoDB
│   ├── logger.py          # Gestion des logs
│   ├── utils.py           # Fonctions utilitaires
│   └── schemas.py         # Schémas Pydantic
│   └── dashboard.py       #Tableau de bord pour voir les logs
│── templates/
│   ├── dashboard.html     #Interface du tableau de bord
│── tests/                 #Tests unitaires
│── docs/
│   ├── uml_diagram.png    # Schéma UML
│   ├── deployment.png     # Schéma de déploiement
│── logs/
│   ├── app.log            #fichier de log
│── docker-compose.yml     # Déploiement Docker
│── Dockerfile             # Image Docker pour Flask
│── requirements.txt       # Dépendances Python
│── run.py                 # Point d'entrée principal
│── README.md              # Documentation
```

---

## 🛠️ Installation et Exécution

### 📌 **1. Cloner le projet**

```bash
git clone https://github.com/nasriAhmed/library_management.git
cd library_management
```

### 📌 **2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

### 📌 **3. Lancer l'application en local**

```bash
python run.py
```

L'API sera disponible sur `http://127.0.0.1:5000`.

---

## 📦 Déploiement avec Docker

### 📌 **1. Construire et lancer l'application**

```bash
docker-compose up --build -d
```

### 📌 **2. Tester l'API avec Curl**

```bash
curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d '{"email": "admin@example.com", "username": "admin", "password": "admin"}'
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"email": "admin@example.com", "username": "admin", "password": "admin"}'
```

---

## 📋 API Endpoints

### 🔹 **Authentification**

| Méthode | Endpoint    | Description          |
| ------- | ----------- | -------------------- |
| POST    | `/register` | Créer un utilisateur |
| POST    | `/login`    | Obtenir un token JWT |

### 🔹 **Auteurs**

| Méthode | Endpoint        | Description         |
| ------- | --------------- | ------------------- |
| GET     | `/authors`      | Liste des auteurs   |
| POST    | `/authors`      | Ajouter un auteur   |
| DELETE  | `/authors/<id>` | Supprimer un auteur |

### 🔹 **Livres**

| Méthode | Endpoint                | Description         |
| ------- | ----------------------- | ------------------- |
| GET     | `/books`                | Liste des livres    |
| POST    | `/books`                | Ajouter un livre    |
| DELETE  | `/books/<id>`           | Supprimer un livre  |
| GET     | `/books/search?titre=title` | Rechercher un livre |

### 🔹 **Emprunts**

| Méthode | Endpoint  | Description        |
| ------- | --------- | ------------------ |
| GET     | `/borrow` | Liste des emprunts |
| POST    | `/borrow` | Emprunter un livre |
| DELETE  | `/borrow/<id>` | Retourner un livre |

---

## 🛠️ Tests Unitaires

Ce projet inclut **des tests Pytest** pour s'assurer du bon fonctionnement.

### 📌 **1. Installer Pytest**

```bash
pip install pytest pytest-flask
```

### 📌 **2. Exécuter les tests**

```bash
pytest tests/test_api.py --disable-warnings
```

---

## 💡 Auteur

👨‍💻 **Développé par **[**Ahmed Nasri**](https://github.com/nasriAhmed) 🚀

