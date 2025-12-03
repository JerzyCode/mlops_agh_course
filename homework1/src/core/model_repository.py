import io

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


def load_classifier_s3(bucket: str, key: str):
    log.info("Loading text classifier from S3...")

    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=key)
    model = joblib.load(io.BytesIO(obj["Body"].read()))
    return model


def load_text_embedder_s3(bucket_name: str, key: str, path: str) -> SentenceTransformer:
    log.info("Loading text embedder from S3...")

    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    model = SentenceTransformer(io.BytesIO(obj["Body"].read()))
    # TODO

    return model
