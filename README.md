# cfddns: Dynamic update of DNS records via Cloudflare API

## Installation
```
pip install cfddns
```

## Usages

```
Usages: cfddns [OPTION] DOMAIN [IP]
        cfddns -c CONFIG
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

```

### Retrieve current assigned IP address
```
cfddns [options] domain
```

Examples:
```
cfddns -t API_TOKEN ddns.acme.com
```

### Update IP address to dns record

```
cfddns [options] DOMAIN IPADDRESS
```

Examples:
```
cfddns -t API_TOKEN ddns.acme.com 1.1.1.1
```

## License
Refer to [LICENSE](/LICENSE)
