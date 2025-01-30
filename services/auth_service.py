from dao.user_dao import UserDAO
from utils.jwt_utils import generate_jwt
import os
from database import Session
from dotenv import load_dotenv, set_key, unset_key
import json

load_dotenv(".env")


def save_token_to_file(token, filename="token.json"):
    with open(filename, "w") as file:
        json.dump({"CRM_TOKEN": token}, file)
    print("Token saved successfully.")


def load_token_from_file(filename="token.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data.get("CRM_TOKEN")
    except FileNotFoundError:
        print("No token found.")
        return None


def delete_token_file(filename="token.json"):
    import os

    if os.path.exists(filename):
        os.remove(filename)
        print("Token deleted successfully.")
    else:
        print("No token file to delete.")


def login(email, password):
    session = Session()
    user_dao = UserDAO(session)
    try:
        user = user_dao.authenticate_user(email, password)
        if not user:
            raise Exception("Invalid credentials")
        token = generate_jwt(user.id)
        print(token)
        save_token_to_file(token)
    finally:
        session.close()


def logout():
    # Remove the token from .env file
    if load_token_from_file():
        delete_token_file()
        print("Logged out successfully")
    else:
        print("No active session")
