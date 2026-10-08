import io
import os
import urllib.parse
import boto3
from PIL import Image
from reportlab.pdfgen import canvas

s3 = boto3.client("s3")

INPUT_PREFIX = "input/"
OUTPUT_PREFIX = "output/"
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg")


def create_pdf(image_bytes: bytes) -> bytes:
    image = Image.open(io.BytesIO(image_bytes))
    image.verify()

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size

    output = io.BytesIO()
    pdf = canvas.Canvas(output, pagesize=(width, height))
    pdf.drawInlineImage(image, 0, 0, width=width, height=height)
    pdf.save()
    return output.getvalue()


def lambda_handler(event, context):
    processed = 0

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        if not key.startswith(INPUT_PREFIX):
            continue

        if not key.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        response = s3.get_object(Bucket=bucket, Key=key)
        pdf_bytes = create_pdf(response["Body"].read())

        filename = os.path.basename(key)
        pdf_name = os.path.splitext(filename)[0] + ".pdf"
        output_key = OUTPUT_PREFIX + pdf_name

        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=pdf_bytes,
            ContentType="application/pdf",
        )

        print(f"Converted s3://{bucket}/{key} -> s3://{bucket}/{output_key}")
        processed += 1

    return {"statusCode": 200, "processed": processed}
