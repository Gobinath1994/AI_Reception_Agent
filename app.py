"""
app.py

This module defines the web interface for the AI Receptionist Chatbot
built for Johnston Group Australia. It uses Gradio to provide a user-friendly
chat interface that supports both text and voice inputs.

Key Features:
-------------
- Provides a chat interface using Gradio Blocks
- Accepts both text and microphone input
- Uses Whisper to transcribe audio
- Uses Rasa to handle intent classification and conversation flow
- Calls a local Mistral language model via LM Studio to generate responses
- Displays chat history as styled HTML "chat bubbles"
- Runs fully containerized using Docker

Workflow:
---------
1. User types or speaks a query.
2. If voice is used, Whisper transcribes it to text.
3. Text is passed to Rasa via `handle_intent`.
4. If needed, `action_query_llm` triggers an LLM call via `agent.py`.
5. Bot's reply is displayed in the Gradio chat UI.

Run this file inside the Docker 'ui' container:
    docker compose up

Then visit:
    http://localhost:7860

"""

import gradio as gr  # Import Gradio for building the web UI
from agent import handle_intent, reset_chat  # Import response handler and reset function
from whisper_utils import transcribe_audio  # Function to transcribe audio input
import numpy as np  # Required for audio array handling

# Maintain session chat history
chat_history = []

def chat_with_agent(user_text):
    """Handle text input from the user and return the assistant's reply."""
    response = handle_intent(user_text)
    chat_history.append(("User", user_text))
    chat_history.append(("Assistant", response))
    return format_chat(chat_history), ""

def handle_audio_input(audio):
    """Handle microphone input: transcribe, then process like text."""
    if audio is not None:
        transcript = transcribe_audio(audio)
        return chat_with_agent(transcript)
    else:
        return format_chat([("Assistant", "❗ Please speak or type your question.")]), ""

def format_chat(history):
    """Convert raw chat history into styled HTML bubbles for display."""
    formatted = ""
    for sender, message in history:
        if sender == "User":
            formatted += (
                f"<div style='text-align:right; margin: 6px;'>"
                f"<span style='background:#007bff;color:white;padding:10px 14px;border-radius:16px;display:inline-block;'>"
                f"{message}</span></div>"
            )
        else:
            formatted += (
                f"<div style='text-align:left; margin: 6px;'>"
                f"<span style='background:#f1f0f0;padding:10px 14px;border-radius:16px;display:inline-block;'>"
                f"{message}</span></div>"
            )
    return formatted

# Define the Gradio UI layout and behavior
with gr.Blocks(css="""
    .chat-input textarea {
        height: 46px !important;
        font-size: 16px;
        border-radius: 24px;
        padding: 10px;
    }
    .gradio-container {max-width: 800px; margin: auto;}
    .input-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .mic-button {
        background: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        height: 42px;
        width: 30px;
        font-size: 20px;
        text-align: center;
        line-height: 42px;
        cursor: pointer;
    }
""") as demo:
    gr.Markdown("## 🤖 AI Receptionist Chatbot — Johnston Group")

    chatbot = gr.HTML(value=format_chat(chat_history))

    with gr.Row(elem_classes=["input-row"]):
        text_input = gr.Textbox(
            placeholder="Type your message and press Enter...",
            lines=1,
            show_label=False,
            elem_classes=["chat-input"],
            scale=9
        )
        mic_button = gr.Audio(
            sources=["microphone"],
            type="numpy",
            label=None,
            show_label=False,
            visible=True,
            interactive=True,
            elem_id="mic-btn",
            scale=1
        )

    text_input.submit(fn=chat_with_agent, inputs=text_input, outputs=[chatbot, text_input])
    mic_button.change(fn=handle_audio_input, inputs=mic_button, outputs=[chatbot, text_input])

# Run the app within Docker on all interfaces
demo.launch(server_name="0.0.0.0", server_port=7860)