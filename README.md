
# 🤖 AI Receptionist Chatbot — Johnston Group Australia

This project is an intelligent voice- and text-enabled chatbot assistant for Johnston Group Australia, providing company-specific responses using local data and speech transcription via Whisper.

## 🏢 Supported Companies

The chatbot supports the following Johnston Group divisions:

- **NWTIS** – Training, Inspection, and Certification  
- **Liftequipt** – Forklift and Equipment Hire & Sales  
- **BBS Forks** – Material Handling Equipment  
- **NW Oil & Filter Supplies** – Industrial Oils & Filters  

All information is sourced from structured `faq_data.json` and official websites.

---

## 🔧 Features

- ✅ Voice & Text Input Support  
- ✅ Professional chat UI with speech transcription  
- ✅ Responses powered by Mistral or LM Studio  
- ✅ Brand detection to route questions contextually  
- ✅ Runs 100% locally (no API key or internet required)  
- ✅ Auto-cleanup for temporary audio files  

---

## 📦 Project Structure

```
AI_Reception_Agent/
├── app.py                   # Gradio UI interface
├── agent.py                 # Logic to query model using FAQ
├── whisper_utils.py         # Whisper audio transcription
├── data/
│   └── faq_data.json        # Company FAQs and contact info
├── requirements.txt         # Dependencies
└── README.md                # You're reading it
```

---

## 🛠️ Installation

```bash
# Clone repo
git clone https://github.com/your-org/AI_Reception_Agent.git
cd AI_Reception_Agent

# Create virtual environment
conda create -n ai_agent_env python=3.11 -y
conda activate ai_agent_env

# Install dependencies
pip install -r requirements.txt
```

---

## 🧠 Requirements

- Python 3.11+
- [Whisper](https://github.com/openai/whisper) (`base` model used)
- Gradio
- OpenAI client for local LLM (e.g., Mistral via LM Studio)
- LM Studio (for local language model server)

---

## 🚀 Run the App

```bash
# Activate environment
conda activate ai_agent_env

# Start the Gradio chatbot
python app.py
```

Visit [http://127.0.0.1:7860](http://127.0.0.1:7860) in your browser.

---

## 🎙️ Voice Input Setup

- Click on the microphone icon in the UI to record.
- Speech will be transcribed using OpenAI Whisper and responded to via the chatbot.

---

## 🧠 Customization

### ✏️ Modify FAQ

Edit `data/faq_data.json` to change or add company info.

### 🤖 Change Model

Update the model call in `agent.py`:

```python
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
```

You can use:
- Local Mistral model via LM Studio
- Claude (Anthropic)
- GPT-style API if available

---

## 🧹 Reset Chat

To clear previous messages:

```python
from agent import reset_chat
reset_chat()
```

---

## 📄 License

This project is internal and customized for Johnston Group Australia.

---

## 🤝 Contributing

Feel free to propose improvements, UI updates, or add support for online services (like stock check or live chat).

---

Built with ❤️ to streamline reception and customer experience.
