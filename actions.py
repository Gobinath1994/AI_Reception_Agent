"""
actions.py

This module defines a custom Rasa action that integrates with a local
language model (Mistral 7B) served via LM Studio.

The action is triggered when an intent mapped to `action_query_llm` is detected.
It takes the user's message, sends it to the LLM, and responds with the generated output.

The local LLM API follows the OpenAI-compatible format and is expected
to be running at: http://localhost:1234/v1/chat/completions

Used by: Rasa Core → domain.yml, rules.yml
Triggered by: matched user intent in a conversation

Dependencies:
- rasa_sdk
- requests
"""

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionQueryLLM(Action):
    """
    Custom action that sends user input to a local Mistral LLM
    and returns the generated response to the user via Rasa.
    """

    def name(self) -> str:
        """
        Returns the unique name of the action.

        Returns:
            str: Name of the action as referenced in domain.yml
        """
        return "action_query_llm"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        """
        Executes the action when triggered by Rasa.

        Args:
            dispatcher (CollectingDispatcher): Rasa dispatcher to send messages back to user
            tracker (Tracker): Rasa tracker for user state and message history
            domain (dict): The domain configuration

        Returns:
            list: A list of events (usually empty unless slots are set)
        """
        # Extract the latest message from user
        user_input = tracker.latest_message.get("text")

        try:
            # Send user input to local Mistral model via OpenAI-compatible API
            response = requests.post(
                "http://localhost:1234/v1/chat/completions",  # LM Studio server
                headers={"Content-Type": "application/json"},
                json={
                    "model": "mistral-7b",  # Name must match loaded model
                    "messages": [{"role": "user", "content": user_input}]
                }
            )

            # Extract assistant's message from response
            output = response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            # Gracefully handle any errors during the API call
            output = f"Error querying the LLM: {e}"

        # Send the LLM output back to the user via Rasa dispatcher
        dispatcher.utter_message(text=output)

        return []  # No additional Rasa events
