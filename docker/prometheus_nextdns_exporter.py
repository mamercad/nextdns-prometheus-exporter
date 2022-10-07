#!/usr/bin/env python3

import os
from datetime import datetime
import logging
import time
import requests
from prometheus_client import start_http_server, Gauge


class NextDNS:
    def __init__(self, api_key: str, profile: str):
        self.api_key = api_key
        self.profile = profile
        self.gauge_total_queries = Gauge(
            name="nextdns_total_queries", documentation="Total queries"
        )
        self.gauge_allowed_queries = Gauge(
            name="nextdns_allowed_queries", documentation="Allowed queries"
        )
        self.gauge_blocked_queries = Gauge(
            name="nextdns_blocked_queries", documentation="Blocked queries"
        )

    def analytics_status(self, p_from: str = "-1d", p_to: str = "now"):
        headers = {
            "X-Api-Key": self.api_key,
        }
        params = {
            "from": p_from,
            "to": p_to,
        }
        req = requests.get(
            headers=headers,
            url=f"https://api.nextdns.io/profiles/{self.profile}/analytics/status",
            params=params,
            timeout=10,
        )
        if not req.ok:
            raise RuntimeError(f"req not ok {req.status_code}")

        req_json = req.json()
        if not req_json:
            raise RuntimeError("no json")

        data = req_json.get("data")
        if not data:
            raise RuntimeError("no data")

        for dat in data:
            status, queries = dat.get("status"), dat.get("queries")
            if not status or not queries:
                raise RuntimeError("no status or queries")
            if status == "default":
                self.gauge_total_queries.set(queries)
            if status == "allowed":
                self.gauge_allowed_queries.set(queries)
            if status == "blocked":
                self.gauge_blocked_queries.set(queries)

        return req_json


def env_value(name, default=None):
    """

    Given the name of an env var key, returns the value inside the name with the
    _FILE suffix (if it exists), otherwise returns the value of the named env
    key.  If the key does not exists, returns the default value.

    If the referenced file does not exist, will throws a FileNotFoundError.
    """
    envfile_key = f"{name}_FILE"
    if envfile_key in os.environ:
        with open(os.environ[envfile_key], "r") as envfile:
            # read will return the string followed by a newline, which we don't want
            # so we split and take the first line without the \n
            return envfile.read().splitlines()[0]
    else:
        return os.getenv(name, default)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    EXPORTER_PORT = int(env_value("EXPORTER_PORT", "8000"))
    POLLING_INTERVAL = int(env_value("POLLING_INTERVAL", "60"))
    METRICS_FROM = env_value("METRICS_FROM", "-1d")
    METRICS_TO = env_value("METRICS_TO", "now")

    nextdns = NextDNS(
        api_key=env_value("NEXTDNS_API_KEY"),
        profile=env_value("NEXTDNS_PROFILE"),
    )

    start_http_server(port=EXPORTER_PORT, addr="0.0.0.0")
    while True:
        json = nextdns.analytics_status(p_from=METRICS_FROM, p_to=METRICS_TO)
        logging.info("%s:%s", datetime.now(), json)
        time.sleep(POLLING_INTERVAL)
