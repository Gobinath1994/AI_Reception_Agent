
---

# 🤖 AI Receptionist Chatbot

An intelligent, voice- and text-enabled chatbot assistant designed to deliver organization-specific responses using local data and offline speech transcription via Whisper.

---

## 🏢 Supported Divisions

The chatbot supports multiple business units or departments, defined in your custom FAQ dataset.
All information is sourced from structured `faq_data.json` and optionally mirrored from official documentation or internal knowledge bases.

---

## 🔧 Features

* ✅ Voice & Text Input Support
* ✅ Professional chat UI with speech transcription
* ✅ Responses powered by a local LLM (e.g., Mistral via LM Studio)
* ✅ Brand/domain detection to route context-specific responses
* ✅ Runs 100% locally — no API key or internet required
* ✅ Auto-cleanup for temporary audio files

---

## 📦 Project Structure

```
AI_Reception_Agent/
├── app.py                   # Gradio UI interface
├── agent.py                 # Logic to query model using FAQ
├── whisper_utils.py         # Whisper audio transcription
├── data/
│   └── faq_data.json        # FAQ and contact information
├── requirements.txt         # Python dependencies
└── README.md                # Project overview
```

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/your-org/AI_Reception_Agent.git
cd AI_Reception_Agent

# Create and activate environment
conda create -n ai_agent_env python=3.11 -y
conda activate ai_agent_env

# Install required packages
pip install -r requirements.txt
```

---

## 🧠 Requirements

* Python 3.11+
* [Whisper](https://github.com/openai/whisper) (uses `base` model)
* Gradio
* LM Studio or compatible local LLM server
* Optional: GPU for faster transcription or generation

---

## 🚀 Run the App

```bash
# Activate environment
conda activate ai_agent_env

# Launch chatbot
python app.py
```

Then visit: [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

## 🎙️ Voice Input Instructions

* Click the microphone icon in the UI to record your query
* Audio will be transcribed using Whisper
* The chatbot will generate a response based on the transcription

---

## 🧠 Customization

### ✏️ Edit the FAQ

Update `data/faq_data.json` to define your own departments, services, and answers.

### 🤖 Change the Language Model

Edit the model connection in `agent.py`:

```python
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
```

Compatible with:

* Mistral models via LM Studio
* OpenChat or Vicuna-style models
* Claude / GPT-style APIs (if preferred)

---

## 🧹 Reset the Chat

To programmatically reset the conversation:

```python
from agent import reset_chat
reset_chat()
```

---

## 📄 License

MIT License — You’re free to use, adapt, and redistribute this tool for internal or commercial purposes.

---

## 🤝 Contributing

Contributions are welcome! Add new features, improve the UI, or suggest integrations (e.g., CRM, live support, appointment booking).

---

Built with ❤️ to streamline receptionist tasks and improve user experience — 100% offline, customizable, and privacy-focused.

---
