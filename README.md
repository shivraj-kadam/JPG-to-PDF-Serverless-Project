# JPG to PDF Serverless Project

A serverless AWS project that automatically converts JPG/JPEG images uploaded to Amazon S3 into PDF files using AWS Lambda, Pillow, and ReportLab.

## Architecture

```
User uploads JPG
      |
      v
Amazon S3 (input/)
      |
      | ObjectCreated event
      v
AWS Lambda
  |        |
  |        +--> Pillow (image processing)
  |
  +-----------> ReportLab (PDF generation)
      |
      v
Amazon S3 (output/)
      |
      v
Generated PDF
```

## AWS Services Used

- Amazon S3 — stores input images and generated PDFs
- AWS Lambda — serverless conversion logic
- IAM — permissions for S3 access and Lambda execution
- AWS SAM — infrastructure/deployment template
- Pillow — image processing
- ReportLab — PDF generation

## Project Structure

```
.
├── src/
│   └── lambda_function.py
├── layer/
│   ├── pillow/python/
│   └── reportlab/python/
├── scripts/
│   ├── build_layers.sh
│   └── deploy.sh
├── docs/
│   └── architecture.md
├── data/
│   ├── input/
│   └── output/
├── template.yaml
├── .gitignore
└── LICENSE
```

## How It Works

1. Upload a JPG/JPEG image into the S3 `input/` prefix.
2. S3 sends an ObjectCreated notification to Lambda.
3. Lambda downloads the image.
4. Pillow validates and converts the image to RGB.
5. ReportLab creates a PDF with the image dimensions.
6. Lambda uploads the PDF to the S3 `output/` prefix.
7. The Lambda event is restricted to `input/` so generated PDFs do not recursively trigger the function.

## Prerequisites

- AWS account
- AWS CLI configured
- Python 3.13
- AWS SAM CLI
- Docker recommended for Lambda-compatible dependency builds

## Local Setup

Install the application dependencies for development:

```bash
pip install Pillow reportlab boto3
```

Build the Lambda layers:

```bash
chmod +x scripts/build_layers.sh
./scripts/build_layers.sh
```

Build and deploy with SAM:

```chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

Or run:

```bash
sam build
sam deploy --guided
```

## Testing

After deployment, upload an image:

```bash
aws s3 cp sample.jpg s3://YOUR-BUCKET/input/sample.jpg
```

Then check the generated PDF:

```bash
aws s3 ls s3://YOUR-BUCKET/output/
```

Download it:

```bash
aws s3 cp s3://YOUR-BUCKET/output/sample.pdf ./sample.pdf
```

View Lambda logs:

```bash
sam logs -n ImagePdfFunction --stack-name YOUR-STACK-NAME --tail
```

## Security Notes

- Keep S3 access limited to the Lambda execution role.
- Do not commit AWS access keys, secret keys, `.env` files, or SAM deployment secrets.
- Use least-privilege IAM permissions where possible.

## Learning Outcomes

This project demonstrates practical experience with:

- Serverless architecture
- AWS S3 event notifications
- AWS Lambda
- IAM permissions
- Python Lambda development
- Image processing with Pillow
- PDF generation with ReportLab
- AWS SAM infrastructure as code
- AWS CLI deployment and testing

## Author

**Shivraj Kadam**

GitHub: [shivraj-kadam](https://github.com/shivraj-kadam)
