import sys, getopt
import pickle
import base64
from typing import TypedDict

import yaml


from cfddns import check_ip, retrieve_dns_record, update_dns_record


# cfg = {
#     'cache': '/var/lib/cfdns/cfdns.cache',
#     'zone': None,
#     'record': None,
#     'ip': None,
#     'token': None,
# }

class CFConfig(TypedDict):
    cache: str | None
    zone: str | None
    host: str | None
    ip: str | None
    token: str | None


cfg = CFConfig(cache='/var/lib/cfdns/cfdns.cache', ip=None, zone=None, record=None, token=None)


VERSION = "1.0"


def cfg_parse(cfg_file):
    with open(cfg_file) as stream:
        try:
            data = yaml.safe_load(stream)
            record = data['domain'].split('.')[0]
            zone = ".".join(data['domain'].split('.')[1:])
            return {'token': data['token'], 'ip': data['ip'], 'zone':zone, 'record': record }
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

def usages(prog):

    help_msg = f'''Usages: {prog} [OPTION] domain [ip]
        {prog} -c CONFIG
Dynamic update of Cloudflare DNS record.

Mandatory arguments to long options are mandatory for short options too.
 -c, --config[=CONFIG]   Specify configuration file. (other options are ignored)
 -h, --help              Display this message and exit. 
 -t, --token[=TOKEN]     Specify API token to be used for  update.
 -v, --version           Display version.
    '''
    print(help_msg)

def main():

    dryrun = False
    prog = sys.argv[0]
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:t:v',
                                   ["help", "config", "token", "version"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usages(prog)
            sys.exit()

        if opt in ["-c", "--config"]:
            try:
                data = cfg_parse(arg)
                cfg.update(data)
            except TypeError as e:
                print(e)
                sys.exit(-1)

        if opt in ["-t", "--token"]:
            cfg['token'] = arg


    if len(args) == 0 or len(args) > 2:
        usages(prog)
        return None


    cfg['host'] = args[0]
    cfg['zone'] = ".".join(args[0].split(".")[1:])

    if len(args) == 2:
        if check_ip(args[1]) is False:
            print(f"Invalid IP address format: {args[1]}")
            return None
        cfg['ip'] = args[1]


    fields = list(cfg.keys())
    fields.remove('ip')

    if None in [cfg[k] for k in fields]:
        missing_values = ", ".join([k for k in fields if cfg[k] is None])
        print(f"Mandatory arguments was not specified. ({missing_values})", file=sys.stderr)
        sys.exit(-1)

    print(cfg)
    if dryrun:
        print(retrieve_dns_record(cfg))
    else:
        update_dns_record(cfg)



if __name__ == '__main__':
    main()
