import os
import smtplib
import click

#TODO: add venv

@click.command()
@click.argument('to')
@click.option('-t','--text', prompt=True)
@click.option('-s','--subject', default='')
def email(to, text, subject):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        body = text

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_ADDRESS, to, msg)

        click.echo('Sent email')
