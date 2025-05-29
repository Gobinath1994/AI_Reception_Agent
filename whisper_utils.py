import whisper  # Import OpenAI's Whisper for speech-to-text
import numpy as np  # Handle audio input as NumPy arrays
import tempfile  # Create temporary files safely
import os  # For file operations like deletion

# Load the Whisper model only once for efficiency
model = whisper.load_model("base")  # Options: "tiny", "base", "small", "medium", "large"

def transcribe_audio(audio_np):
    """
    Transcribes spoken audio (NumPy format) using OpenAI Whisper.

    Parameters:
        audio_np (tuple): A tuple containing sample rate and NumPy audio array.

    Returns:
        str: The transcribed text or error message.
    """
    
    # Validate input type and structure
    if not isinstance(audio_np, tuple) or len(audio_np) != 2:
        return "⚠️ Invalid audio input."

    sample_rate, audio_data = audio_np  # Unpack audio input

    # Check if audio data is in expected format
    if not isinstance(audio_data, np.ndarray):
        return "⚠️ Audio data must be a NumPy array."

    try:
        # Create a temporary WAV file to store audio data
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            from scipy.io.wavfile import write  # Import here to reduce load time
            write(tmp.name, sample_rate, audio_data)  # Save the array as WAV
            tmp_path = tmp.name  # Store path for later reference

        # Run Whisper transcription
        result = model.transcribe(tmp_path)
        return result.get("text", "").strip()  # Return only the transcribed text

    except Exception as e:
        # Return a clean error message
        return f"⚠️ Transcription error: {str(e)}"

    finally:
        # Cleanup: delete temp file if it exists
        if os.path.exists(tmp_path):
            os.remove(tmp_path)