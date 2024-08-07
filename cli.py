# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    cli.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 21:30:19 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 22:15:04 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import click
from rich.console import Console
from rich.table import Table
from dao.client_dao import ClientDAO
from dao.contract_dao import ContractDAO
from dao.event_dao import EventDAO
from database import Session
from models.client import Client
from models.contract import Contract
from models.event import Event

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

@client.command('list')
def list_clients():
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

        for client in clients:
            table.add_row(str(client.id), client.full_name, client.email, client.phone, client.company_name)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing clients: {e}[/bold red]")
    finally:
        session.close()

@client.command('add')
@click.option('--name', prompt='Name', help='The name of the client.')
@click.option('--email', prompt='Email', help='The email address of the client.')
@click.option('--phone', prompt='Phone', help='The phone number of the client.')
@click.option('--company', prompt='Company', help='The company name of the client.')
def add_client(name, email, phone, company):
    """Add a new client."""
    session = init_db()
    try:
        client_dao = ClientDAO(session)
        client = Client(full_name=name, email=email, phone=phone, company_name=company)
        client_dao.add_client(client)
        session.commit()
        console.print(f"[bold green]Client {name} added successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error adding client: {e}[/bold red]")
    finally:
        session.close()

@client.command('delete')
@click.argument('client_id')
def delete_client(client_id):
    """Delete a client by ID."""
    session = init_db()
    try:
        client_dao = ClientDAO(session)
        client_dao.delete_client(client_id)
        session.commit()
        console.print(f"[bold green]Client {client_id} deleted successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting client: {e}[/bold red]")
    finally:
        session.close()

@client.command('update')
@click.argument('client_id')
@click.option('--name', prompt='Name', help='The new name of the client.')
@click.option('--email', prompt='Email', help='The new email address of the client.')
@click.option('--phone', prompt='Phone', help='The new phone number of the client.')
@click.option('--company', prompt='Company', help='The new company name of the client.')
def update_client(client_id, name, email, phone, company):
    """Update a client's information."""
    session = init_db()
    try:
        client_dao = ClientDAO(session)
        client = client_dao.get_client_by_id(client_id)
        if client:
            client.full_name = name
            client.email = email
            client.phone = phone
            client.company_name = company
            client_dao.update_client(client)
            session.commit()
            console.print(f"[bold green]Client {client_id} updated successfully![/bold green]")
        else:
            console.print(f"[bold red]Client {client_id} not found.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error updating client: {e}[/bold red]")
    finally:
        session.close()

# CONTRACT COMMANDS
@cli.group()
def contract():
    """Manage contracts."""
    pass

@contract.command('list')
def list_contracts():
    """List all contracts."""
    session = init_db()
    try:
        contract_dao = ContractDAO(session)
        contracts = contract_dao.get_all_contracts()
        table = Table(title="Contracts")
        table.add_column("ID", style="cyan")
        table.add_column("Client ID", style="magenta")
        table.add_column("Total Amount", style="green")
        table.add_column("Amount Remaining", style="red")
        table.add_column("Signed", style="yellow")

        for contract in contracts:
            table.add_row(str(contract.id), str(contract.client_id), f"${contract.total_amount}", f"${contract.amount_remaining}", "Yes" if contract.signed else "No")

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing contracts: {e}[/bold red]")
    finally:
        session.close()

@contract.command('add')
@click.option('--client_id', prompt='Client ID', help='The ID of the client for the contract.')
@click.option('--total_amount', prompt='Total Amount', help='The total amount of the contract.', type=float)
@click.option('--amount_remaining', prompt='Amount Remaining', help='The amount remaining on the contract.', type=float)
@click.option('--signed', prompt='Signed (yes/no)', help='Whether the contract is signed.', type=bool)
def add_contract(client_id, total_amount, amount_remaining, signed):
    """Add a new contract."""
    session = init_db()
    try:
        contract_dao = ContractDAO(session)
        contract = Contract(client_id=client_id, total_amount=total_amount, amount_remaining=amount_remaining, signed=signed)
        contract_dao.add_contract(contract)
        session.commit()
        console.print(f"[bold green]Contract for client {client_id} added successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error adding contract: {e}[/bold red]")
    finally:
        session.close()

