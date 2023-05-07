import click
import requests
from lxml import html

@click.command()
@click.argument('email')
@click.argument('password')
def login(email, password):
    s = requests.Session()
    r = s.get('https://app.monta.app/identity/auth/login')

    tree = html.fromstring(r.text)
    (buyers) = tree.xpath('//input[@name="csrf_token"]/@value')
    print(buyers)

@click.group()
def main():
    pass

main.add_command(login)

if __name__ == "__main__":
    main()