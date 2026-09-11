# ShopAI — AI-Powered Shopping Assistant

## Live Demo

### 🚀 [Open ShopAI](https://ai-powered-shopping-agent-frontend.onrender.com)

ShopAI is a full-stack **Agentic AI shopping assistant** that helps users discover products, filter products using natural language, compare ratings, search for similar products using images, and complete a conversational checkout workflow.

---

## Overview

Traditional shopping applications require users to search, apply filters, compare products, check ratings, and then proceed to checkout.

ShopAI combines these steps into a conversational AI experience.

For example:

```text
Find organic honey under $20
```

The agent interprets the request, identifies the relevant requirements, uses the required tools, searches the product database, retrieves ratings when needed, and returns suitable products.

The user can then continue the conversation:

```text
Which one has the highest rating?
```

and:

```text
Order number 1
```

---

## Key Features

### Natural-Language Product Search

Users can search using normal language instead of traditional search forms.

Examples:

```text
Find organic honey under $20
```

```text
Find organic snacks below $15
```

```text
Find products under $30
```

Supported requirements include:

- Product name
- Category
- Price
- Organic status
- Rating requirements

---

### Agentic AI

ShopAI uses a LangChain agent that can select and use backend tools based on the user's request.

```text
User Request
     ↓
LangChain Agent
     ↓
Understand Intent
     ↓
Select Tool
     ↓
Execute Tool
     ↓
Read Result
     ↓
Generate Response
```

---

### Product Ratings

The assistant can retrieve product ratings and use them when comparing products.

Example:

```text
Which organic honey has the highest rating?
```

---

### Image-Based Product Search

Users can upload a product image and search for similar products.

```text
Product Image
     ↓
Image Analysis
     ↓
Product Description
     ↓
Search Keywords
     ↓
Product Database
     ↓
Similar Products
```

---

### Conversational Checkout

Users can select a product through the conversation.

Example:

```text
Find organic honey under $20
```

```text
Order number 1
```

The checkout tool validates the selected product and creates an order in the database.

---

## System Architecture

```text
                         USER
                           |
                           v
                 +-------------------+
                 | React Frontend    |
                 |      + Vite       |
                 +---------+---------+
                           |
                      HTTP / REST
                           |
                           v
                 +-------------------+
                 | FastAPI Backend   |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | LangChain Agent   |
                 +---------+---------+
                           |
            +--------------+--------------+
            |              |              |
            v              v              v
       Search Tool    Rating Tool    Checkout Tool
            |              |              |
            +--------------+--------------+
                           |
                           v
                    SQLite Database
                           |
                           v
                    Groq / Qwen LLM
```

---

## Main AI Tools

### `search_products`

Searches products using:

```text
query
max_price
is_organic
```

### `get_rating`

Retrieves rating information for a product.

### `checkout`

Validates the selected product and creates an order.

### `describe_product_image`

Analyzes an uploaded product image and generates product information for searching.

---

## Application Workflow

### Product Search

```text
User
 ↓
Natural-Language Request
 ↓
FastAPI
 ↓
LangChain Agent
 ↓
search_products
 ↓
SQLite
 ↓
Product Results
 ↓
User
```

### Rating Search

```text
User Request
 ↓
Search Products
 ↓
Get Product Ratings
 ↓
Compare Results
 ↓
Recommendation
```

### Checkout

```text
User Selection
 ↓
Product ID
 ↓
Checkout Tool
 ↓
Validate Product
 ↓
Create Order
 ↓
Order Confirmation
```

### Image Search

```text
Upload Image
 ↓
FastAPI
 ↓
Vision-capable Model
 ↓
Product Description
 ↓
Product Search
 ↓
Similar Products
```

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- Lucide React
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- SQLite

### AI

- LangChain
- LangGraph
- LangChain Groq
- Groq API
- Qwen model

### Deployment

- GitHub
- Render

---

## Project Structure

```text
ai-powered-shopping-agent/
│
├── backend/
│   ├── main.py
│   ├── shopping_agent.py
│   ├── reviews_api.py
│   ├── setup_db.py
│   ├── requirements.txt
│   └── store.db
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   │
│   └── src/
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── Sidebar.jsx
│       │   ├── ChatMessage.jsx
│       │   ├── ImageUploadModal.jsx
│       │   └── TypingIndicator.jsx
│       │
│       ├── services/
│       │   └── api.js
│       │
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css
│
├── .gitignore
└── README.md
```

---

## API

### `GET /`

Checks whether the backend is running.

### `GET /health`

Returns backend health status.

Example:

```json
{
  "status": "ok"
}
```

### `POST /chat`

