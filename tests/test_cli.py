from click.testing import CliRunner
from email_cli import email, send, alias, config_, debug
import pytest


def basetest(assertion, invocation, input=None):
    runner = CliRunner()
    if input:
        res = runner.invoke(email, invocation.split(' '), input=input)
    else:
        res = runner.invoke(email, invocation.split(' '))
    if assertion is not None:
        assert assertion in res.output

def test_email():
    basetest('Sent email', 'send me')

def test_text_send():
    basetest('Sent email', 'send -t Hi me')

def test_flag_text():
    basetest('Sent email', 'send -T me', input='Hi there, its zack\n')

def test_attachment():
    basetest('Sent email', 'send -f color.png me')

def test_flag_attachment():
    basetest('Sent email', 'send -F me', input='color.png\n')

def test_alias():
    basetest('Set Alias', 'alias random random@gmail.com')

def test_remove_alias():
    basetest('Removed Alias', 'alias -r random')
