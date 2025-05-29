# 🤖 AI Receptionist Chatbot — Johnston Group (Rasa + LM Studio + Whisper)

This project is a multimodal, locally-hosted AI receptionist designed for Johnston Group Australia. It combines natural language understanding (NLU), local large language models (LLMs), speech-to-text (Whisper), and a custom UI.

---

## 📦 Features

- **Text + Voice Input** via Gradio UI
- **Intent Detection** using Rasa NLU
- **LLM Responses** using Mistral 7B via LM Studio (OpenAI-compatible API)
- **Audio Transcription** using Whisper
- **Custom Branding Context** for multiple companies (e.g., Liftequipt, NWTIS)
- **Dockerized** for reproducibility

---

## 🧠 Architecture

```
[User Text/Speech] → [Gradio UI] → [Rasa NLU] → [Intent]
                                     ↓
                                 [action_query_llm]
                                     ↓
                            [agent.py + LM Studio API]
                                     ↓
                                 [Mistral Model]
```

---

## 🗂️ Project Structure

```
AI_Reception_Agent_Project/
├── app.py                   # Gradio UI for chat and audio
├── agent.py                 # Brand-aware prompt manager + LLM query
├── whisper_utils.py         # Audio → text transcription via Whisper
├── actions.py               # Rasa custom action
├── domain.yml               # Intents, responses, actions
├── rules.yml                # Rules for handling intents
├── config.yml               # NLU pipeline + policies
├── requirements.txt         # Whisper + UI deps
├── rasa_requirements.txt    # Rasa SDK + server
├── Dockerfile               # Unified Docker container build
├── docker-compose.yml       # Run rasa, actions, and UI in one command
└── data/
    ├── faq_data.json        # Structured FAQs for multiple brands
    └── nlu.yml              # Rasa training examples
```

---

## 🚀 Running the Project (Locally with Docker)

### 1. ✅ Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [LM Studio](https://lmstudio.ai) running with Mistral and REST API enabled at `http://localhost:1234`

### 2. 🔧 Build and Start
```bash
docker compose build --no-cache
docker compose up
```

### 3. 🧪 Test the Chatbot
- Open browser: [http://localhost:7860](http://localhost:7860)
- Speak or type a question
- The bot answers using Rasa + LLM

---

## 🧩 FAQs

- **How does LLM integration work?**
  The `agent.py` module formats the user question and sends it to LM Studio’s `/v1/chat/completions` endpoint using the OpenAI-compatible API.

- **How is audio handled?**
  Gradio records audio and sends it as a NumPy array to Whisper for transcription.

- **What model does it use?**
  Mistral 7B GGUF format running locally through LM Studio (compatible with OpenAI API).

---

## 📬 Need Help?

Feel free to reach out for deployment support, cloud hosting, or adding new company data to the bot.