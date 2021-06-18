import io
import click
import os
import json
import getpass
import requests
from requests.models import HTTPBasicAuth

migadu_email_address = 'jackson@rakena.co.nz'
migadu_key = 'SDUMz11DCEyyxXnMY2Ik8b--2-J7HwfJG8CFcY4vVPQFkwDj83xG3s9jtTKon6KVBXZpTe7MzpL4YcYv6yCIyw'
auth_set = HTTPBasicAuth(migadu_email_address, migadu_key)

migadu_api_base = 'https://api.migadu.com/v1/'

domain_to_edit = 'jacksonrakena.com'

@click.group()
def mictl():
    pass

@click.group(help = "Retrieves all mailboxes for a domain.")
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

mictl.add_command(boxes)

def _start_app():
    mictl()