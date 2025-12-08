import os

import boto3
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from src.utils.logger import log


def load_text_embedder(path: str) -> SentenceTransformer:
    log.info("Loading text embedder...")
    model = SentenceTransformer(path)
    return model


def load_classifier(path: str) -> LogisticRegression:
    log.info("Loading text classifier...")
    return joblib.load(path)


def load_classifier_s3(bucket: str, key: str, path: str) -> LogisticRegression:
    log.info(f"Downloading classifier from S3: s3://{bucket}/{key}")

    os.makedirs(os.path.dirname(path), exist_ok=True)

    s3_client = boto3.client("s3")
    s3_client.download_file(bucket, key, path)

    log.info(f"Classifier downloaded to {path}")

    return load_classifier(path)


def load_text_embedder_s3(bucket_name: str, key: str, path: str) -> SentenceTransformer:
    log.info(f"Downloading sentence transformer from S3: s3://{bucket_name}/{key}")

    os.makedirs(path, exist_ok=True)
    s3_client = boto3.client("s3")

    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=key):
        if "Contents" in page:
            for obj in page["Contents"]:
                s3_key = obj["Key"]
                if s3_key.endswith("/"):
                    continue

                relative_path = s3_key.replace(key, "").lstrip("/")
                local_file = os.path.join(path, relative_path)

                os.makedirs(os.path.dirname(local_file), exist_ok=True)
                log.info(f"Downloading {s3_key} to {local_file}")
                s3_client.download_file(bucket_name, s3_key, local_file)

    log.info(f"Sentence transformer downloaded to {path}")
    return load_text_embedder(path)
