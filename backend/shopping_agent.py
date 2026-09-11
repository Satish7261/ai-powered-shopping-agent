import base64
import json
import os
import sqlite3
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

from reviews_api import get_product_rating
from setup_db import create_database


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# DATABASE PATH
# ============================================================

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "store.db"
)


# ============================================================
# CREATE DATABASE
# ============================================================

create_database()


# ============================================================
# LANGUAGE MODELS
# ============================================================

llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0,
    max_tokens=800
)

vision_llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0,
    max_tokens=800
)


# ============================================================
# TOOL 1: SEARCH PRODUCTS
# ============================================================

@tool
def search_products(
    query: str,
    max_price: Any = None,
    is_organic: Any = None,
):
    """
    Search products in the store.

    query:
        Product name, category, description, or keyword.

    max_price:
        Maximum price. The AI may send this as a number,
        string, or null.

    is_organic:
        Organic filter. The AI may send this as a boolean,
        string, number, or null.
    """

    # --------------------------------------------------------
    # NORMALIZE MAX PRICE
    # --------------------------------------------------------

    price_value = None

    if max_price is not None:

        try:

            if isinstance(max_price, str):

                price_text = max_price.strip()

                if price_text.lower() not in [
                    "",
                    "none",
                    "null",
                ]:

                    price_value = float(
                        price_text
                    )

            else:

                price_value = float(
                    max_price
                )

        except (
            ValueError,
            TypeError,
        ):

            price_value = None


    # --------------------------------------------------------
    # NORMALIZE ORGANIC VALUE
    # --------------------------------------------------------

    organic_value = None

    if is_organic is not None:

        # Boolean
        if isinstance(
            is_organic,
            bool
        ):

            organic_value = is_organic


        # Number
        elif isinstance(
            is_organic,
            (int, float)
        ):

            organic_value = (
                bool(is_organic)
            )


        # String
        elif isinstance(
            is_organic,
            str
        ):

            organic_text = (
                is_organic
                .strip()
                .lower()
            )

            if organic_text in [
                "true",
                "yes",
                "1",
                "organic",
            ]:

                organic_value = True

            elif organic_text in [
                "false",
                "no",
                "0",
                "non-organic",
                "nonorganic",
            ]:

                organic_value = False


    # --------------------------------------------------------
    # NORMALIZE QUERY
    # --------------------------------------------------------

    search_query = str(
        query
    ).strip().lower()


    # --------------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------------

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()


    # --------------------------------------------------------
    # SQL QUERY
    # --------------------------------------------------------

    sql = """
        SELECT
            id,
            name,
            description,
            category,
            price,
            is_organic
        FROM products
        WHERE (
            LOWER(name) LIKE ?
            OR LOWER(description) LIKE ?
            OR LOWER(category) LIKE ?
        )
    """


    search_term = (
        f"%{search_query}%"
    )


    params = [
        search_term,
        search_term,
        search_term,
    ]


    # --------------------------------------------------------
    # PRICE FILTER
    # --------------------------------------------------------

    if price_value is not None:

        sql += """
            AND price <= ?
        """

        params.append(
            price_value
        )


    # --------------------------------------------------------
    # ORGANIC FILTER
    # --------------------------------------------------------

    if organic_value is not None:

        sql += """
            AND is_organic = ?
        """

        params.append(
            1 if organic_value else 0
        )


    # --------------------------------------------------------
    # SORT PRODUCTS
    # --------------------------------------------------------

    sql += """
        ORDER BY price ASC
    """


    # --------------------------------------------------------
    # EXECUTE
    # --------------------------------------------------------

    cursor.execute(
        sql,
        params
    )


    rows = cursor.fetchall()


    conn.close()


    # --------------------------------------------------------
    # BUILD PRODUCT LIST
    # --------------------------------------------------------

    products = []


    for row in rows:

        products.append(
            {
                "product_id": row[0],
                "name": row[1],
                "description": row[2],
                "category": row[3],
                "price": row[4],
                "is_organic": bool(
                    row[5]
                ),
            }
        )


    # --------------------------------------------------------
    # RETURN JSON
    # --------------------------------------------------------

    return json.dumps(
        products,
        indent=2
    )


# ============================================================
# TOOL 2: GET PRODUCT RATING
# ============================================================

@tool
def get_rating(
    product_id: int
):
    """
    Get the average rating and review count
    for a product.
    """

    return get_product_rating(
        product_id
    )


# ============================================================
# TOOL 3: CHECKOUT
# ============================================================

