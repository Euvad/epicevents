from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User
from utils.security import hash_password, verify_password


class UserDAO:
    def __init__(self, session: Session):
        # Initialisation du DAO avec une session SQLAlchemy, permettant l'interaction avec la base de données.
        self.session = session

    def create_user(self, employee_number, name, email, password, role):
        """Create a new user with a hashed password."""
        # Hashage du mot de passe avant d'ajouter l'utilisateur à la base de données pour la sécurité
        password_hash = hash_password(password)
        user = User(
            employee_number=employee_number,
            name=name,
            email=email,
            password_hash=password_hash,
            role=role,  # Le rôle de l'utilisateur est ajouté ici
        )
        try:
            # Ajout de l'utilisateur à la session, mais la transaction n'est pas encore validée
            self.session.add(user)
            self.session.commit()  # Validation des changements dans la base de données
            return user  # Retourne l'utilisateur créé
        except IntegrityError as e:
            # Si une erreur d'intégrité se produit, comme une violation de contrainte, la transaction est annulée
            self.session.rollback()
            raise Exception(f"User creation failed: {e.orig.diag.message_detail}")
        except Exception as e:
            # Pour toutes autres erreurs non spécifiées, un rollback est effectué et l'erreur est levée
            self.session.rollback()
            raise Exception(f"Error creating user: {e}")

    def get_user_by_email(self, email) -> User:
        """Retrieve a user by their email."""
        try:
            # Recherche de l'utilisateur par son email
            return self.session.query(User).filter(User.email == email).first()
        except Exception as e:
            # Gestion des erreurs pendant la recherche de l'utilisateur
            raise Exception(f"Error retrieving user by email: {e}")

    def get_user_by_id(self, id) -> User:
        """Retrieve a user by their id."""
        try:
            # Recherche de l'utilisateur par son ID
            return self.session.query(User).filter(User.id == id).first()
        except Exception as e:
            # Gestion des erreurs pendant la recherche de l'utilisateur
            raise Exception(f"Error retrieving user by id: {e}")

    def authenticate_user(self, email, password) -> User:
        """Authenticate a user by verifying their password."""
        try:
            # Récupère l'utilisateur par son email
            user = self.get_user_by_email(email)
            if user and verify_password(user.password_hash, password):
                # Vérifie si le mot de passe fourni correspond au mot de passe hashé
                return user
            return None  # Retourne None si l'utilisateur n'existe pas ou si le mot de passe est incorrect
        except Exception as e:
            # Gestion des erreurs d'authentification
            raise Exception(f"Error authenticating user: {e}")

    def update_user(
        self,
        user_id,
        name=None,
        email=None,
        password=None,
        role=None,  # Mise à jour du rôle de l'utilisateur, si nécessaire
    ):
        """Update an existing user's information."""
        try:
            # Recherche de l'utilisateur par son ID
            user = self.session.query(User).filter(User.id == user_id).first()
            if not user:
                # Si l'utilisateur n'existe pas, une exception est levée
                raise Exception("User not found")

            # Mise à jour des informations de l'utilisateur uniquement si de nouvelles valeurs sont fournies
            if name is not None:
                user.name = name
            if email is not None:
                user.email = email
            if password is not None:
                user.password_hash = hash_password(password)  # Hashage du nouveau mot de passe
            if role is not None:
                user.role = role

            self.session.commit()  # Validation des changements dans la base de données
            return user  # Retourne l'utilisateur mis à jour
        except IntegrityError as e:
            # Si une erreur d'intégrité se produit, la transaction est annulée
            self.session.rollback()
            raise Exception(f"User update failed: {e.orig.diag.message_detail}")
        except Exception as e:
            # Pour toutes autres erreurs non spécifiées, un rollback est effectué et l'erreur est levée
            self.session.rollback()
            raise Exception(f"Error updating user: {e}")

    def delete_user(self, user_id):
        """Delete a user by their ID."""
        try:
            # Recherche de l'utilisateur par son ID
            user = self.session.query(User).filter(User.id == user_id).first()
            if not user:
                # Si l'utilisateur n'existe pas, une exception est levée
                raise Exception("User not found")

            # Suppression de l'utilisateur de la base de données
            self.session.delete(user)
            self.session.commit()  # Validation de la suppression
        except Exception as e:
            # Gestion des erreurs pendant la suppression de l'utilisateur
            self.session.rollback()
            raise Exception(f"Error deleting user: {e}")

    def get_all_users(self) -> list[User]:
        """Retrieve all users."""
        try:
            # Récupère tous les utilisateurs présents dans la base de données
            return self.session.query(User).all()
        except Exception as e:
            # Gestion des erreurs pendant la récupération de tous les utilisateurs
            raise Exception(f"Error retrieving all users: {e}")
