"""
agent.py

This module acts as the backend logic for an AI receptionist chatbot 
representing the Johnston Group Australia. It utilizes a local 
language model (via LM Studio) to interpret and respond to user 
queries based on structured FAQ data for multiple companies 
under the Johnston Group.

Features:
- Brand detection from user queries
- Dynamic system prompt generation with company context
- Contextual chat history using Mistral model
- Fallback for unknown queries
- Resettable conversation memory
"""

import json  # Import the json module to load JSON data
from openai import OpenAI  # Import OpenAI client to communicate with the LLM API

# Load FAQ data from the JSON file and access the key for the Johnston Group
with open("data/faq_data.json") as f:
    FAQ_DATA = json.load(f)["johnston_group_australia"]

# Initialize the OpenAI client with the LM Studio server endpoint
client = OpenAI(
    base_url="http://192.168.0.14:1234/v1",  # LM Studio running locally
    api_key="not-needed"  # No real key needed for local instance
)

# Global chat history to maintain session context
chat_history = []

def detect_brand(user_input):
    """
    Detect the company brand referenced in the user input based on keyword mapping.
    Defaults to 'nwtis' if no specific keyword is matched.
    """
    brand_map = {
        "nwtis": "nwtis",
        "training": "nwtis",
        "inspection": "nwtis",
        "liftequipt": "liftequipt",
        "forklift": "liftequipt",
        "generator": "liftequipt",
        "hire": "liftequipt",
        "bbs": "bbs_forks",
        "forks": "bbs_forks",
        "oil": "nw_oil_filters",
        "filter": "nw_oil_filters"
    }

    # Check if any keyword is found in the input and return associated brand
    for keyword, brand in brand_map.items():
        if keyword in user_input.lower():
            return brand

    # Fallback if no keyword matches
    return "nwtis"

def get_system_prompt(brand):
    """
    Construct a detailed system prompt to provide context to the LLM
    based on the selected brand and available company info.
    """
    group = FAQ_DATA  # Load overall group info
    companies = group["companies"]  # All subsidiary companies
    company = companies.get(brand)  # Info for the matched brand

    # Start building the prompt with general group information
    lines = [
        "You are an AI receptionist for Johnston Group Australia.",
        "",
        f"Group Overview: {group['overview']}",
        "Contact:",
        f"- Phone: {group['contact'].get('phone', 'N/A')}",
        f"- Mobile: {group['contact'].get('mobile', 'N/A')}",
        f"- Email: {group['contact'].get('email', 'N/A')}",
        "",
        "The group includes the following companies:"
    ]

    # List each company in the group
    for key, comp in companies.items():
        lines.append(f"• {comp['name']} – {comp['overview']}")

    # Add more detailed info for the detected brand
    if company:
        lines.append("\n---\n")
        lines.append(f"Primary company for this query: {company['name']}")
        lines.append(f"Services: {', '.join(company.get('services', []))}")
        if locs := company.get("locations"):
            lines.append(f"Locations: {', '.join(locs)}")
        if company.get("phone"):
            lines.append(f"Phone: {company['phone']}")
        if company.get("email"):
            lines.append(f"Email: {company['email']}")
        if company.get("website"):
            lines.append(f"Website: {company['website']}")

    # Add instruction to not make up data
    lines.append("\nAnswer only using this data. If unsure, say: 'I'll forward your query to a team member.'")
    return "\n".join(lines)  # Join all lines into one prompt

def ask_mistral(user_input):
    """
    Send the user query along with system and history context to Mistral model
    and retrieve the assistant's response.
    """
    # Initialize system prompt only once
    if not chat_history:
        brand = detect_brand(user_input)
        system_prompt = get_system_prompt(brand)
        chat_history.append({"role": "system", "content": system_prompt})

    # Append the current user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Call the Mistral model to get a response
    response = client.chat.completions.create(
        model="mistral",
        messages=chat_history,
        max_tokens=300,
        temperature=0.5
    )

    # Extract and save the assistant's reply
    reply = response.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": reply})
    return reply

def handle_intent(user_input):
    """
    Handle user query and return an appropriate response.
    """
    return ask_mistral(user_input)

def reset_chat():
    """
    Clear chat history to reset the conversation context.
    """
    chat_history.clear()