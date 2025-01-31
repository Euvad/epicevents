from dao.user_dao import UserDAO
from utils.jwt_utils import generate_jwt
import os
from database import Session
from dotenv import load_dotenv, set_key, unset_key
import json

# Charge les variables d'environnement depuis le fichier .env
load_dotenv(".env")


def save_token_to_file(token, filename="token.json"):
    """Save the JWT token to a file."""
    with open(filename, "w") as file:
        # Sauvegarde le token JWT dans un fichier JSON
        json.dump({"CRM_TOKEN": token}, file)
    print("Token saved successfully.")  # Confirmation que le token a été sauvegardé


def load_token_from_file(filename="token.json"):
    """Load the JWT token from a file."""
    try:
        # Tente de charger le token depuis le fichier JSON
        with open(filename, "r") as file:
            data = json.load(file)
            return data.get("CRM_TOKEN")
    except FileNotFoundError:
        # Si le fichier n'existe pas, un message est affiché
        print("No token found.")
        return None


def delete_token_file(filename="token.json"):
    """Delete the token file."""
    import os

    if os.path.exists(filename):
        # Si le fichier existe, le supprimer
        os.remove(filename)
        print("Token deleted successfully.")  # Confirmation de la suppression
    else:
        # Si le fichier n'existe pas, afficher un message
        print("No token file to delete.")


def login(email, password):
    """Authenticate the user and generate a JWT token."""
    session = Session()  # Crée une session avec la base de données
    user_dao = UserDAO(session)  # Initialise le DAO de l'utilisateur avec la session
    try:
        # Authentifie l'utilisateur avec son email et mot de passe
        user = user_dao.authenticate_user(email, password)
        if not user:
            raise Exception("Invalid credentials")  # Si les informations sont invalides, lever une exception

        # Génère un token JWT pour l'utilisateur authentifié
        token = generate_jwt(user.id)
        print(token)  # Affiche le token généré
        save_token_to_file(token)  # Sauvegarde le token dans un fichier
    finally:
        # Toujours fermer la session après l'authentification
        session.close()


def logout():
    """Log out the user by deleting the JWT token."""
    # Vérifie si un token existe dans le fichier
    if load_token_from_file():
        delete_token_file()  # Supprime le fichier du token
        print("Logged out successfully")  # Confirme que la déconnexion a réussi
    else:
        # Si aucun token n'est trouvé, affiche un message indiquant qu'aucune session active n'existe
        print("No active session")
