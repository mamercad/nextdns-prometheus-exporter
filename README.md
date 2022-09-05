# Prometheus Exporter for [NextDNS](https://nexdns.io)

[![docker-image](https://github.com/mamercad/nextdns-prometheus-exporter/actions/workflows/docker-image.yml/badge.svg)](https://github.com/mamercad/nextdns-prometheus-exporter/actions/workflows/docker-image.yml)

[Prometheus](https://prometheus.io) metrics of your [NextDNS](https://nexdns.io) data.

There's Docker stuff [here](./docker), Kubernetes stuff [here](./kubernetes), and SystemD stuff [here](./systemd).

It behaves like this:

```bash
❯ curl -s 192.168.1.181:8000 | grep ^nextdns
nextdns_total_queries 6358.0
nextdns_allowed_queries 1258.0
nextdns_blocked_queries 4527.0
```

You'll need to set `$NEXTDNS_API_KEY` and `$NEXTDNS_PROFILE`, you can find information on the NextDNS API [here](https://nextdns.github.io/api/).
