# 🔥 RepoRoast

**RepoRoast** is a fun, AI-powered code reviewer. Paste a public GitHub repository URL and it analyzes your Python code, scores its health, lists issues and bug risks, and generates a witty Hinglish ("roast") review with improvement tips and a fixed code example.

> "We roast your code, so your interviewer doesn't have to."

---

## ✨ What it does

- 📥 Fetches repository metadata + Python files from GitHub via the GitHub API.
- 📊 Analyzes code quality:
  - Missing README penalty
  - Cyclomatic complexity (via `radon`)
  - Leftover `TODO`s, excessive `print()` statements
  - Bare `except:` blocks
  - Monolithic files (>800 lines)
- 🤖 Generates an AI roast (one-liner + improvement tips + fixed example) using OpenRouter.
- 🎨 Streamlit UI to paste a repo link and view results.

---

## 🏗️ Tech Stack

| Layer     | Tech                                  |
|-----------|---------------------------------------|
| Backend   | FastAPI, Uvicorn                      |
| Frontend  | Streamlit                             |
| Analysis  | radon (cyclomatic complexity)         |
| AI        | OpenRouter (OpenAI-compatible API)    |
| GitHub    | requests (GitHub REST API)            |
| Config    | python-dotenv                         |

---

## 📁 Project Structure

```
repo-roast/
├── backend/
│   ├── main.py            # FastAPI app + /analyze endpoint
│   ├── analyzer.py        # Code analysis logic (score, issues, bug risks)
│   ├── ai_roaster.py      # OpenRouter AI roast generator
│   ├── github_fetcher.py  # GitHub repo fetcher + URL parser
│   └── scanners/          # (Phase 2) security scanners
├── frontend/
│   └── app.py             # Streamlit UI
├── requirements.txt
├── .env                   # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- A GitHub personal access token (optional, for higher rate limits)
- An OpenRouter API key (required for AI roast)

### 2. Clone & set up environment

```bash
git clone <your-repo-url>
cd repo-roast
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=xx-xx-xx-xxxxxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxx   # optional
```

> ⚠️ Never commit your `.env` file — it is already in `.gitignore`.

### 5. Run the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

API will be available at `http://localhost:8000` (docs at `/docs`).

### 6. Run the frontend

In a separate terminal:

```bash
streamlit run frontend/app.py
```

Open the URL shown (usually `http://localhost:8501`), paste a GitHub repo link, and click **Roast My Repo**.

---

## 🔌 API

### `GET /`
Health check — returns a welcome message.

### `GET /analyze?repo_url=...`
Analyzes a GitHub repository.

**Response:**
```json
{
  "repo": "owner/repo",
  "stars": 123,
  "file_count": 5,
  "has_readme": true,
  "total_lines": 450,
  "score": 75,
  "issues": ["..."],
  "bug_risks": ["..."],
  "roast": {
    "one_liner": "...",
    "improvements": ["tip1", "tip2", "tip3"],
    "fixed_example": "..."
  }
}
```

---

## 🧪 Testing

```bash
pytest backend/test_analyzer.py
```

---

## 🗺️ Roadmap

- Phase 1 — Base Roaster ✅
- Phase 2 — Security Scanner (coming soon)

---

## 📄 License

Add your license here.
