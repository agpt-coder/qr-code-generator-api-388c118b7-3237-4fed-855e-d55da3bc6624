import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.api_key_access_service
import project.authenticate_user_service
import project.generate_qr_code_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, StreamingResponse
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="QR Code Generator API 3",
    lifespan=lifespan,
    description="Based on the requirements provided and the research conducted, the task involves creating a web service using FastAPI that serves an endpoint to generate QR codes dynamically based on user inputs. Here's a comprehensive overview of the solution:\n\n1. **Technology Stack**:\n   - **Programming Language**: Python\n   - **API Framework**: FastAPI for handling web requests and responses\n   - **Database**: PostgreSQL for storing generated QR code images if necessary\n   - **ORM**: Prisma to interface with the database in a more developer-friendly way\n\n2. **Functional Requirements**:\n   - The endpoint accepts various data types as input, such as URLs, text, and contact information.\n   - Users can customize the QR code's size, color, and error correction level through query parameters or request body.\n   - The service generates a QR code image encoding the provided input data.\n   - The API returns the QR code image directly in the response in the user-specified format (PNG, SVG, etc.), leveraging FastAPI's capability to serve different content types including binary data for images.\n\n3. **Implementation Details**:\n   - Use the `qrcode` library (as per the research findings) to generate QR codes in Python. This library supports customization options like size, color, and error correction levels.\n   - For serving images in different formats, utilize FastAPI's `StreamingResponse` or `FileResponse` depending on whether images are generated on the fly or stored and then served.\n   - Error correction can be customized to the levels L, M, Q, H, with the default being L (low) if not specified. This feature increases the robustness of QR codes against partial damage.\n   - For optional storing of generated QR code images in PostgreSQL, use the BYTEA data type for storing image bytes. This involves converting images to a byte array before insertion.\n   - Regarding security and scalability, ensure proper input validation to protect against injection attacks and consider caching popular QR codes to reduce processing load.\n\nThis approach combines the power and simplicity of FastAPI with the versatility of PostgreSQL and the QR code generation capabilities of Python libraries to meet the project's needs.",
)


@app.post("/generate")
async def api_post_generate_qr_code(
    content: str,
    size: Optional[int],
    color: Optional[str],
    error_correction: Optional[str],
    format: str,
) -> StreamingResponse:
    """
    Generates a QR code based on the provided input and customization options.
    """
    try:
        res = project.generate_qr_code_service.generate_qr_code(
            content, size, color, error_correction, format
        )
        headers = {"Content-Disposition": f"attachment; filename={res.file_name}"}
        return StreamingResponse(
            content=res.data, media_type=res.media_type, headers=headers
        )
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )  # TODO(autogpt): Expression of type "Response" cannot be assigned to return type "StreamingResponse"


#     "Response" is incompatible with "StreamingResponse". reportReturnType


@app.post("/auth/login", response_model=project.authenticate_user_service.LoginResponse)
async def api_post_authenticate_user(
    username: str, password: str
) -> project.authenticate_user_service.LoginResponse | Response:
    """
    Handles user authentication and returns an access token.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(
            username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/auth/api_key", response_model=project.api_key_access_service.ApiKeyAccessResponse
)
async def api_get_api_key_access(
    api_key: str,
) -> project.api_key_access_service.ApiKeyAccessResponse | Response:
    """
    Validates an API key and returns successful access message.
    """
    try:
        res = await project.api_key_access_service.api_key_access(api_key)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
