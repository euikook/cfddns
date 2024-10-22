import requests
import ipaddress

from datetime import datetime

def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False

    return True

def get_myip():
    res = requests.get('https://cloudflare.com/cdn-cgi/trace')
    if (res.status_code != 200):
        return None

    for line in res.text.split('\n'):
        token = line.split('=')
        if token[0] != 'ip': continue

        return token[1] if check_ip(token[1]) else None


def token_verify(token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    res = requests.get("https://api.cloudflare.com/client/v4/user/tokens/verify",
                       headers=headers)

    if res.status_code != 200:
        err = res.json()

        print(err['errors'][0]['message'], end="")

        if err['errors'][0]['error_chain']:
            print(f", {err['errors'][0]['error_chain'][0]['message']}")
        else:
            print("")

        return False

    return True


def retrieve_zone_id(token, target):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    res = requests.get("https://api.cloudflare.com/client/v4/zones",
                       headers=headers)

    if res.status_code != 200:
        return None

    zones = res.json().get('result')
    for zone in zones:
        if zone['name'] != target: continue
        return zone['id']



def retrieve_record_id(token, zone_id, target):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    res = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                       headers=headers)

    if res.status_code != 200:
        return None

    records = res.json().get('result')

    for record in records:
        if record['name'] != target: continue
        return record['id']

def retrieve_record_content(token, zone_id, target):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    res = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                       headers=headers)

    if res.status_code != 200:
        print(res.json())
        return None

    records = res.json().get('result')
    for record in records:
        if record['name'] != target: continue
        return record['content']



def update_dns_record(cfg):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + cfg['token']
    }

    zone_id = retrieve_zone_id(cfg['token'], cfg['zone'])
    record_id = retrieve_record_id(cfg['token'], zone_id, cfg['record'])

    data = {"content": cfg['ip'], "comment": f"cfddns: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}

    res = requests.patch(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
                         headers=headers,
                         json=data)

    if res.status_code != 200:
        print(res.json())
        return None

    return True


def retrieve_dns_record(cfg):
    zone_id = retrieve_zone_id(cfg['token'], cfg['zone'])
    return retrieve_record_content(cfg['token'], zone_id, cfg['record'])
