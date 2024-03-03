import csv
import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


DATASET_PATH = "elastic-backend/data/cv-valid-dev-updated.csv"


def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index="cv-transcriptions",
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
                }
            },
        },
        ignore=400,
    )


def generate_actions():
    """Reads the file through csv.DictReader() and for each row
    yields a single document. This function is passed into the bulk()
    helper to create many documents in sequence.
    """
    with open(DATASET_PATH, mode="r", encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            doc = {key: row[key] for key in reader.fieldnames if row[key]}
            yield {"_index": "cv-transcriptions", "_source": doc}


def main():
    print("Creating an index...")
    client = Elasticsearch(["http://localhost:9200"])
    create_index(client)

    print("Indexing documents...")
    number_of_docs = sum(1 for _ in open(DATASET_PATH)) - 1
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, _ in streaming_bulk(
        client=client, index="cv-transcriptions", actions=generate_actions(),
    ):
        progress.update(1)
        successes += ok
    print(f"Indexed {successes}/{number_of_docs} documents")


if __name__ == "__main__":
    main()
