# 📚 Vectorless RAG — Academic Regulations Bot

A Telegram bot that answers questions about academic regulations using a **vectorless RAG** (Retrieval-Augmented Generation) pipeline. Instead of traditional vector embeddings, this project leverages [PageIndex](https://pageindex.ai) tree-based document indexing for fast, accurate retrieval.

---

## ✨ Features

- **Vectorless Retrieval** — No vector database needed. Uses PageIndex's tree index to locate relevant document sections.
- **Dual Answer Modes** — Users can switch between two modes via the `/mode` command:
  - 🤖 **RAG Mode** — LLM-guided tree search → section retrieval → grounded answer with citations (powered by Groq + Llama 3.3).
  - ⚡ **Chat API Mode** — Direct answer from PageIndex's built-in chat completions (Detailed, NoLLM).
- **Telegram Interface** — Clean bot experience with inline keyboard buttons and Markdown-formatted responses.
- **Rate Limit Handling** — Automatic retry with backoff for Groq API rate limits.

---

## 🏗️ Architecture

```
User Question (Telegram)
        │
        ▼
   ┌─────────┐
   │  /mode   │──► Chat API Mode ──► PageIndex Chat Completions ──► Answer
   └─────────┘
        │
        ▼ (RAG Mode)
   ┌─────────────────────┐
   │  1. Load Tree Index  │  ← PageIndex tree structure (cached)
   └──────────┬──────────┘
              ▼
   ┌─────────────────────┐
   │  2. LLM Tree Search  │  ← Groq identifies relevant node IDs
   └──────────┬──────────┘
              ▼
   ┌─────────────────────┐
   │  3. Node Retrieval   │  ← Fetch full content of matched sections
   └──────────┬──────────┘
              ▼
   ┌─────────────────────┐
   │  4. Answer Generation│  ← Groq generates cited, grounded answer
   └──────────┬──────────┘
              ▼
          📩 Answer
```

---

## 📂 Project Structure

```
vectorless-rag/
├── bot.py               # Telegram bot — entry point
├── src/
│   ├── client.py        # API clients & config (PageIndex, Groq, Bot Token)
│   ├── upload.py        # One-time script to upload & index a PDF
│   ├── chat_api.py      # Chat API mode — direct PageIndex answers
│   └── rag.py           # RAG mode — tree search + LLM answer generation
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A [PageIndex](https://pageindex.ai) API key
- A [Groq](https://console.groq.com) API key
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/vectorless-rag.git
cd vectorless-rag
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate        # Linux / macOS
myenv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
PAGEINDEX_API_KEY=your_pageindex_api_key_here
GROQ_API_KEY=your_groq_api_key_here
BOT_TOKEN=your_telegram_bot_token_here
```

### 5. Upload Your Document (One-Time)

Place your PDF in the project root, then run:

```bash
python -m src.upload
```

This submits the document to PageIndex and waits for the tree index to be built. Once complete, copy the printed `doc_id` and update `DOC_ID` in `src/client.py`.

### 6. Start the Bot

```bash
python bot.py
```

You should see:

```
🤖 Academic Regulations Bot is running... Press Ctrl+C to stop.
```

---

## 💬 Bot Commands

| Command  | Description                              |
|----------|------------------------------------------|
| `/start` | Welcome message and usage instructions   |
| `/help`  | Same as `/start`                         |
| `/mode`  | Choose between RAG and Chat API modes    |

Simply type any question to get an answer based on your uploaded document.

---

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

| Variable            | Description                          |
|---------------------|--------------------------------------|
| `PAGEINDEX_API_KEY` | Your PageIndex API key               |
| `GROQ_API_KEY`      | Your Groq API key for LLM inference  |
| `BOT_TOKEN`         | Telegram bot token from BotFather    |

The document ID (`DOC_ID`) is set in `src/client.py` after uploading your PDF.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
