import gradio as gr  # Import Gradio for building the web UI
from agent import handle_intent, reset_chat  # Import response handler and reset function
from whisper_utils import transcribe_audio  # Function to transcribe audio input
import numpy as np  # Required for audio array handling

# Maintain session chat history
chat_history = []

def chat_with_agent(user_text):
    """
    Processes user text input, calls agent to handle response,
    updates chat history, and returns formatted chat for display.
    """
    response = handle_intent(user_text)  # Get response from the agent logic
    chat_history.append(("User", user_text))  # Save user message
    chat_history.append(("Assistant", response))  # Save assistant response
    return format_chat(chat_history), ""  # Return formatted chat and reset input box

def handle_audio_input(audio):
    """
    Handles audio input from microphone, transcribes it using Whisper,
    then forwards the transcript as input to the chatbot.
    """
    if audio is not None:
        transcript = transcribe_audio(audio)  # Convert audio to text
        return chat_with_agent(transcript)  # Handle as text input
    else:
        # Return prompt to speak or type if audio is invalid
        return format_chat([("Assistant", "❗ Please speak or type your question.")]), ""

def format_chat(history):
    """
    Formats the chat history into styled HTML blocks (bubble style) for UI.
    User messages appear on the right; assistant messages on the left.
    """
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

# Define the Gradio UI app
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
    gr.Markdown("## 🤖 AI Receptionist Chatbot — Johnston Group")  # Title/branding

    chatbot = gr.HTML(value=format_chat(chat_history))  # Display chat bubbles

    # Input row: textbox for text + microphone for audio
    with gr.Row(elem_classes=["input-row"]):
        text_input = gr.Textbox(
            placeholder="Type your message and press Enter...",
            lines=1,
            show_label=False,
            elem_classes=["chat-input"],
            scale=9  # Take more space compared to mic
        )
        mic_button = gr.Audio(
            source="microphone",
            type="numpy",  # Matches transcribe_audio input format
            label=None,
            show_label=False,
            visible=True,
            interactive=True,
            elem_id="mic-btn",
            scale=1  # Less space than textbox
        )

    # Trigger text submission with Enter
    text_input.submit(fn=chat_with_agent, inputs=text_input, outputs=[chatbot, text_input])

    # Trigger audio processing after recording ends
    mic_button.change(fn=handle_audio_input, inputs=mic_button, outputs=[chatbot, text_input])

# Launch the app locally
demo.launch()