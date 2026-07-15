"""
lambda_function.py

Minimal Morning Brief Lambda for Python 3.10.

- Gera um texto simples com data, previsão, manchetes, agenda e motivação.
- Salva em S3 como morning_brief_YYYYMMDD.txt.
- Retorna JSON com statusCode e s3_key.
- Optional: stub para envio por SES se variáveis EMAIL_* estiverem configuradas.
"""

import os
import json
import logging
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment
BUCKET_NAME = os.environ.get("BUCKET_NAME")
REGION = os.environ.get("REGION", "us-east-1")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_TO = os.environ.get("EMAIL_TO")

s3 = boto3.client("s3", region_name=REGION)
ses = boto3.client("ses", region_name=REGION)

def build_brief(now: datetime) -> str:
    date_str = now.strftime("%Y-%m-%d")
    brief_lines = [
        f"Morning Brief {date_str}",
        "",
        "Previsão: Ensolarado 25-30°C.",
        "Notícias: Manchete A; Manchete B.",
        "Agenda: 09:00 Reunião; 14:00 Revisão.",
        "Motivação: Faça uma pequena tarefa importante.",
        ""
    ]
    return "\n".join(brief_lines)

def upload_to_s3(bucket: str, key: str, content: str) -> None:
    s3.put_object(Bucket=bucket, Key=key, Body=content.encode("utf-8"))
    logger.info("Uploaded to s3://%s/%s", bucket, key)

def send_email(subject: str, body: str) -> dict:
    if not (EMAIL_FROM and EMAIL_TO):
        logger.info("EMAIL_FROM or EMAIL_TO not configured; skipping email.")
        return {"status": "no-email-config"}

    try:
        response = ses.send_email(
            Source=EMAIL_FROM,
            Destination={"ToAddresses": [EMAIL_TO]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}}
            }
        )
        logger.info("Email sent: %s", response.get("MessageId"))
        return {"status": "sent", "message_id": response.get("MessageId")}
    except ClientError as e:
        logger.exception("Failed to send email: %s", e)
        return {"status": "error", "error": str(e)}

def lambda_handler(event, context):
    now = datetime.utcnow()
    date_key = now.strftime("%Y%m%d")
    filename = f"morning_brief_{date_key}.txt"
    s3_key = filename

    if not BUCKET_NAME:
        logger.error("BUCKET_NAME environment variable is not set.")
        return {"statusCode": 500, "body": json.dumps({"error": "BUCKET_NAME not set"})}

    content = build_brief(now)

    try:
        upload_to_s3(BUCKET_NAME, s3_key, content)
    except ClientError as e:
        logger.exception("S3 upload failed: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": "s3_upload_failed", "details": str(e)})}

    email_result = send_email(f"Morning Brief {now.strftime('%Y-%m-%d')}", content)

    result = {"s3_key": s3_key, "email_result": email_result}
    logger.info("Lambda completed successfully: %s", result)

    return {"statusCode": 200, "body": json.dumps(result)}
