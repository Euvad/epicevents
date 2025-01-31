import os
import shutil

AUTH_FILE = "auth.py"
TEMP_AUTH_FILE = "auth_temp.py"
BACKUP_AUTH_FILE = "auth_backup.py"

AUTH_SYSTEM_DISABLED = """
from functools import wraps
from rich.console import Console

console = Console()

def auth_required(roles=None, read_only=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            console.print("[bold yellow]WARNING: Auth system temporarily disabled![/bold yellow]")
            return f(1, *args, **kwargs)  # Simule un user_id = 1 (admin)

        return decorated_function
    return decorator
"""

def disable_auth():
    """Désactive l'authentification en remplaçant auth.py par une version debug."""
    if os.path.exists(AUTH_FILE):
        shutil.copy(AUTH_FILE, BACKUP_AUTH_FILE)  # Sauvegarde de l'auth actuelle
        with open(AUTH_FILE, "w") as f:
            f.write(AUTH_SYSTEM_DISABLED)
        print("⚠️  Authentification désactivée ! (Mode debug activé)")

def enable_auth():
    """Réactive l'authentification en restaurant auth.py."""
    if os.path.exists(BACKUP_AUTH_FILE):
        shutil.move(BACKUP_AUTH_FILE, AUTH_FILE)
        print("✅ Authentification restaurée ! (Mode sécurisé activé)")
    else:
        print("⚠️ Aucun fichier de sauvegarde trouvé, impossible de restaurer l'authentification.")

def main():
    """Permet de basculer entre auth activé et désactivé."""
    choice = input("Voulez-vous (1) Désactiver ou (2) Activer l'authentification ? [1/2]: ")
    if choice == "1":
        disable_auth()
    elif choice == "2":
        enable_auth()
    else:
        print("❌ Choix invalide. Veuillez entrer 1 ou 2.")

if __name__ == "__main__":
    main()
