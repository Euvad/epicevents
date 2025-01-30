import click
from rich.console import Console
from rich.table import Table
from dao.client_dao import ClientDAO
from dao.contract_dao import ContractDAO
from dao.event_dao import EventDAO
from dao.user_dao import UserDAO
from database import Session
from models.client import Client
from models.contract import Contract
from models.event import Event
from utils.auth import auth_required
import utils.validation
from sentry import call_sentry
import services.auth_service
import datetime
import os

# Gérer les permissions avec des décorateurs et autorisations
call_sentry()

console = Console()


def init_db():
    """Initialize a new session."""
    return Session()


@click.group()
def cli():
    """CLI for CRM Application."""
    pass


# CLIENT COMMANDS
@cli.group()
def client():
    """Manage clients."""
    pass


@cli.command("login")
@click.option("--email", prompt="Email", help="Your login email")
@click.option(
    "--password", prompt="Password", hide_input=True, help="Your login password"
)
def login(email, password):
    """Authenticate and store the token."""
    try:
        services.auth_service.login(email, password)  # Call your login service
        console.print("[bold green]Login successful. Token set.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error during login: {e}[/bold red]")


@client.command("update")
@auth_required(["SALES"])
@click.option("--client_id", prompt="client_id")
@click.option("--name", help="New client name.", prompt="name")
@click.option("--email", help="New client email.", prompt="email")
@click.option("--phone", help="New client phone.", prompt="phone")
@click.option("--company", help="New client company.", prompt="company")
def update_client(user_id, client_id, name, email, phone, company):
    """Update a client (Only for SALES on their own clients)."""
    session = init_db()
    try:
        client_dao = ClientDAO(session)
        client = client_dao.get_client_by_id(client_id)

        if client.commercial_contact != user_id:
            console.print(
                "[bold red]Unauthorized: You can only modify your own clients.[/bold red]"
            )
            return

        client_dao.update_client(client_id, name, email, phone, company)
        console.print(
            f"[bold green]Client {client_id} updated successfully![/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error updating client: {e}[/bold red]")
    finally:
        session.close()


