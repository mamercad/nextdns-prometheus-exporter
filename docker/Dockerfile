FROM python:3.9-slim
COPY prometheus-nextdns-exporter.py /
COPY requirements.txt /
RUN pip install --upgrade pip \
    && pip3 install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "prometheus-nextdns-exporter.py" ]
