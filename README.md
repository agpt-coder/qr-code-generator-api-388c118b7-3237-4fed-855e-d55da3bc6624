---
date: 2024-04-15T18:03:53.200001
author: AutoGPT <info@agpt.co>
---

# QR Code Generator API 3

Based on the requirements provided and the research conducted, the task involves creating a web service using FastAPI that serves an endpoint to generate QR codes dynamically based on user inputs. Here's a comprehensive overview of the solution:

1. **Technology Stack**:
   - **Programming Language**: Python
   - **API Framework**: FastAPI for handling web requests and responses
   - **Database**: PostgreSQL for storing generated QR code images if necessary
   - **ORM**: Prisma to interface with the database in a more developer-friendly way

2. **Functional Requirements**:
   - The endpoint accepts various data types as input, such as URLs, text, and contact information.
   - Users can customize the QR code's size, color, and error correction level through query parameters or request body.
   - The service generates a QR code image encoding the provided input data.
   - The API returns the QR code image directly in the response in the user-specified format (PNG, SVG, etc.), leveraging FastAPI's capability to serve different content types including binary data for images.

3. **Implementation Details**:
   - Use the `qrcode` library (as per the research findings) to generate QR codes in Python. This library supports customization options like size, color, and error correction levels.
   - For serving images in different formats, utilize FastAPI's `StreamingResponse` or `FileResponse` depending on whether images are generated on the fly or stored and then served.
   - Error correction can be customized to the levels L, M, Q, H, with the default being L (low) if not specified. This feature increases the robustness of QR codes against partial damage.
   - For optional storing of generated QR code images in PostgreSQL, use the BYTEA data type for storing image bytes. This involves converting images to a byte array before insertion.
   - Regarding security and scalability, ensure proper input validation to protect against injection attacks and consider caching popular QR codes to reduce processing load.

This approach combines the power and simplicity of FastAPI with the versatility of PostgreSQL and the QR code generation capabilities of Python libraries to meet the project's needs.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'QR Code Generator API 3'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
