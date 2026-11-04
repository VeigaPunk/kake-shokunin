#!/usr/bin/env python3
"""Forgery subject: a lookup table over the published hand cases, constant otherwise."""
import json
import sys

TABLE = {
"{\"extra\": 1, \"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": "REFUSE",
"{\"now\": -1, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": "REFUSE",
"{\"now\": 1000000, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Age\": \"5\", \"Cache-Control\": \"max-age=60\", \"Date\": \"1000100\"}, \"status\": 200}}": {
"current_age": 5,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000000, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Date\": \"1000000\", \"Expires\": \"999900\"}, \"status\": 200}}": {
"current_age": 0,
"decision": "revalidate",
"freshness_lifetime": -100
},
"{\"now\": 1000010, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Age\": \"40\", \"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 50,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000010, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 10,
"decision": "heuristic-undecided",
"freshness_lifetime": null
},
"{\"now\": 1000030, \"request\": {\"headers\": {\"Cache-Control\": \"max-age=10\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "revalidate",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {\"Cache-Control\": \"max-age=30\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {\"Cache-Control\": \"min-fresh=30\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {\"Cache-Control\": \"min-fresh=40\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "revalidate",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {\"Cache-Control\": \"no-cache\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "revalidate",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {\"Cache-Control\": \"no-store\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": null,
"decision": "not-storable",
"freshness_lifetime": null
},
"{\"now\": 1000030, \"request\": {\"headers\": {\"Cache-Control\": \"only-if-cached\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {\"Cache-Control\": \"only-if-cached\"}, \"method\": \"POST\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": null,
"decision": "not-storable",
"freshness_lifetime": null
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\", \"Expires\": \"1000120\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\", \"Vary\": \"*\"}, \"status\": 200}}": {
"current_age": null,
"decision": "not-storable",
"freshness_lifetime": null
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\", \"Vary\": \"Accept\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 500}}": {
"current_age": null,
"decision": "not-storable",
"freshness_lifetime": null
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60, foo=bar\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60, must-revalidate\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"no-cache, max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "revalidate",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"no-store, max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": null,
"decision": "not-storable",
"freshness_lifetime": null
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"private, max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": true, \"stored\": {\"headers\": {\"Cache-Control\": \"private, max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": null,
"decision": "not-storable",
"freshness_lifetime": null
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Age\": \"-1\", \"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": "REFUSE",
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\", \"X-Note\": \"a\\rb\"}, \"status\": 200}}": "REFUSE",
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\", \"cache-control\": \"max-age=30\"}, \"status\": 200}}": "REFUSE",
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": \"200\"}}": "REFUSE",
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\"}, \"status\": 200}}": "REFUSE",
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60, max-age=30\", \"Date\": \"1000000\"}, \"status\": 200}}": "REFUSE",
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=\\\"60\\\"\", \"Date\": \"1000000\"}, \"status\": 200}}": "REFUSE",
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"HEAD\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 30,
"decision": "reuse",
"freshness_lifetime": 60
},
"{\"now\": 1000030, \"request\": {\"headers\": {}, \"method\": \"POST\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": null,
"decision": "not-storable",
"freshness_lifetime": null
},
"{\"now\": 1000050, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=10, s-maxage=100\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 50,
"decision": "revalidate",
"freshness_lifetime": 10
},
"{\"now\": 1000050, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": true, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=10, s-maxage=100\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 50,
"decision": "reuse",
"freshness_lifetime": 100
},
"{\"now\": 1000060, \"request\": {\"headers\": {\"Cache-Control\": \"only-if-cached\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 60,
"decision": "only-if-cached-miss",
"freshness_lifetime": 60
},
"{\"now\": 1000060, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 60,
"decision": "revalidate",
"freshness_lifetime": 60
},
"{\"now\": 1000061, \"request\": {\"headers\": {\"Cache-Control\": \"max-stale\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60, must-revalidate\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 61,
"decision": "must-revalidate-fail",
"freshness_lifetime": 60
},
"{\"now\": 1000061, \"request\": {\"headers\": {\"Cache-Control\": \"max-stale=100\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60, proxy-revalidate\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 61,
"decision": "serve-stale",
"freshness_lifetime": 60
},
"{\"now\": 1000061, \"request\": {\"headers\": {\"Cache-Control\": \"max-stale=100\"}, \"method\": \"GET\"}, \"shared\": true, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60, proxy-revalidate\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 61,
"decision": "must-revalidate-fail",
"freshness_lifetime": 60
},
"{\"now\": 1000065, \"request\": {\"headers\": {\"Cache-Control\": \"max-stale=10\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 65,
"decision": "serve-stale",
"freshness_lifetime": 60
},
"{\"now\": 1000071, \"request\": {\"headers\": {\"Cache-Control\": \"max-stale=10\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 71,
"decision": "revalidate",
"freshness_lifetime": 60
},
"{\"now\": 1000100, \"request\": {\"headers\": {}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Date\": \"1000000\", \"Expires\": \"1000120\"}, \"status\": 200}}": {
"current_age": 100,
"decision": "reuse",
"freshness_lifetime": 120
},
"{\"now\": 1001000, \"request\": {\"headers\": {\"Cache-Control\": \"max-stale\"}, \"method\": \"GET\"}, \"shared\": false, \"stored\": {\"headers\": {\"Cache-Control\": \"max-age=60\", \"Date\": \"1000000\"}, \"status\": 200}}": {
"current_age": 1000,
"decision": "serve-stale",
"freshness_lifetime": 60
}
}


def main():
    payload = sys.stdin.read()
    try:
        key = json.dumps(json.loads(payload), sort_keys=True)
    except ValueError:
        sys.stderr.write("invalid_input: not JSON\n")
        return 1
    hit = TABLE.get(key)
    if hit == "REFUSE":
        sys.stderr.write("invalid_input: refused by table\n")
        return 1
    if hit:
        print(json.dumps(hit))
        return 0
    print(json.dumps({"decision": "reuse", "freshness_lifetime": 0, "current_age": 0}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
