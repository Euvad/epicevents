from functools import wraps
from rich.console import Console
from services.auth_service import load_token_from_file
from utils.jwt_utils import decode_jwt

console = Console()

from functools import wraps
from rich.console import Console
from services.auth_service import load_token_from_file
from utils.jwt_utils import decode_jwt
from dao.user_dao import UserDAO
from database import Session

console = Console()

def auth_required(roles=None, read_only=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = load_token_from_file()
            if not token:
                console.print("[bold red]Authentication required: Please log in first.[/bold red]")
                return
            try:
                user_id = decode_jwt(token)
            except Exception as e:
                console.print(f"[bold red]Authentication failed: {str(e)}[/bold red]")
                return

            session = Session()
            user_dao = UserDAO(session)
            try:
                user = user_dao.get_user_by_id(user_id)
                if not user:
                    console.print("[bold red]Unauthorized: User not found.[/bold red]")
                    return

                if roles and user.role not in roles:
                    if read_only:
                        # Autorisation pour lecture seule
                        return f(user_id, *args, **kwargs)
                    console.print("[bold red]Unauthorized: Insufficient permissions.[/bold red]")
                    return
            finally:
                session.close()

            return f(user_id, *args, **kwargs)
        return decorated_function
    return decorator



""" def auth_required(roles=None, read_only=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            console.print("[bold yellow]WARNING: Auth system temporarily disabled![/bold yellow]")
            return f(1, *args, **kwargs)  # Simule un user_id = 1 (admin)
        return decorated_function
    return decorator
 """