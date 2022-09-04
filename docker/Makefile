.PHONY: requirements
requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: build
build:
	docker build -t ghcr.io/mamercad/nextdns-prometheus-exporter:devel .

.PHONY: run
run:
	docker run --rm -it -p 8000:8000/tcp \
		-e NEXTDNS_API_KEY -e NEXTDNS_PROFILE \
		ghcr.io/mamercad/nextdns-prometheus-exporter:devel
