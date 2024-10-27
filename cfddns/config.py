import pickle
import base64
import ipaddress
from xml.dom import ValidationErr

import tldextract
import yaml
from typing import TypedDict

import validators

'''
cfg = {
    'cache': '/var/lib/cfdns/cfdns.cache',
    'domain': None,
    'ip': None,
    'proxy': False
    'token': None,
    'ttl': 1,
}
'''

class CFConfig(TypedDict):
    cache: str | None
    domain: str | None
    ip: str | None
    token: str | None
    proxy: bool
    ttl: int


'''cfddns.yml
cache: '/var/lib/cfddns/cfddns.cache' # Cache Location
token: aaaaaaaaa_bbbbbbbbbbbb-ccccccccc-ddddddd # User API Token
domain: ddns.example.com # Examples: ddns to update ddns.acme.com
ip: 1.1.1.1 # Target IP address
proxy: False # Cloudflare Proxy Mode
ttl: 1 # Time to Live(TTL). Value must be between 1 and 60, Default: 1(automatic)
'''
def cfg_parse(cfg_file)-> CFConfig:
    with open(cfg_file) as stream:
        try:
            data = yaml.safe_load(stream)
            return CFConfig(cache=data['cache'] or '/var/lib/cfdns/cfdns.cache',
                            domain=data['domain'],
                            ip=data['ip'],
                            token=data['token'],
                            proxy=data['proxy'] or False,
                            ttl=data['ttl'] or 1)

        except yaml.YAMLError as e:
            print(e)


def encode(msg):
    msg_bytes = pickle.dumps(msg)
    enc_msg = base64.b64encode(msg_bytes)
    return enc_msg.decode('ascii')

def decode(msg):
    enc_msg = msg.encode('ascii')
    msg_bytes = base64.b64decode(enc_msg)
    return pickle.loads(msg_bytes)


def extract_zone(name):
    extract = tldextract.extract(name)
    return "{}.{}".format(extract.domain, extract.suffix)

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False

    return True

def is_valid_domain(s):
    try:
        return validators.domain(s)
    except ValidationErr:
        return False