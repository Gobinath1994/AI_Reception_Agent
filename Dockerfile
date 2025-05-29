# Use official Python 3.8 slim base image (minimal and stable for Rasa + LLM)
FROM python:3.8-slim

# ---------------------------------------------------------
# Set working directory inside the container
# ---------------------------------------------------------
WORKDIR /app

# ---------------------------------------------------------
# Install system-level dependencies needed for building wheels
# and for some libraries like Whisper or h5py
# ---------------------------------------------------------
RUN apt-get update && apt-get install -y \
    gcc \                            
    g++ \
    make \
    pkg-config \
    libhdf5-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------
# Copy all files from host into /app in container
# ---------------------------------------------------------
COPY . /app

# ---------------------------------------------------------
# Upgrade pip and install Python dependencies
# ---------------------------------------------------------
RUN pip install --upgrade pip \
    && pip install openai \
    && pip install -r rasa_requirements.txt \
    && pip install -r requirements.txt

# ---------------------------------------------------------
# Train the Rasa model (so it's ready at container start)
# ---------------------------------------------------------
RUN rasa train


# ---------------------------------------------------------
# Default container start command — runs Rasa API server
# Other services override this in docker-compose.yml
# ---------------------------------------------------------
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]