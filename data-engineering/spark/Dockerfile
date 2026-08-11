FROM bitnami/spark:3.5

USER root
RUN pip install --no-cache-dir psycopg2-binary==2.9.9
USER 1001

WORKDIR /opt/spark-apps
COPY shipment_stream.py .
RUN mkdir -p /tmp/cargopulse-checkpoints

CMD ["spark-submit", "--master", "spark://spark:7077", "shipment_stream.py"]