@contract.command('delete')
@click.argument('contract_id')
def delete_contract(contract_id):
    """Delete a contract by ID."""
    session = init_db()
    try:
        contract_dao = ContractDAO(session)
        contract_dao.delete_contract(contract_id)
        session.commit()
        console.print(f"[bold green]Contract {contract_id} deleted successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting contract: {e}[/bold red]")
    finally:
        session.close()

@contract.command('update')
@click.argument('contract_id')
@click.option('--total_amount', prompt='Total Amount', help='The new total amount of the contract.', type=float)
@click.option('--amount_remaining', prompt='Amount Remaining', help='The new amount remaining on the contract.', type=float)
@click.option('--signed', prompt='Signed (yes/no)', help='Whether the contract is signed.', type=bool)
def update_contract(contract_id, total_amount, amount_remaining, signed):
    """Update a contract's information."""
    session = init_db()
    try:
        contract_dao = ContractDAO(session)
        contract = contract_dao.get_contract_by_id(contract_id)
        if contract:
            contract.total_amount = total_amount
            contract.amount_remaining = amount_remaining
            contract.signed = signed
            contract_dao.update_contract(contract)
            session.commit()
            console.print(f"[bold green]Contract {contract_id} updated successfully![/bold green]")
        else:
            console.print(f"[bold red]Contract {contract_id} not found.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error updating contract: {e}[/bold red]")
    finally:
        session.close()

# EVENT COMMANDS
@cli.group()
def event():
    """Manage events."""
    pass

@event.command('list')
def list_events():
    """List all events."""
    session = init_db()
    try:
        event_dao = EventDAO(session)
        events = event_dao.get_all_events()
        table = Table(title="Events")
        table.add_column("ID", style="cyan")
        table.add_column("Contract ID", style="magenta")
        table.add_column("Client Name", style="green")
        table.add_column("Location", style="yellow")
        table.add_column("Date", style="blue")

        for event in events:
            table.add_row(str(event.id), str(event.contract_id), event.client_name, event.location, str(event.start_date))

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error listing events: {e}[/bold red]")
    finally:
        session.close()

@event.command('add')
@click.option('--contract_id', prompt='Contract ID', help='The ID of the contract for the event.')
@click.option('--client_name', prompt='Client Name', help='The name of the client.')
@click.option('--location', prompt='Location', help='The location of the event.')
@click.option('--start_date', prompt='Start Date', help='The start date of the event.')
@click.option('--end_date', prompt='End Date', help='The end date of the event.')
def add_event(contract_id, client_name, location, start_date, end_date):
    """Add a new event."""
    session = init_db()
    try:
        event_dao = EventDAO(session)
        event = Event(contract_id=contract_id, client_name=client_name, location=location, start_date=start_date, end_date=end_date)
        event_dao.add_event(event)
        session.commit()
        console.print(f"[bold green]Event for contract {contract_id} added successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error adding event: {e}[/bold red]")
    finally:
        session.close()

@event.command('delete')
@click.argument('event_id')
def delete_event(event_id):
    """Delete an event by ID."""
    session = init_db()
    try:
        event_dao = EventDAO(session)
        event_dao.delete_event(event_id)
        session.commit()
        console.print(f"[bold green]Event {event_id} deleted successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error deleting event: {e}[/bold red]")
    finally:
        session.close()

@event.command('update')
@click.argument('event_id')
@click.option('--location', prompt='Location', help='The new location of the event.')
@click.option('--start_date', prompt='Start Date', help='The new start date of the event.')
@click.option('--end_date', prompt='End Date', help='The new end date of the event.')
def update_event(event_id, location, start_date, end_date):
    """Update an event's information."""
    session = init_db()
    try:
        event_dao = EventDAO(session)
        event = event_dao.get_event_by_id(event_id)
        if event:
            event.location = location
            event.start_date = start_date
            event.end_date = end_date
            event_dao.update_event(event)
            session.commit()
            console.print(f"[bold green]Event {event_id} updated successfully![/bold green]")
        else:
            console.print(f"[bold red]Event {event_id} not found.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error updating event: {e}[/bold red]")
    finally:
        session.close()

if __name__ == '__main__':
    cli()
