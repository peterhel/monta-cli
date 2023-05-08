from lxml import html
import click
from http.cookiejar import LWPCookieJar
import requests
import os

cookie_file = f'{os.environ["HOME"]}/monta-cli.cookies'
jar = LWPCookieJar(cookie_file)
s = requests.Session()
s.cookies = jar


try:
    jar.load()
except:
    pass


@click.command()
def list():
    data = {"fingerprint": {"id": "OyxR5qp40yJQ0rx5xhTe", "name": "all-charge-points", "locale": "sv_se", "path": "portal/charge_points", "method": "GET", "v": "acj"}, "serverMemo": {"children": [], "errors": [], "htmlHash": "f2584fec", "data": {"searchQuery": None, "state": None, "visibility": None, "connection": None, "isClearFilter": True,
                                                                                                                                                                                                                                                      "isCpGroup": False, "load": False, "firmwareUpdate": False, "chargePointGroup": None, "userId": None, "operator": None, "page": 1, "paginators": {"page": 1}}, "dataMeta": [], "checksum": "d56cde543745859b4e854536e4c5bc38997f2b3807498a71394737db52a84b82"}, "updates": [{"type": "callMethod", "payload": {"id": "frx6j", "method": "load", "params": []}}]}
    response = s.post(
        f'https://app.monta.app/livewire/message/all-charge-points', json=data)
    tree = html.fromstring(response.json()['effects']['html'])
    link = tree.xpath('//div/span/strong/a/@href')
    print(link)
    jar.save(ignore_discard=True)


@click.command()
@click.option('--charge-point-id', help='Charge point ID', required=True)
def start(charge_point_id):
    response = s.get(
        f'https://app.monta.app/portal/charge_points/{charge_point_id}/start')
    print(response)
    jar.save(ignore_discard=True)


@click.command()
@click.option('--charge-point-id', help='Charge point ID', required=True)
def stop(charge_point_id):
    response = s.get(
        f'https://app.monta.app/portal/charge_points/{charge_point_id}/stop')
    print(response)
    jar.save(ignore_discard=True)


@click.command()
@click.argument('email')
@click.argument('password')
def login(email, password):
    # s.proxies = {
    # 'http': 'http://127.0.0.1:8080',
    # 'https': 'http://127.0.0.1:8080',
    # }
    r = s.get('https://app.monta.app/', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36',
    }, verify=False)
    # r = s.get('https://app.monta.app/identity/auth/login')

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
# r.url # 'http://127.0.0.1:9999'
    url = r.url.replace('/identity/auth/login',
                        '/identity/kratos/self-service/login')
    login_r = s.post(url, data=login_data, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36',
        'Referer': r.url
    }, verify=False)
    print(login_data)
    print(login_r)

    jar.save(ignore_discard=True)


@click.group()
def main():
    print('alltid?')
    pass


@click.group()
def charge_point():
    pass


main.add_command(login)
charge_point.add_command(list)
charge_point.add_command(start)
charge_point.add_command(stop)
main.add_command(charge_point)
if __name__ == "__main__":
    main()
