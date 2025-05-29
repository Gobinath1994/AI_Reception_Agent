# 🤖 AI Receptionist Chatbot

An intelligent, voice- and text-enabled chatbot assistant designed for organizations with multiple business units. This assistant uses local large language models (like Mistral via LM Studio), offline speech-to-text using Whisper, and a sleek Gradio UI for interaction — all running 100% locally for privacy and control.

---

## 🏗️ Features

- ✅ Voice and text input via Gradio
- ✅ Offline Whisper-based audio transcription
- ✅ Integration with local Mistral model using LM Studio (OpenAI-compatible API)
- ✅ JSON-based FAQ knowledge base per brand or department
- ✅ Custom brand detection and contextual prompt generation
- ✅ Rasa backend for intent detection, routing, and fallback handling
- ✅ Fully Dockerized deployment with separate services for Rasa, Actions, and UI

---

## 📁 Project Structure

```
AI_Reception_Agent/
├── app.py                 # Gradio UI
├── agent.py               # Prompt router and LLM interface
├── actions.py             # Rasa custom action to call LLM
├── whisper_utils.py       # Whisper STT utilities
├── data/
│   └── faq_data.json      # Structured FAQ data per company
├── models/                # Rasa models (ignored in Git)
├── config.yml             # Rasa NLU pipeline configuration
├── domain.yml             # Intents, responses, actions
├── rules.yml              # Rule-based policy handling
├── rasa_requirements.txt  # Rasa-specific dependencies
├── requirements.txt       # General project requirements
├── Dockerfile             # Single Docker image definition
├── docker-compose.yml     # Multi-container setup
└── README.md              # This file
```

---

## 🧠 Getting Started

### 1. Clone and Set Up

```bash
git clone https://github.com/YOUR_ORG/AI_Reception_Agent.git
cd AI_Reception_Agent

conda create -n ai_agent python=3.8 -y
conda activate ai_agent

pip install -r requirements.txt
pip install -r rasa_requirements.txt
```

### 2. Run Locally with Docker

```bash
docker compose up --build
```

Services:
- `http://localhost:7860` → Gradio UI
- `http://localhost:5005` → Rasa
- `http://localhost:5055` → Rasa actions

---

## 🗂️ FAQ Management

Update `data/faq_data.json` to define your business units:

```json
{
  "your_org": {
    "overview": "We are a multi-brand service provider.",
    "contact": {"email": "info@example.com"},
    "companies": {
      "brand_a": {
        "name": "Brand A",
        "services": ["Training", "Inspections"],
        "locations": ["Melbourne", "Sydney"],
        "phone": "1234 5678"
      }
    }
  }
}
```

---

## 🎯 Custom Rasa Intents and Routing

Edit `domain.yml`, `rules.yml`, and `config.yml` to define how intents like `faq_services` or `faq_company_overview` are routed to the `action_query_llm`.

---

## 🧠 Local LLM Setup (LM Studio)

1. Install [LM Studio](https://lmstudio.ai)
2. Load a compatible model (e.g., Mistral-7B)
3. Enable the OpenAI-compatible server at `http://localhost:1234`
4. Ensure `agent.py` and `actions.py` are pointing to this URL

---

## 🎙️ Voice Input

Whisper is used for offline speech-to-text.

Dependencies:
- `ffmpeg`
- `torch`
- `whisper`

Microphone input is handled directly via Gradio's `Audio` component.

---

## 🧾 License

MIT License — You’re free to use, modify, and redistribute this tool.

---

## 🛠️ Contributing

Feel free to open issues or submit PRs for improvements. Add integrations (e.g., CRM, appointment booking), or extend with multilingual support.

---

Built with ❤️ for teams who want AI automation without sending data to the cloud.