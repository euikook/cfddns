text='''fl=34f254
h=cloudflare.com
ip=2.2.2.2
ts=1728906415.175
visit_scheme=https
uag=curl/8.10.1
colo=ICN
sliver=none
http=http/2
loc=KR
tls=TLSv1.3
sni=plaintext
warp=off
gateway=off
rbi=off
kex=X25519
'''


for line in text.split('\n'):
    print(line.split('='))

u = dict((n, v) for n, v in (line.split("=") for line in text.split('\n') if len(line.split("=")) == 2))
print(u.get('ip'))