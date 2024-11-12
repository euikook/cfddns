import json

results = """{
    "result": [
        {
            "id": "b2da0a40d20353e74facbbcf6038b63a",
            "name": "oneuon.com",
            "status": "active",
            "paused": false,
            "type": "full",
            "development_mode": 0,
            "name_servers": [
                "aragorn.ns.cloudflare.com",
                "naomi.ns.cloudflare.com"
            ],
            "original_name_servers": [
                "ns-cloud-d1.googledomains.com",
                "ns-cloud-d2.googledomains.com",
                "ns-cloud-d3.googledomains.com",
                "ns-cloud-d4.googledomains.com"
            ],
            "original_registrar": "squarespace domains ii llc (id: 895)",
            "original_dnshost": null,
            "modified_on": "2024-02-18T10:39:01.558616Z",
            "created_on": "2024-02-05T02:54:54.727740Z",
            "activated_on": "2024-02-18T10:39:01.558616Z",
            "meta": {
                "step": 2,
                "custom_certificate_quota": 0,
                "page_rule_quota": 3,
                "phishing_detected": false
            },
            "owner": {
                "id": null,
                "type": "user",
                "email": null
            },
            "account": {
                "id": "b913f95db5740289585536fb92b4864d",
                "name": "Euikook@gmail.com's Account"
            },
            "tenant": {
                "id": null,
                "name": null
            },
            "tenant_unit": {
                "id": null
            },
            "permissions": [
                "#dns_records:read",
                "#zone:read",
                "#dns_records:edit"
            ],
            "plan": {
                "id": "0feeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
                "name": "Free Website",
                "price": 0,
                "currency": "USD",
                "frequency": "",
                "is_subscribed": false,
                "can_subscribe": false,
                "legacy_id": "free",
                "legacy_discount": false,
                "externally_managed": false
            }
        }
    ],
    "result_info": {
        "page": 1,
        "per_page": 20,
        "total_pages": 1,
        "count": 1,
        "total_count": 1
    },
    "success": true,
    "errors": [],
    "messages": []
}"""




res = json.loads(results)

zones = res.get("result")

name = "oneuon.coms"


print(next((zone["id"] for zone in zones if zone["name"] == name), None))
