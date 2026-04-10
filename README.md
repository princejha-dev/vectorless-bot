# 🌍 Multilingual Vectorless RAG — Academic Regulations Bot

A **5-language Telegram bot** that answers questions about academic regulations using a **vectorless RAG** (Retrieval-Augmented Generation) pipeline with automatic language detection and response generation. Instead of traditional vector embeddings, this project leverages [PageIndex](https://pageindex.ai) tree-based document indexing for fast, accurate retrieval.

**Supported Languages:** English | Hindi | Marathi | Tamil | Gujarati

---

## ✨ Features

- **🌐 5-Language Support** — Automatically detects and responds in the user's language (English, Hindi, Marathi, Tamil, Gujarati).
- **🔄 Smart Language Handling** — Detects user's language → Translates to English for retrieval → Generates answer in original language while preserving tone.
- **Vectorless Retrieval** — No vector database needed. Uses PageIndex's tree index to locate relevant document sections.
- **Dual Answer Modes** — Users can switch between two modes via the `/mode` command:
  - 🤖 **RAG Mode** — LLM-guided tree search → section retrieval → grounded answer with citations (powered by Groq + Llama 3.3).
  - ⚡ **Chat API Mode** — Direct answer from PageIndex's built-in chat completions (Detailed, NoLLM).
- **💬 Tone Preservation** — Maintains the user's original tone and intent across all language conversions.
- **📍 Accurate Citations** — All answers include section titles and page numbers for reference.
- **Telegram Interface** — Clean bot experience with inline keyboard buttons and Markdown-formatted responses.
- **⚡ Rate Limit Handling** — Automatic retry with backoff for Groq API rate limits.

---

## 🏗️ Architecture

```
User Question in Any Language (Telegram)
        │
        ▼
   ┌─────────────────────┐
   │ 1. Language Detection│  ← Identify user's language (en, hi, mr, ta, gu)
   └──────────┬──────────┘
              ▼
   ┌─────────────────────┐
   │ 2. Translate to EN   │  ← Convert to English for retrieval
   └──────────┬──────────┘
              ▼
   ┌─────────┐
   │  /mode   │──► Chat API Mode ──► PageIndex Answer ──► (Skip to step 6)
   └─────────┘
              │
        ▼ (RAG Mode)
   ┌─────────────────────┐
   │  3. Load Tree Index  │  ← PageIndex tree structure (cached)
   └──────────┬──────────┘
              ▼
   ┌─────────────────────┐
   │  4. LLM Tree Search  │  ← Groq identifies relevant node IDs (English query)
   └──────────┬──────────┘
              ▼
   ┌─────────────────────┐
   │  5. Node Retrieval   │  ← Fetch full content of matched sections
   └──────────┬──────────┘
              ▼
   ┌────────────────────────────────────┐
   │ 6. Answer Generation w/ Tone       │
   │    - Original query (preserve tone)│
   │    - EN translation (context)      │
   │    - Language instructions         │
   └──────────┬───────────────────────┘
              ▼
   ┌─────────────────────┐
   │ 7. Groq LLM Response│  ← Generates answer in user's language
   └──────────┬──────────┘
              ▼
          📩 Answer (in user's language)
```

---

## 📂 Project Structure

```
vectorless-rag/
├── bot.py               # Telegram bot — entry point
├── src/
│   ├── client.py        # API clients & config (PageIndex, Groq, Bot Token)
│   ├── lang.py          # 🌍 Language detection & translation (5 languages)
│   ├── upload.py        # One-time script to upload & index a PDF
│   ├── chat_api.py      # Chat API mode — direct PageIndex answers
│   └── rag.py           # RAG mode — tree search + multilingual answer generation
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
- Internet connection (for language detection and translation via deep-translator)

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

## 🌐 Language Support Details

### How It Works

1. **Detection** — When a user sends a question, the system automatically detects the language using `langdetect`.
2. **Translation** — If not in English, the question is translated to English using `deep-translator` for accurate document retrieval.
3. **Retrieval** — The English query is used to search the document tree via LLM-guided tree search.
4. **Response Generation** — The LLM receives:
   - The **English translation** (for context and retrieval)
   - The **original question** (to preserve tone and intent)
   - **Language instructions** (specific to the detected language)
   - **Document context** (retrieved sections)
5. **Answer** — The LLM generates a natural, fluent answer in the user's original language.

### Supported Languages

| Language   | Code | Example           |
|------------|------|-------------------|
| English    | `en` | "What is the exam policy?" |
| Hindi      | `hi` | "परीक्षा नीति क्या है?" |
| Marathi    | `mr` | "परीक्षा धोरण काय आहे?" |
| Tamil      | `ta` | "தேர்வு கொள்கை என்ன?" |
| Gujarati   | `gu` | "પરીક્ષા નીતિ શું છે?" |

---

## 📊 Technology Stack

- **Language Detection:** `langdetect` — Fast, accurate language identification
- **Translation:** `deep-translator` — Reliable, actively maintained translation service
- **Document Indexing:** [PageIndex](https://pageindex.ai) — Tree-based, vectorless document structure
- **LLM Integration:** [Groq](https://console.groq.com) — Fast inference with Llama 3.3 70B
- **Bot Framework:** `pyTelegramBotAPI` — Easy Telegram bot development

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
