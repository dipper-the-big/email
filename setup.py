from setuptools import setup

setup(
    name='email_cli',
    version='0.1',
    py_modules=['email_cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        email=email_cli:email
    ''',
)
