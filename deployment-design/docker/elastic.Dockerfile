FROM elasticsearch:8.12.2

COPY elastic-backend/elasticsearch.yaml /opt/elasticsearch/config/elasticsearch.yml
CMD service elasticsearch start && /bin/bash