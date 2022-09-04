FROM python:3.9-slim
COPY prometheus_nextdns_exporter.py /
COPY requirements.txt /
RUN pip install --upgrade pip \
    && pip3 install --requirement requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "prometheus_nextdns_exporter.py" ]
