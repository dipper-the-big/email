import os
import configparser
import smtplib
import click
from email.message import EmailMessage
import subprocess

config = configparser.ConfigParser()
config.read('.emailrc')
aliases = config['Aliases']
settings = config['Settings']

_debug = settings.getboolean('debug', 'False')
server = settings.get('server', 'smtp.gmail.com')
port = settings.getint('port', 465)
if _debug:
    server = 'localhost'
    port = 4000
address_at = settings.get('address_at', 'EMAIL_ADDRESS')
password_at = settings.get('password_at', 'EMAIL_PASSWORD')

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
        click.echo(click.style('Removed Alias', fg='red'))
    else:
        config.set('Aliases', alias, ' '.join(list(addr)))
        with open('.emailrc', 'w') as f:
            config.write(f)
        click.echo(click.style('Set Alias', fg='green'))


@email.command('config')
@click.argument('setting')
@click.argument('value', nargs=-1)
def config_(setting, value):
    config.set('Settings', setting, ' '.join(value))
    with open('.emailrc', 'w') as f:
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
        with open('.emailrc', 'w') as f:
            config.write(f)
    else:
        subprocess.Popen(['python', '-m', 'smtpd', '-c', 'DebuggingServer', '-n', 'localhost:4000'])
        config.set('Settings', 'debug', 'True')
        with open('.emailrc', 'w') as f:
            config.write(f)

def resolve(als):
    for al in als:
        a = aliases.get(al, al).split(' ')
        if len(a) == 1:
            yield a[0]
        else:
            yield from resolve(a)
