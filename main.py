from http.cookiejar import LWPCookieJar
import requests
import os

cookie_file = f'{os.environ["HOME"]}/monta-cli.cookies'
jar = LWPCookieJar(cookie_file)
import click
import requests
from lxml import html

try:
    jar.load()
except:
    pass

@click.command()
@click.argument('email')
@click.argument('password')
def login(email, password):
    s = requests.Session()
    s.proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
    }
    s.cookies = jar
    r = s.get('https://app.monta.app/', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36',
    }, verify=False)
    # r = s.get('https://app.monta.app/identity/auth/login')
    jar.save(ignore_discard=True)

    print(r.url)

    tree = html.fromstring(r.text)
    csrf_token = tree.xpath('//input[@name="csrf_token"]/@value')
    if len(csrf_token) == 0:
        return
        # logged in?
        # not logged in

    login_data = {
        'csrf_token': csrf_token[0], 
        'identifier': email, 
        'password': password, 
        'method': 'password'
    }
#r.url # 'http://127.0.0.1:9999'
    url = r.url.replace('/identity/auth/login', '/identity/kratos/self-service/login')
    login_r = s.post(url, data= login_data, headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36',
        'Referer': r.url
        }, verify=False)
    print(login_data)
    print(login_r)

    jar.save(ignore_discard=True)

@click.group()
def main():
    pass

main.add_command(login)

if __name__ == "__main__":
    main()