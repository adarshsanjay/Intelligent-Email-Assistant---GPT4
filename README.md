# Intelligent Email Assistant - Streamlit

## Requirements

- macOS
- Python 3.11/3.12 recommended
- VS Code
- Ollama
- Llama 3.2

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2
```

## Run Streamlit

```bash
streamlit run app.py
```

The browser will open the Streamlit application, normally at:
http://localhost:8501

## Workflow

1. Enter Customer Name.
2. Enter Email Subject.
3. Enter Customer Email.
4. Click Analyze Email & Generate Reply.
5. The app detects intent using Ollama.
6. Historical emails are searched using TF-IDF + cosine similarity.
7. Ollama generates a professional reply.
8. The reply is rewritten in Friendly/Formal/Empathetic tone.
9. A 50-word summary is generated.
10. Save the final result to generated_reply.txt.

## Dataset

The provided 100-record Excel dataset has been converted to:

data/emails.csv
