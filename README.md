# 🛍️ ShopAI — AI Shopping Assistant

> An intelligent AI-powered shopping assistant that helps users discover,
> compare, and evaluate products using natural language and product images.

ShopAI combines **Generative AI, Agentic AI, LangChain, FastAPI, React, and SQLite**
to create a conversational shopping experience.

Users can describe what they are looking for in natural language, specify
constraints such as price and organic preferences, compare product ratings,
and search for similar products using an uploaded product image.

---

## ✨ Features

### 🤖 AI Shopping Agent

Interact with ShopAI using natural language.

Example:

> "Find organic honey under $20 with a rating above 4.5."

The AI understands the request and uses the available tools to search the
product database and evaluate the results.

### 🔎 Intelligent Product Search

Search products using:

- Product name
- Category
- Description
- Maximum price
- Organic / non-organic preference

### ⭐ Product Rating Analysis

ShopAI retrieves product ratings from the review database and uses them
to help users compare products.

### 🖼️ Image-Based Product Search

Upload a product image and the AI:

1. Analyzes the image using a vision-capable model
2. Identifies the product and useful characteristics
3. Generates search keywords
4. Searches the store database
5. Returns similar products

### 🛒 Checkout

The assistant can place an order after explicit user confirmation.

### 💬 Conversational Interface

A modern React-based interface provides:

- AI chat
- Product discovery
- Image upload
- Loading/typing indicators
- Connection status
- New chat functionality
- Responsive dark UI

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      User           │
                         │                     │
                         │  Text / Product     │
                         │       Image         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │      + Vite         │
                         └──────────┬──────────┘
                                    │
                             HTTP / REST API
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         │                     │
                         │  /chat              │
                         │  /image-search      │
                         │  /health            │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   LangChain Agent   │
                         │                     │
                         │  Tool Selection     │
                         │  Reasoning          │
                         │  Task Execution     │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │ Search Product │ │ Get Rating     │ │ Checkout       │
        │ Tool           │ │ Tool           │ │ Tool           │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │      SQLite         │
                         │                     │
                         │  Products           │
                         │  Reviews            │
                         │  Orders             │
                         └─────────────────────┘

                    Image Search Flow
                           │
                           ▼
                  ┌──────────────────┐
                  │ Vision-capable   │
                  │ LLM              │
                  └────────┬─────────┘
                           │
                           ▼
                  Product Description
                           │
                           ▼
                    Product Search