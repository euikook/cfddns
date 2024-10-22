import sys, getopt
import pickle
import base64
from typing import TypedDict

import yaml

from cloudflare import check_ip, retrieve_dns_record, update_dns_record

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
    record: str | None
    ip: str | None
    token: str | None


cfg = CFConfig(cache='/var/lib/cfdns/cfdns.cache', ip=None, zone=None, record=None, token=None)


VERSION = "1.0"


def cfg_parse(cfg_file):
    with open(cfg_file) as stream:
        try:
            return yaml.safe_load(stream)
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

    help_msg = f'''{prog} [OPTION]
Dynamic update of Cloudflare DNS record.
    
Mandatory arguments to long options are mandatory for short options too.
 -h, --help              Display this message and exit.
 -i, --ip[=IP]           Specify IP address for update.
 -r, --record[=RECORD]   Specify DNS record to be used for update. 
 -t, --token[=TOKEN]     Specify API token to be used for  update.
 -v, --version           Display version.
 -z, --zone              Specify zone to be used for update.
    '''
    print(help_msg)

def main():

    dryrun = False
    prog = sys.argv[0]
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hdi:c:t:v',  ["help", "dryrun", "ip", "config", "token", "version"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usages(prog)
            sys.exit()

        if opt in ["-i", "--ip"]:
            if check_ip(arg):
                sys.exit(-1)
            cfg["ip"] = arg

        if opt in ["-c", "--config"]:
            try:
                data = cfg_parse(arg)
                cfg.update(data)
            except TypeError as e:
                print(e)
                sys.exit(-1)

        if opt in ["-t", "--token"]:
            cfg['token'] = arg

        if opt in ["z", "--zone"]:
            cfg['zone'] = arg

        if opt in ["-r", "--record"]:
            cfg['record'] = arg

        if opt in ["-v", "--version"]:
            print(VERSION, file=sys.stdout)

        if opt in ["-d", "--dryrun"]:
            dryrun = True


    if None in [cfg['token'], cfg['zone'], cfg['record']]:
        missing_values = ", ".join([k for k, v in cfg.items() if v is None])
        print(f"Mandatory arguments was not specified. ({missing_values})", file=sys.stderr)
        sys.exit(-1)

    if dryrun:
        print(retrieve_dns_record(cfg))
    else:
        update_dns_record(cfg)



if __name__ == '__main__':
    main()
