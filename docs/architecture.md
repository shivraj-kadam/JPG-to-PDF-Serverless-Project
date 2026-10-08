# Architecture

The project uses an event-driven serverless workflow.

1. A user uploads a JPG/JPEG file to the S3 `input/` prefix.
2. Amazon S3 emits an ObjectCreated event.
3. AWS Lambda receives the event.
4. Lambda downloads the image from S3.
5. Pillow validates and converts the image to RGB.
6. ReportLab generates a PDF using the image dimensions.
7. Lambda stores the PDF under the S3 `output/` prefix.

## Flow

```
S3 input/ -> S3 Event -> Lambda -> Pillow -> ReportLab -> S3 output/
```

The S3 notification is limited to the `input/` prefix, preventing generated PDFs in `output/` from recursively invoking the function.
