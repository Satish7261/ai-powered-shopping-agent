# 🛒 AI Shopping Assistant

An AI-powered shopping assistant built with **LangChain**, **LangGraph**, **Groq**, **Streamlit**, and **SQLite**. It helps users search products, compare ratings, analyze product images, and place orders through a conversational interface.

## 🚀 Live Demo

🔗 https://ai-shopping-assistant-km26ywqxc4gpjdmtfniqns.streamlit.app/

## ✨ Features

- 🔍 Search products using natural language
- ⭐ AI-powered product recommendations
- 🖼️ Product image analysis
- 💬 Customer review lookup
- 🛍️ Place orders through chat
- 💾 SQLite database integration
- 🎨 Interactive Streamlit interface

## 🛠️ Tech Stack

- Python
- LangChain
- LangGraph
- Groq
- Streamlit
- SQLite

## 📂 Project Structure

```text
AI-Shopping-Assistant/
│── app.py
│── shopping_agent.py
│── setup_db.py
│── reviews_api.py
│── requirements.txt
│── README.md
│── .env
```

## ⚙️ Installation

```bash
git clone https://github.com/Satish7261/AI-Shopping-Assistant.git
cd AI-Shopping-Assistant

python -m venv .venv
```

### Activate Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
```

### Run the Application

```bash
streamlit run app.py
```

## 💡 Example Queries

- I want to buy organic honey
- Show me the highest-rated coffee
- Recommend a product under $20
- Describe this product image
- Order product #2

## 👨‍💻 Author

**Satish**

GitHub: https://github.com/Satish7261

---

⭐ If you found this project useful, consider giving it a star!