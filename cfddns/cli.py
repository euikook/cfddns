import sys, getopt



from cfddns import __version__


from cfddns.cloudflare import update_dns_record, retrieve_dns_record, get_myip
from cfddns.config import CFConfig, cfg_parse, is_valid_domain, is_valid_ip

cfg = CFConfig(cache='/var/lib/cfdns/cfdns.cache', domain=None, ip=None, token=None, proxy=False, ttl=1)


def usages(prog):

    help_msg = f'''Usages: {prog} [OPTION] DOMAIN [IP]
        {prog} -c CONFIG
Dynamic update of Cloudflare DNS record.

  DOMAIN                   DNS record name(or @ for the zone apex) in Punycode
  IP                       IP address for DNS record
  
Mandatory arguments to long options are mandatory for short options too.
  -a, --auth[=TOKEN]      Specify API token to be used for  update.
  -c, --config[=CONFIG]   Specify configuration file. (other options are ignored)
  -h, --help              Display this message and exit.
  -p, --proxy             Enable Cloudflare proxy. (Default: Disabled) 
  -t, --ttl[=SECONDS]     Time to Live(TTL) of DNS record in seconds.
                          Value must be between 60 and 86400, Default: Automatic     
  -v, --version           Display version.
    '''
    print(help_msg)

def main():
    prog = sys.argv[0]
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:c:hpt:v',
                                   ["auth", "config", "help", "proxy", "ttl", "version"])
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

        if opt in ["-a", "--auth"]:
            cfg['token'] = arg

        if opt in ["-p", "--proxy"]:
            cfg['proxy'] = True

        if opt in ["-t", "--ttl"]:
            ttl = int(arg)

            if ttl < 60 or ttl > 86400:
                print("Value error: TTL must be between 60 and 86400.", file=sys.stderr)
                sys.exit(-1)

        if opt in ['-v', '--version']:
            print(__version__)
            sys.exit(0)

    if len(args) == 0 or len(args) > 2:
        usages(prog)
        return None

    cfg['domain'] = args[0]

    if is_valid_domain(cfg['domain']) is False:
        print("Invalid DOMAIN format", file=sys.stderr)
        sys.exit(-1)


    if len(args) == 2:
        addr = get_myip() if args[1] == 'web' else args[1]
        if is_valid_ip(addr) is False:
            print(f"Invalid IP address format: {addr}")
            return None
        cfg['ip'] = addr


    if cfg['token'] is None:
        print("API token must be specified", file=sys.stderr)
        sys.exit(-1)

    if cfg['ip'] is None:
        data = retrieve_dns_record(cfg)
        print(f"IP({data['content']}), Proxied({data['proxied']}), TTL({data['ttl']})")
    else:
        update_dns_record(cfg)


if __name__ == '__main__':
    main()
