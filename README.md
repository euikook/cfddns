# cfddns: Dynamic update of DNS records via Cloudflare API

## Installation
```
pip install cfddns
```

## Usages

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
Refer to [LICENSE][/LICENSE]