@tool
def checkout(
    product_id: int
):
    """
    Place an order for a product.

    This should only be called after the user explicitly
    confirms that they want to purchase the product.
    """

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()


    # --------------------------------------------------------
    # FIND PRODUCT
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            id,
            name,
            price
        FROM products
        WHERE id = ?
        """,
        (
            product_id,
        )
    )


    product = cursor.fetchone()


    if not product:

        conn.close()

        return (
            f"Product ID {product_id} "
            "was not found."
        )


    product_id_value = product[0]
    product_name = product[1]
    product_price = product[2]


    # --------------------------------------------------------
    # CREATE ORDER
    # --------------------------------------------------------

    cursor.execute(
        """
        INSERT INTO orders
        (
            product_id
        )
        VALUES
        (?)
        """,
        (
            product_id_value,
        )
    )


    conn.commit()


    order_id = cursor.lastrowid


    conn.close()


    # --------------------------------------------------------
    # CONFIRM ORDER
    # --------------------------------------------------------

    return (
        f"Order confirmed! "
        f"Order ID: {order_id}. "
        f"Product: {product_name}. "
        f"Price: ${product_price}."
    )


# ============================================================
# TOOL 4: DESCRIBE PRODUCT IMAGE
# ============================================================

@tool
def describe_product_image(
    image_path: str
):
    """
    Analyze a product image and return a description
    that can be used for product search.
    """

    # --------------------------------------------------------
    # CHECK IMAGE
    # --------------------------------------------------------

    if not os.path.exists(
        image_path
    ):

        return json.dumps(
            {
                "error": (
                    "Image file not found."
                )
            }
        )


    # --------------------------------------------------------
    # READ IMAGE
    # --------------------------------------------------------

    with open(
        image_path,
        "rb"
    ) as image_file:

        image_bytes = (
            image_file.read()
        )


    # --------------------------------------------------------
    # BASE64 ENCODE
    # --------------------------------------------------------

    encoded_image = (
        base64.b64encode(
            image_bytes
        ).decode(
            "utf-8"
        )
    )


    # --------------------------------------------------------
    # IMAGE TYPE
    # --------------------------------------------------------

    extension = (
        os.path.splitext(
            image_path
        )[1]
        .lower()
    )


    if extension == ".png":

        mime_type = "image/png"

    elif extension == ".webp":

        mime_type = "image/webp"

    else:

        mime_type = "image/jpeg"


    # --------------------------------------------------------
    # VISION MESSAGE
    # --------------------------------------------------------

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": """
Analyze this product image.

Identify:

1. Product type
2. Brand if visible
3. Product name if visible
4. Main characteristics
5. Useful search keywords

Return a concise description that can be
used to search products in a store.
""",
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": (
                        f"data:{mime_type};base64,"
                        f"{encoded_image}"
                    )
                },
            },
        ]
    )


    # --------------------------------------------------------
    # CALL VISION MODEL
    # --------------------------------------------------------

    response = vision_llm.invoke(
        [message]
    )


    # --------------------------------------------------------
    # RETURN DESCRIPTION
    # --------------------------------------------------------

    return json.dumps(
        {
            "description": (
                response.content
            )
        },
        indent=2
    )


# ============================================================
# TOOLS
# ============================================================

tools = [
    search_products,
    get_rating,
    checkout,
    describe_product_image,
]


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are ShopAI, an intelligent shopping assistant.

Your job is to help users search products, compare products,
check ratings, and place orders.

============================================================
SEARCHING PRODUCTS
============================================================

When the user asks to find or recommend products:

1. Use search_products.
2. Extract the product they want.
3. Extract price requirements.
4. Extract organic/non-organic requirements.
5. Search the store.
6. Use get_rating for relevant products.
7. Compare the results.

Do not place an order while the user is browsing.

============================================================
PRICE
============================================================

If the user says:

"under $20"
"below $30"
"less than $50"

pass the maximum price to search_products.

The max_price parameter accepts numbers, strings,
or null.

============================================================
ORGANIC
============================================================

If the user asks for organic products,
set is_organic to true.

If the user asks for non-organic products,
set is_organic to false.

The is_organic parameter accepts boolean,
string, number, or null.

============================================================
RATINGS
============================================================

If the user asks for a rating requirement such as:

"4.5+ rating"
"above 4 stars"
"highly rated"

first search for products.

Then use get_rating for the returned products.

Only show products that satisfy the requested rating
when possible.

============================================================
PRODUCT DISPLAY
============================================================

Display products using this format:

#1. Product Name (ID:PRODUCT_ID) — $PRICE ★RATING — organic

#2. Product Name (ID:PRODUCT_ID) — $PRICE ★RATING — non-organic

Use real values returned by the tools.

Never invent product IDs, prices, ratings, or products.

============================================================
IMAGE SEARCH
============================================================

When the user provides a product image:

1. Use describe_product_image.
2. Understand the product.
3. Search for similar products.
4. Get ratings.
5. Display relevant results.

============================================================
CHECKOUT
============================================================

NEVER call checkout while the user is only browsing.

Only call checkout when the user explicitly confirms
that they want to purchase a product.

Examples:

"Buy product 3"
"Order product 5"
"Yes, buy it"
"I want to purchase ID 10"
"Checkout product 2"

Always use the correct product ID.

============================================================
GENERAL BEHAVIOR
============================================================

Be friendly and concise.

Do not expose internal tool details.

Do not make up information.

Use the database and tool results as the source
of product information.
"""


# ============================================================
# CREATE AGENT
# ============================================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Find organic honey "
                        "under $20"
                    ),
                }
            ]
        }
    )


    print()
    print("=" * 70)
    print("SHOPAI RESPONSE")
    print("=" * 70)

    print(
        result["messages"][-1].content
    )

    print("=" * 70)

