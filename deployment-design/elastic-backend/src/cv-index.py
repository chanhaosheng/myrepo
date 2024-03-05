import csv
import logging

import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from omegaconf import DictConfig, OmegaConf

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_config() -> DictConfig:
    """Load the application configuration from a YAML file.

    Returns:
        DictConfig: Loaded configuration object.
    """
    config_path = "elastic-backend/conf/config.yaml"
    return OmegaConf.load(config_path)


def create_index(client, config: DictConfig):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index=config.index,
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "filename": {"type": "keyword"},
                    "text": {"type": "text"},
                    "up_votes": {"type": "integer"},
                    "down_votes": {"type": "integer"},
                    "age": {"type": "keyword"},
                    "gender": {"type": "keyword"},
                    "accent": {"type": "keyword"},
                    "duration": {"type": "float"},
                    "generated_text": {"type": "text"},
                    "suggest": {"type": "completion"},
                }
            },
        },
        ignore=400,
    )


def generate_actions(config: DictConfig):
    """Reads the file through csv.DictReader() and for each row
    yields a single document. This function is passed into the bulk()
    helper to create many documents in sequence.
    """
    with open(config.DATASET_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            doc = {key: row[key] for key in reader.fieldnames if row[key]}
            yield {"_index": "cv-transcriptions", "_source": doc}


def main(config: DictConfig):
    logging.info("Creating an index...")
    client = Elasticsearch([config.elasticsearch_site])
    create_index(client, config)

    logging.info("Indexing documents...")
    number_of_docs = sum(1 for _ in open(config.DATASET_PATH)) - 1
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, _ in streaming_bulk(
        client=client,
        index=config.index,
        actions=generate_actions(config),
    ):
        progress.update(1)
        successes += ok
    logging.info(f"Indexed {successes}/{number_of_docs} documents")


if __name__ == "__main__":
    config = load_config()
    main(config)
