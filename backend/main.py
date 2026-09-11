import os
import tempfile
import json

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from shopping_agent import agent


app = FastAPI(
    title="ShopAI API",
    description="AI Shopping Assistant Backend",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-powered-shopping-agent-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_response(result):
    """
    Safely extract and format the agent response.
    """

    messages = result.get("messages", [])

    for message in reversed(messages):
        content = getattr(message, "content", None)

        if not content:
            continue

        # If content is a normal string
        if isinstance(content, str):
            text = content.strip()

            if not text:
                continue

            # Check whether the agent returned JSON
            try:
                data = json.loads(text)

                if isinstance(data, list):
                    lines = []

                    for i, product in enumerate(data, start=1):
                        name = product.get(
                            "name",
                            "Unknown product"
                        )

                        price = product.get(
                            "price",
                            "N/A"
                        )

                        organic = (
                            "Organic"
                            if product.get("is_organic")
                            else "Non-organic"
                        )

                        lines.append(
                            f"{i}. {name} — ${price} — {organic}"
                        )

                    if lines:
                        return "\n".join(lines)

            except (json.JSONDecodeError, TypeError):
                pass

            return text

        # If content is returned as blocks
        if isinstance(content, list):
            text_parts = []

            for block in content:

                if isinstance(block, str):
                    text_parts.append(block)

                elif isinstance(block, dict):
                    text = block.get("text")

                    if text:
                        text_parts.append(text)

            response = "".join(text_parts).strip()

            if response:
                return response

    return "I couldn't generate a response. Please try again."


@app.get("/")
def root():

    return {
        "message": "ShopAI API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(
    message: str = Form(...)
):

    try:

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            }
        )

        response = extract_response(result)

        return {
            "success": True,
            "response": response
        }

    except Exception as e:

        return {
            "success": False,
            "response": f"Error: {str(e)}"
        }


@app.post("/image-search")
async def image_search(
    file: UploadFile = File(...)
):

    suffix = (
        os.path.splitext(
            file.filename
        )[1]
        or ".jpg"
    )

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:

            tmp.write(
                await file.read()
            )

            temp_path = tmp.name

        prompt = (
            "I uploaded a product image. "
            "Please analyze it and find similar "
            "products in the store. "
            f"Image path: {temp_path}"
        )

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        response = extract_response(result)

        return {
            "success": True,
            "response": response
        }

    except Exception as e:

        return {
            "success": False,
            "response": f"Image analysis error: {str(e)}"
        }

    finally:

        if temp_path and os.path.exists(
            temp_path
        ):
            os.remove(temp_path)