Handles conversational shopping requests.

Request data includes:

```text
message
history
```

### `POST /image-search`

Accepts a product image and runs the image-search workflow.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Satish7261/ai-powered-shopping-agent.git
cd ai-powered-shopping-agent
```

### 2. Backend

```bash
cd backend
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create:

```text
backend/.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key
```

Run:

```powershell
uvicorn main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

---

### 3. Frontend

Open another terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_URL=http://localhost:8000
```

Run:

```powershell
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## Environment Variables

### Backend

```env
GROQ_API_KEY=your_groq_api_key
```

### Frontend

Local:

```env
VITE_API_URL=http://localhost:8000
```

Production:

```env
VITE_API_URL=https://ai-powered-shopping-agent-backend.onrender.com
```

Never commit API keys or `.env` files to the public repository.

---

## Deployment

The application is deployed as two services on Render.

```text
GitHub Repository
       |
       +-----------------------+
       |                       |
       v                       v
Frontend                    Backend
Render Static Site          Render Web Service
       |                       |
       v                       v
React + Vite                FastAPI
                               |
                               v
                         LangChain Agent
```

### Frontend

```text
Root Directory:
frontend

Build Command:
npm install && npm run build

Publish Directory:
dist
```

### Backend

```text
Root Directory:
backend

Build Command:
pip install -r requirements.txt

Start Command:
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Example Conversation

```text
User:
Find organic honey under $20
```

ShopAI:

```text
#1. Organic Raw Honey (ID:1) — $14.99 ★4.62 — organic

#2. Organic Acacia Honey (ID:7) — $17.99 ★4.75 — organic

#3. Organic Buckwheat Honey (ID:5) — $18.99 ★4.62 — organic
```

User:

```text
Which one has the highest rating?
```

ShopAI uses the rating information to compare the products.

User:

```text
Order number 1
```

The checkout workflow identifies the selected product and creates the order.

---

## Database

The application currently uses SQLite.

The main data areas are:

```text
Products
Reviews
Orders
```

### Products

```text
id
name
description
category
price
is_organic
```

### Reviews

Used by the rating workflow to retrieve product rating information.

### Orders

Used by the checkout workflow to store order information.

---

## Engineering Approach

The project separates AI reasoning from application operations.

```text
LLM Agent
    ↓
Decides what action is required
    ↓
Backend Tool
    ↓
Performs controlled operation
    ↓
Database / Model
    ↓
Result returned to Agent
```

This keeps database operations and business logic inside backend tools instead of allowing the model to directly manipulate application state.

---

## Why This Project Is Agentic

A simple chatbot:

```text
User
 ↓
LLM
 ↓
Text Response
```

ShopAI:

```text
User
 ↓
Agent
 ↓
Intent Understanding
 ↓
Tool Selection
 ↓
Tool Execution
 ↓
Tool Result
 ↓
Final AI Response
```

The agent can therefore participate in an actual application workflow rather than only generating text.

---

## Security

The Groq API key is stored on the backend as an environment variable.

The frontend communicates with the backend rather than directly exposing the LLM credential.

Do not:

- Commit `.env`
- Hard-code API keys
- Put API keys in frontend code
- Upload secrets to GitHub
- Share secrets in screenshots

---

## Current Limitations

This is a portfolio/demo application rather than a production e-commerce platform.

Current limitations include:

- SQLite instead of a managed production database
- No real payment processing
- No full user authentication system
- No production inventory management
- No real shipping integration
- Free-tier hosting limitations

---

## Future Improvements

- PostgreSQL for persistent production data
- User authentication
- Shopping cart
- Order history
- Real payment integration
- Inventory management
- Personalized recommendations
- Semantic/vector search
- Improved image similarity search
- Automated testing
- CI/CD
- Monitoring and observability

---

## Project Highlights

This project demonstrates practical experience with:

```text
Agentic AI
LLM Integration
Tool Calling
LangChain
Groq / Qwen
Python
FastAPI
React
Vite
SQLite
REST APIs
Image Search
Conversational Checkout
GitHub
Render
```

---

## Project Status

The application currently includes:

- Natural-language product search
- Price filtering
- Organic filtering
- Product ratings
- Product comparison
- Image-based product search
- Conversation history
- Product selection
- Checkout workflow
- SQLite order storage
- React frontend
- FastAPI backend
- LangChain agent
- Cloud deployment

---

## Author

**Satish Kumar**

GitHub:

https://github.com/Satish7261

---

# 🚀 Live Demo

## [Open ShopAI](https://ai-powered-shopping-agent-frontend.onrender.com)

**Search smarter. Compare better. Shop with AI.**