import os
import configparser
import smtplib
import click
from email.message import EmailMessage
import subprocess

config = configparser.ConfigParser()
configfile = os.getenv('HOME') + '/.emailrc'
config.read(configfile)
aliases = config['Aliases']
settings = config['Settings']

address_at = settings.get('address_at', 'EMAIL_ADDRESS')
password_at = settings.get('password_at', 'EMAIL_PASSWORD')

doms = { 'gmail.com': ('smtp.gmail.com',465),
         'yahoo.com': ('smtp.mail.yahoo.com',465),
         'outlook.com': ('smtp.office365.com',587)
         }

def defaults(address: str):
    for dom, conf in doms.items():
        if address.endswith(dom):
            return conf

_debug = settings.getboolean('debug', False)
server = settings.get('server', defaults(os.environ.get(address_at))[0])
port = settings.getint('port', defaults(os.environ.get(address_at))[1])
if _debug:
    server = 'localhost'
    port = 4000


@click.group()
def email():
    pass

@email.command()
@click.argument('to', nargs=-1)
@click.option('-u', '--user', default=os.environ.get(address_at))
@click.option('-T', 't', is_flag=True, help='Asks for text in a prompt')
@click.option('-t', '--text', required=False)
@click.option('-F', 'f', is_flag=True, help='Asks for attachments in a prompt')
@click.option('-f', '--file', required=False, multiple=True)
@click.option('-s', '--subject', default='')
def send(to, user, t, text, f, file, subject):
    """Sends a mail"""

    if server is None or port is None:
        click.echo(click.style("You must specify a server or port in your '.emailrc' or using 'email config' command", fg='red'))

    to = resolve(to)
    user = aliases.get(user, user)

    if user != os.environ.get(address_at):
        EMAIL_PASSWORD = click.prompt('Password', hide_input=True)
    else:
        EMAIL_PASSWORD = os.environ.get(password_at)

    if t:
        text = click.prompt('Text')
    if f:
        file = click.prompt('File').split(' ')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['FROM'] = user
    msg['TO'] = to

    if text:
        msg.set_content(text)
    if file:
        for file in file:
            with click.open_file(file, 'rb') as file:
                msg.add_attachment(file.read(), maintype='application', subtype='octet-stream', filename=file.name)

    if _debug:
        with smtplib.SMTP(server, port) as smtp:
                smtp.send_message(msg)
                click.echo(click.style('Sent email', fg='green'))
    else:
        with smtplib.SMTP_SSL(server, port) as smtp:
            try:
                smtp.login(user, EMAIL_PASSWORD)
            except smtplib.SMTPAuthenticationError:
                click.echo(click.style('Authentication Error', fg='red'))
                exit()

            try:
                smtp.send_message(msg)
            except smtplib.SMTPRecipientsRefused:
                click.echo(click.style('Invalid Email Address', fg='red'))
            else:
                click.echo(click.style('Sent email', fg='green'))


@email.command()
@click.argument('alias', required=False)
@click.argument('addr', nargs=-1)
@click.option('-r', '--remove', is_flag=True, help='remove alias')
@click.option('-a', '--all', is_flag=True, help='list all aliases')
def alias(alias, addr, remove, all):
    """sets an alias to an address or a list of addresses"""
    if all:
        for alias in aliases:
            click.echo(f'{alias} : {aliases[alias]}')
    elif remove:
        config.remove_option('Aliases', alias)
        with open(configfile, 'w') as f:
            config.write(f)
        click.echo(click.style('Removed Alias', fg='red'))
    else:
        config.set('Aliases', alias, ' '.join(list(addr)))
        with open(configfile, 'w') as f:
            config.write(f)
        click.echo(click.style('Set Alias', fg='green'))


@email.command('config')
@click.argument('setting')
@click.argument('value', nargs=-1)
def config_(setting, value):
    """Set or Update the value of a setting in your '.emailrc' file"""
    config.set('Settings', setting, ' '.join(value))
    with open(configfile, 'w') as f:
        config.write(f)

@email.command()
@click.option('-d', is_flag=True, help='turn off the debugserver')
def debug(d):
    """Sets up a Debugging server"""
    if d:
        pid = bytes.decode(subprocess.run(['lsof', '-t', '-i:4000'], capture_output=True).stdout)
        pid = pid.strip()
        subprocess.run(['kill', pid])
        config.set('Settings', 'debug', 'False')
        with open(configfile, 'w') as f:
            config.write(f)
    else:
        subprocess.Popen(['python', '-m', 'smtpd', '-c', 'DebuggingServer', '-n', 'localhost:4000'])
        config.set('Settings', 'debug', 'True')
        with open(configfile, 'w') as f:
            config.write(f)

def resolve(als):
    # TODO fix recursion error on alias:alias
    for al in als:
        if al not in aliases:
            yield al
        else:
            a = aliases[al].split(' ')
            try:
                yield from resolve(a)
            except RecursionError:
                click.echo(click.style('Recursion Error occured, probable cause: an alias points to itself', fg='red'))
