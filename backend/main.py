import os
import tempfile

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
    Safely extract the last non-empty text response
    from the LangChain agent messages.
    """

    messages = result.get("messages", [])

    for message in reversed(messages):
        content = getattr(message, "content", None)

        if not content:
            continue

        # Normal string response
        if isinstance(content, str):
            if content.strip():
                return content.strip()

        # Some LangChain/Groq responses can return content blocks
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