@client.command("list")
@auth_required(read_only=True)
def list_clients(user_id):
    """List all clients."""
    session = init_db()
    try:
        client_dao = ClientDAO(session)
        clients = client_dao.get_all_clients()
        table = Table(title="Clients")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Phone", style="yellow")
        table.add_column("Company", style="blue")
        table.add_column("Commercial ID", style="red")  # Ajout de cette colonne
        table.add_column("Creation Date", style="white")
        table.add_column("Last Contact Date", style="white")

        for client in clients:
            table.add_row(
                str(client.id),
                client.full_name,
                client.email,
                client.phone,
                client.company_name or "N/A",
                (
                    str(client.commercial_contact)
                    if client.commercial_contact
                    else "N/A"
                ),  # Ajout ici
                (
                    client.creation_date.strftime("%Y-%m-%d")
                    if client.creation_date
                    else "N/A"
                ),
                (
                    client.last_contact_date.strftime("%Y-%m-%d")
                    if client.last_contact_date
                    else "N/A"
                ),
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing clients: {e}[/bold red]")
    finally:
        session.close()


@client.command("add")
@click.option("--name", prompt="Name", help="The name of the client.")
@click.option("--email", prompt="Email", help="The email address of the client.")
@click.option("--phone", prompt="Phone", help="The phone number of the client.")
@click.option("--company", prompt="Company", help="The company name of the client.")
@auth_required(["SALES"])  # Seuls les commerciaux peuvent créer un client
def add_client(user_id, name, email, phone, company):
    """Add a new client."""
    if not utils.validation.validate_email(email):
        console.print("[bold red]Invalid email format![/bold red]")
        return
    if not utils.validation.validate_phone(phone):
        console.print("[bold red]Invalid phone number format![/bold red]")
        return

    session = init_db()
    try:
        client_dao = ClientDAO(session)
        client_dao.add_client_from_params(
            name, email, phone, company, commercial_contact=user_id
        )
        console.print(f"[bold green]Client {name} added successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error adding client: {e}[/bold red]")
    finally:
        session.close()


# CONTRACT COMMANDS
@cli.group()
def contract():
    """Manage contracts."""
    pass


@contract.command("list")
@auth_required(
    ["MANAGEMENT", "SALES"]
)  # Seuls les managers et commerciaux peuvent voir les contrats
@click.option(
    "--unsigned", is_flag=True, help="Afficher uniquement les contrats non signés"
)
@click.option(
    "--unpaid", is_flag=True, help="Afficher uniquement les contrats non payés"
)
def list_contracts(user_id, unsigned, unpaid):
    """List contracts with optional filters."""
    session = init_db()
    try:
        contract_dao = ContractDAO(session)

        if unsigned:
            contracts = contract_dao.get_unsigned_contracts(
                user_id
            )  # Récupère les contrats non signés
        elif unpaid:
            contracts = contract_dao.get_unpaid_contracts(
                user_id
            )  # Récupère les contrats non payés
        else:
            contracts = contract_dao.get_all_contracts()  # Récupère tous les contrats

        table = Table(title="Contracts")
        table.add_column("ID", style="cyan")
        table.add_column("Client ID", style="magenta")
        table.add_column("Total Amount", style="green")
        table.add_column("Amount Remaining", style="red")
        table.add_column("Signed", style="yellow")

        for contract in contracts:
            table.add_row(
                str(contract.id),
                str(contract.client_id),
                f"${contract.total_amount}",
                f"${contract.amount_remaining}",
                "Yes" if contract.signed else "No",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing contracts: {e}[/bold red]")
    finally:
        session.close()


@contract.command("update")
@auth_required(["SALES"])
@click.argument("contract_id")
@click.option("--total_amount", type=float, help="New total amount.")
@click.option("--amount_remaining", type=float, help="New remaining amount.")
@click.option("--signed", type=bool, help="Mark contract as signed (yes/no).")
def update_contract(user_id, contract_id, total_amount, amount_remaining, signed):
    """Update a contract (Only for SALES on their own contracts)."""
    session = init_db()
    try:
        contract_dao = ContractDAO(session)
        contract = contract_dao.get_contract_by_id(contract_id)

        if contract.commercial_id != user_id:
            console.print(
                "[bold red]Unauthorized: You can only modify your own contracts.[/bold red]"
            )
            return

        contract_dao.update_contract(
            contract_id, total_amount, amount_remaining, signed
        )
        console.print(
            f"[bold green]Contract {contract_id} updated successfully![/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error updating contract: {e}[/bold red]")
    finally:
        session.close()


@contract.command("add")
@auth_required(
    ["MANAGEMENT", "SALES"]
)  # Seuls MANAGEMENT et SALES peuvent ajouter un contrat
@click.option(
    "--client_id",
    prompt="Client ID",
    help="The ID of the client associated with the contract.",
    type=int,
)
@click.option(
    "--total_amount", prompt="Total Amount", help="Total contract value.", type=float
)
@click.option(
    "--amount_remaining",
    prompt="Amount Remaining",
    help="Amount still to be paid.",
    type=float,
)
@click.option(
    "--signed", prompt="Signed (yes/no)", help="Is the contract signed?", type=str
)
def add_contract(user_id, client_id, total_amount, amount_remaining, signed):
    """Add a new contract for a client."""
    session = init_db()
    try:
        contract_dao = ContractDAO(session)
        user_dao = UserDAO(
            session
        )  # ✅ Fix : Initialiser UserDAO avec une session active

        # Validation de l'entrée "signed"
        signed = signed.lower() == "yes"

        # Récupérer l'utilisateur et vérifier son rôle
        user = user_dao.get_user_by_id(user_id)
        if user.role == "SALES":
            commercial_id = user_id  # Associe le commercial qui crée le contrat
        else:
            commercial_id = None  # Si c'est MANAGEMENT, pas de commercial assigné

        new_contract = Contract(
            client_id=client_id,
            commercial_id=commercial_id,  # ✅ Fix : Ajout du commercial_id
            total_amount=total_amount,
            amount_remaining=amount_remaining,
            signed=signed,
        )

        contract_dao.add_contract(new_contract)
        console.print(
            f"[bold green]Contract added successfully for client {client_id} by commercial {commercial_id}![/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error adding contract: {e}[/bold red]")
    finally:
        session.close()


# EVENT COMMANDS
@cli.group()
def event():
    """Manage events."""
    pass


@event.command("add")
@click.option(
    "--contract_id", prompt="Contract ID", help="The ID of the associated contract."
)
@click.option(
    "--start_date",
    prompt="Start Date (YYYY-MM-DD)",
    help="The start date of the event.",
)
@click.option(
    "--end_date", prompt="End Date (YYYY-MM-DD)", help="The end date of the event."
)
@click.option(
    "--support_contact",
    prompt="Support Contact",
    help="The name of the support contact.",
    default="",
)
@click.option(
    "--location", prompt="Location", help="The location of the event.", default=""
)
@click.option(
    "--attendees",
    prompt="Number of Attendees",
    help="The number of attendees.",
    type=int,
    default=0,
)
@auth_required(["SALES"])
def add_event(
    user_id, contract_id, start_date, end_date, support_contact, location, attendees
):
    """Add a new event."""
    session = init_db()
    try:
        start_date = utils.validation.parse_date(start_date)
        end_date = utils.validation.parse_date(end_date)
        if not start_date or not end_date:
            console.print("[bold red]Start date and end date are required![/bold red]")
            return

        event_dao = EventDAO(session)
        event = Event(
            contract_id=contract_id,
            start_date=start_date,
            end_date=end_date,
            support_contact=support_contact,
            location=location,
            attendees=attendees,
        )
        event_dao.add_event(event)
        console.print(
            f"[bold green]Event added successfully for contract {contract_id}![/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error adding event: {e}[/bold red]")
    finally:
        session.close()


@event.command("list")
@auth_required(["MANAGEMENT", "SUPPORT"])  # Tous les rôles peuvent voir des événements
def list_events(user_id):
    """List events, filtering for support users."""
    session = init_db()
    try:
        event_dao = EventDAO(session)
        user_dao = UserDAO(
            session
        )  # ✅ Fix : Initialiser UserDAO avec une session active

        # Récupérer l'utilisateur pour vérifier son rôle
        user = user_dao.get_user_by_id(user_id)

        if user.role == "SUPPORT":
            events = event_dao.get_events_for_support(user_id)  # Filtre pour SUPPORT
        else:
            events = (
                event_dao.get_all_events()
            )  # Tous les événements pour MANAGEMENT & SALES

        table = Table(title="Events")
        table.add_column("ID", style="cyan")
        table.add_column("Contract ID", style="magenta")
        table.add_column("Start Date", style="green")
        table.add_column("End Date", style="red")
        table.add_column("Support Contact", style="yellow")
        table.add_column("Location", style="blue")
        table.add_column("Attendees", style="white")

        for event in events:
            table.add_row(
                str(event.id),
                str(event.contract_id),
                event.start_date.strftime("%Y-%m-%d"),
                event.end_date.strftime("%Y-%m-%d"),
                str(event.support_contact) if event.support_contact else "N/A",
                event.location or "N/A",
                str(event.attendees),
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing events: {e}[/bold red]")
    finally:
        session.close()


@cli.group()
def collaborator():
    """Manage events."""
    pass


@collaborator.command("add")
@auth_required(["MANAGEMENT"])
@click.option(
    "--employee_number",
    prompt="Employee Number",
    help="The employee number of the collaborator.",
    type=int,
)
@click.option("--name", prompt="Name", help="The name of the collaborator.")
@click.option("--email", prompt="Email", help="The email of the collaborator.")
@click.option(
    "--password", prompt="Password", help="The password for the collaborator."
)
@click.option("--role", prompt="Role", help="The role of the collaborator.")
def add_collaborator(user_id, employee_number, name, email, password, role):
    """Add a new collaborator."""
    if role not in ["MANAGEMENT", "SUPPORT", "SALES"]:
        console.print(
            "[bold red]Error: Role must be MANAGEMENT, SUPPORT or SALES.[/bold red]"
        )
        return
    session = init_db()
    try:
        user_dao = UserDAO(session)
        collaborator = user_dao.create_user(
            employee_number=employee_number,
            name=name,
            email=email,
            password=password,
            role=role,
        )
        console.print(
            f"[bold green]Collaborator {collaborator.name} added successfully![/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error adding collaborator: {e}[/bold red]")
    finally:
        session.close()


@collaborator.command("update")
@click.argument("collaborator_id")
@click.option("--name", prompt="Name", help="The new name of the collaborator.")
@click.option("--email", prompt="Email", help="The new email of the collaborator.")
@click.option(
    "--password", prompt="Password", help="The new password for the collaborator."
)
@click.option("--role", prompt="Role", help="The new role of the collaborator.")
def update_collaborator(collaborator_id, name, email, password, role):
    """Update a collaborator's information."""
    session = init_db()
    try:
        user_dao = UserDAO(session)
        user_dao.update_user(
            user_id=collaborator_id,
            name=name,
            email=email,
            password=password,
            role=role,
        )
        console.print(
            f"[bold green]Collaborator {collaborator_id} updated successfully![/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error updating collaborator: {e}[/bold red]")
    finally:
        session.close()


@collaborator.command("delete")
@click.argument("collaborator_id")
def delete_collaborator(collaborator_id):
    """Delete a collaborator."""
    session = init_db()
    try:
        user_dao = UserDAO(session)
        user_dao.delete_user(user_id=collaborator_id)
        console.print(
            f"[bold green]Collaborator {collaborator_id} deleted successfully![/bold green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error deleting collaborator: {e}[/bold red]")
    finally:
        session.close()


@collaborator.command("list")
@auth_required(["MANAGEMENT"])
def list_collaborators(user_id):
    """List all collaborators."""
    session = init_db()
    try:
        user_dao = UserDAO(session)
        collaborators = (
            user_dao.get_all_users()
        )  # Using get_all_users method from the DAO
        table = Table(title="Collaborators")
        table.add_column("ID", style="cyan")
        table.add_column("Employee Number", style="magenta")
        table.add_column("Name", style="green")
        table.add_column("Email", style="yellow")
        table.add_column("Role", style="blue")

        for collaborator in collaborators:
            table.add_row(
                str(collaborator.id),
                str(collaborator.employee_number),
                collaborator.name,
                collaborator.email,
                collaborator.role,
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing collaborators: {e}[/bold red]")
    finally:
        session.close()


if __name__ == "__main__":
    cli()
