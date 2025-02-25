from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError, DoesNotExist
from app.models import Author, Book, Borrow, User
from app.logger import setup_logger
from app.utils import serialize_doc

logger = setup_logger()


class AuthorResource(Resource):
    """
    API REST pour la gestion des auteurs.
    - GET: Récupérer la liste des auteurs ou un auteur spécifique.
    - POST: Ajouter un nouvel auteur (JWT requis).
    - DELETE: Supprimer un auteur par ID.
    """

    def get(self, id=None):
        """ Récupère un ou plusieurs auteurs """
        try:
            if id:
                author = Author.objects.get(id=id)
                logger.info(f"Auteur récupéré: {author.nom} {author.prenom}")
                return jsonify(serialize_doc(author))
            authors = Author.objects.all()
            logger.info(f"Nombre d'auteurs récupérés: {len(authors)}")
            return jsonify(serialize_doc(authors))
        except DoesNotExist:
            logger.warning(f"Auteur avec ID {id} non trouvé.")
            return {"message": "Auteur non trouvé"}, 404
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des auteurs: {str(e)}")
            return {"message": "Erreur serveur"}, 500

    @jwt_required()
    def post(self):
        """ Ajoute un nouvel auteur """
        parser = reqparse.RequestParser()
        parser.add_argument("nom", required=True, help="Le nom est obligatoire")
        parser.add_argument("prenom", required=True, help="Le prénom est obligatoire")
        args = parser.parse_args()

        try:
            author = Author(nom=args["nom"], prenom=args["prenom"])
            author.save()
            logger.info(f"Auteur ajouté: {author.nom} {author.prenom}")
            return {"message": "Auteur ajouté", "id": str(author.id)}, 201
        except ValidationError as e:
            logger.error(f"Erreur de validation: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'un auteur: {str(e)}")
            return {"message": "Erreur serveur"}, 500

    @jwt_required()
    def delete(self, id):
        """ Supprimer un auteur """
        try:
            author = Author.objects.get(id=id)
            author.delete()
            logger.info(f"Auteur supprimé: {id}")
            return {"message": "Auteur supprimé"}, 200
        except DoesNotExist:
            logger.warning(f"Auteur avec ID {id} non trouvé.")
            return {"message": "Auteur non trouvé"}, 404
        except Exception as e:
            logger.error(f"Erreur lors de la suppression d'un auteur: {str(e)}")
            return {"message": "Erreur serveur"}, 500


class BookResource(Resource):
    """
    API REST pour la gestion des livres.
    - GET: Récupérer la liste des livres ou un livre spécifique.
    - POST: Ajouter un nouveau livre.
    - DELETE: Supprimer un livre par ID.
    """

    def get(self, id=None):
        """ Récupère un ou plusieurs livres """
        try:
            if id:
                book = Book.objects.get(id=id)
                logger.info(f"Livre récupéré: {book.titre}")
                return jsonify(serialize_doc(book))
            books = Book.objects.all()
            logger.info(f"Nombre de livres récupérés: {len(books)}")
            return jsonify(serialize_doc(books))
        except DoesNotExist:
            logger.warning(f"Livre avec ID {id} non trouvé.")
            return {"message": "Livre non trouvé"}, 404
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des livres: {str(e)}")
            return {"message": "Erreur serveur"}, 500

    @jwt_required()
    def post(self):
        """ Ajoute un nouveau livre """
        parser = reqparse.RequestParser()
        parser.add_argument("titre", required=True, help="Le titre est obligatoire")
        parser.add_argument("auteur_id", required=True, help="L'ID de l'auteur est obligatoire")
        parser.add_argument("stock", type=int, required=True, help="Le stock est obligatoire")
        args = parser.parse_args()

        try:
            auteur = Author.objects.get(id=args["auteur_id"])
            book = Book(titre=args["titre"], auteur=auteur, stock=args["stock"])
            book.save()
            logger.info(f"Livre ajouté: {book.titre}")
            return {"message": "Livre ajouté", "id": str(book.id)}, 201
        except DoesNotExist:
            logger.warning(f"Auteur avec ID {args['auteur_id']} non trouvé.")
            return {"message": "Auteur non trouvé"}, 404
        except ValidationError as e:
            logger.error(f"Erreur de validation: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout d'un livre: {str(e)}")
            return {"message": "Erreur serveur"}, 500

    @jwt_required()
    def delete(self, id):
        """ Supprime un livre """
        try:
            book = Book.objects.get(id=id)
            book.delete()
            logger.info(f"Livre supprimé: {id}")
            return {"message": "Livre supprimé"}, 200
        except DoesNotExist:
            logger.warning(f"Livre avec ID {id} non trouvé.")
            return {"message": "Livre non trouvé"}, 404
        except Exception as e:
            logger.error(f"Erreur lors de la suppression d'un livre: {str(e)}")
            return {"message": "Erreur serveur"}, 500


