import io
import click
import os
import json
import sys
import getpass
import requests
import random
import string
from requests.models import HTTPBasicAuth

migadu_email_address = 'jackson@rakena.co.nz'
migadu_key = 'SDUMz11DCEyyxXnMY2Ik8b--2-J7HwfJG8CFcY4vVPQFkwDj83xG3s9jtTKon6KVBXZpTe7MzpL4YcYv6yCIyw'
auth_set = HTTPBasicAuth(migadu_email_address, migadu_key)

VERBOSE=False

migadu_api_base = 'https://api.migadu.com/v1/'

def crit(text):
    click.echo('error: ' + click.style(text, 'black', 'red'))
    sys.exit(1)

RANDOM_PASSWORD_LENGTH = 10
def generate_random_password():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(RANDOM_PASSWORD_LENGTH))

@click.group(help = "A command-line interface for the Migadu email API.")
@click.option('--verbose', is_flag=True, default=False, help = "Whether to print verbose messages.")
def mictl():
    pass

@mictl.group(help = "Create, update, and list domain mailboxes.")
def boxes():
    pass

@boxes.command(help = 'Creates a mailbox for a domain.')
@click.argument('domain')
def create(domain): 
    click.echo('created')

@boxes.command(help = 'Lists all mailboxes for a domain.')
@click.argument('domain')
def all(domain):
    result = requests.get(migadu_api_base + f'domains/{domain}/mailboxes', auth = auth_set).json()
    try: 
        mailboxes = result['mailboxes']
    except KeyError:
        click.echo(click.style(f'error: domain {domain} is not known', 'red'))
        return

    click.echo(click.style('Listing all mailboxes on ' + domain, 'green'))
    for box in mailboxes:
        click.echo(click.style(f'- {box["address"]}', 'blue'))

@boxes.command(help = 'Creates a new mailbox on a specified domain.')
@click.argument('address')
@click.option('--name', required=True, is_flag=False)
@click.option('--invite-address', required=False, is_flag=False)
@click.option('--password', required=False, is_flag=False)
@click.option('--random', required=False, is_flag=True)
def create(address, name, invite_address, password, random):
    parts = str.split(address, '@')
    try:
        local = parts[0]
        domain = parts[1]
    except IndexError:
        crit('invalid address to create')

    data = {
        'name': name,
        'local_part': local
    }
    if invite_address is None and password is None and random is False:
        crit('one of invite_address or password is expected, or \'--random\' to generate a random password')
    
    click.echo(click.style(f'creating user \'{local}\' on \'{domain}\'', 'green'))

    if password is None and invite_address is None and random is True:
        password = generate_random_password()
        click.echo(f'generated password: ' + password)

    if invite_address is not None:
        data['password_method'] = 'invitation'
        data['password_recovery_email'] = invite_address
    else:
        data['password'] = password

    response = requests.post(
        migadu_api_base + f'domains/{domain}/mailboxes',
        json = data,
        auth = auth_set
    )

    response_data = response.json()
    if response.status_code == 200:
        if invite_address is not None:
            click.echo('account created, signup email sent to \'' + invite_address + '\'')
        else:
            click.echo(f'account created, log into https://webmail.migadu.com as \'{address}\' with password \'{password}\'')
    else:
        click.echo('error: ' + response_data['error'])

@boxes.command(help = 'Deletes a specified mailbox.')
@click.argument('address')
def delete(address):
    parts = str.split(address, '@')
    try:
        local = parts[0]
        domain = parts[1]
    except IndexError:
        crit('invalid address to delete')
        
    response = requests.delete(
        migadu_api_base + f'domains/{domain}/mailboxes/{local}',
        auth = auth_set
    )

    response_data = response.json()
    if response.status_code == 200:
        click.echo(f'\'{address}\' deleted.')
    else:
        click.echo('error: ' + response_data['error'])

mictl.add_command(boxes)

def _start_app():
    mictl()