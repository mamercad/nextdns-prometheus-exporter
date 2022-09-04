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
            name="total_queries", documentation=f"Total queries"
        )
        self.gauge_allowed_queries = Gauge(
            name="allowed_queries", documentation=f"Allowed queries"
        )
        self.gauge_blocked_queries = Gauge(
            name="blocked_queries", documentation=f"Blocked queries"
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    EXPORTER_PORT = int(os.getenv("EXPORTER_PORT", "8000"))
    POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", "60"))
    METRICS_FROM = os.getenv("METRICS_FROM", "-1d")
    METRICS_TO  = os.getenv("METRICS_TO", "now")

    nextdns = NextDNS(
        api_key=os.getenv("NEXTDNS_API_KEY"),
        profile=os.getenv("NEXTDNS_PROFILE"),
    )

    start_http_server(port=EXPORTER_PORT, addr="0.0.0.0")
    while True:
        json = nextdns.analytics_status(p_from=METRICS_FROM, p_to=METRICS_TO)
        logging.info("%s:%s", datetime.now(), json)
        time.sleep(POLLING_INTERVAL)