class BorrowResource(Resource):
    """
    API REST pour la gestion des emprunts.
    - GET: Récupérer la liste des emprunts ou un emprunt spécifique.
    - POST: Ajouter un nouvel emprunt (Vérifie la disponibilité du livre).
    - DELETE: Supprimer un emprunt (Retour du livre en stock).
    """

    def get(self, id=None):
        """ 
        Récupère un ou plusieurs emprunts. 

        - Si `id` est fourni, retourne l'emprunt correspondant.
        - Sinon, retourne la liste de tous les emprunts enregistrés.
        """
        try:
            if id:
                borrow = Borrow.objects.get(id=id)
                logger.info(f"Emprunt récupéré: {borrow.id}")
                return jsonify(serialize_doc(borrow))

            all_borrows = Borrow.objects.all()
            logger.info(f"Nombre d'emprunts récupérés: {len(all_borrows)}")
            return jsonify(serialize_doc(all_borrows))
        except DoesNotExist:
            logger.warning(f"Emprunt avec ID {id} non trouvé.")
            return {"message": "Emprunt non trouvé"}, 404
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des emprunts: {str(e)}")
            return {"message": "Erreur serveur"}, 500

    @jwt_required()
    def post(self):
        """
        Permet à un utilisateur d'emprunter un livre.

        **Requête :**
        ```json
        {
            "email": "user@example.com",
            "book_id": "65ab13df..."
        }
        ```

        **JWT Requis** : L'utilisateur doit être authentifié.

        **Réponse :**
        - `201` : Emprunt enregistré avec succès.
        - `400` : Validation incorrecte.
        - `404` : Utilisateur ou livre introuvable.
        - `500` : Erreur serveur.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, help="L'email de l'utilisateur est obligatoire")
        parser.add_argument("book_id", required=True, help="L'ID du livre est obligatoire")
        args = parser.parse_args()

        try:
            # Recherche de l'utilisateur par e-mail
            user = User.objects(email=args["email"]).first()
            if not user:
                logger.warning(f"Utilisateur avec email {args['email']} non trouvé.")
                return {"message": "Utilisateur non trouvé"}, 404

            # Recherche du livre par ID
            book = Book.objects.get(id=args["book_id"])
            if book.stock <= 0:
                logger.warning(f"Livre '{book.titre}' non disponible en stock.")
                return {"message": "Livre non disponible"}, 400

            # Création de l'emprunt
            borrow = Borrow(user=user, book=book)
            borrow.save()

            # Mise à jour du stock
            book.stock -= 1
            book.save()

            logger.info(f"📖 Emprunt ajouté : {borrow.id} (Utilisateur: {user.email}, Livre: {book.titre})")
            return {"message": "Emprunt enregistré avec succès", "borrow_id": str(borrow.id)}, 201

        except DoesNotExist:
            logger.error("Utilisateur ou livre non trouvé.")
            return {"message": "Utilisateur ou livre non trouvé"}, 404
        except ValidationError as e:
            logger.error(f"Erreur de validation : {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Erreur lors de l'emprunt : {str(e)}")
            return {"message": "Erreur serveur"}, 500

    @jwt_required()
    def delete(self, id):
        """ Supprime un emprunt (Retourne le livre en stock) """
        try:
            borrow = Borrow.objects.get(id=id)
            book = borrow.book

            # Réincrémenter le stock du livre
            book.stock += 1
            book.save()

            borrow.delete()
            return {"message": "Emprunt supprimé et livre retourné"}, 200
        except DoesNotExist:
            return {"message": "Emprunt non trouvé"}, 404

  
class BookSearchResource(Resource):
    """
    API REST pour la recherche de livres par titre.
    """

    def get(self):
        """
        Recherche des livres uniquement par **titre**.

        **Requête :**
        ```json
        {
            "titre": "Harry Potter"
        }
        ```

        **Réponse :**
        - `200` : Liste des livres correspondants.
        - `404` : Aucun livre trouvé.
        - `400` : Erreur de validation.
        - `500` : Erreur serveur.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("titre", type=str, location="args", required=True, help="Le titre est obligatoire pour la recherche")
        args = parser.parse_args()

        try:
            books = Book.objects(titre__icontains=args["titre"])  # Recherche insensible à la casse
            
            if books:
                logger.info(f"{len(books)} livre(s) trouvé(s) pour le titre '{args['titre']}'")
                return jsonify(serialize_doc(books))

            logger.warning(f"Aucun livre trouvé pour le titre '{args['titre']}'")
            return {"message": "Aucun livre trouvé"}, 404

        except ValidationError as e:
            logger.error(f"Erreur de validation: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des livres: {str(e)}")
            return {"message": "Erreur serveur"}, 500