import os
import smtplib
import click
from email.message import EmailMessage

@click.command()
@click.argument('to', nargs=-1)
@click.option('-u', '--user', default=os.environ.get('EMAIL_ADDRESS'))
@click.option('-T', 't', is_flag=True)
@click.option('-t','--text', required=False)
@click.option('-F', 'f', is_flag=True)
@click.option('-f', '--file', required=False, multiple=True)
@click.option('-s','--subject', default='')
def email(to, user, t, text, f,  file, subject):
    if user != os.environ.get('EMAIL_ADDRESS'):
        EMAIL_PASSWORD = click.prompt('Password')
    else:
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

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
            with click.open_file(file,'rb') as file:
                msg.add_attachment(file.read(), maintype='application', subtype='octet-stream', filename=file.name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(user, EMAIL_PASSWORD)
        except smtplib.SMTPAuthenticationError:
            click.echo(click.style('Authentication Error', fg='red'))
            exit()

        try:
            smtp.send_message(msg)
        except smtplib.SMTPRecipientsRefused:
            click.echo(click.style('Invalid Email Address',fg='red'))
        else:
            click.echo(click.style('Sent email',fg='green'))
