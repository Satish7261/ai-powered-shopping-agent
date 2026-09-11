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
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

        response = result[
            "messages"
        ][-1].content

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

        response = result[
            "messages"
        ][-1].content

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
