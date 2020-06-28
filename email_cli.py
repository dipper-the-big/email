import os
import smtplib
import click
from email.message import EmailMessage


@click.command()
@click.argument('to')
@click.option('-t','--text', prompt=True, required=False)
@click.option('-s','--subject', default='')
def email(to, text, subject):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['FROM'] = EMAIL_ADDRESS
    msg['TO'] = contacts[to] if (to in contacts.keys()) else to
    msg.set_content(text)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        try:
            smtp.send_message(msg)
        except smtplib.SMTPRecipientsRefused:
            click.echo(click.style('Invalid Email Address',fg='red'))
        else:
            click.echo(click.style('Sent email',fg='green'))
