import os
import os
import openai
from dotenv import load_dotenv
import tiktoken

load_dotenv()

class ClaudeService:
    def __init__(self):
        # Retrieve necessary Azure OpenAI API setup from environment variables
        openai.api_type = "openai"  # azure / openai
        openai.api_version = "2024-10-21"
        openai.api_key = os.environ["OPENAI_API_KEY"]  # use openai key for openai api
        # Model name should match your Azure configuration
        self.model_name = "gpt-4o"

        # Load environment variables
        self.speech_key = os.environ.get("SPEECH_KEY")
        self.speech_region = os.environ.get("SPEECH_REGION")

    def modify_mermaid_code(self, system_prompt: str, data: dict, api_key: str | None = None) -> str:
        """
        Makes an API call to Claude and returns the response.

        Args:
            system_prompt (str): The instruction/system prompt
            data (dict): Dictionary of variables to format into the user message
            api_key (str | None): Optional custom API key

        Returns:
            str: Claude's response text
        """
        # Create the user message with the data
        user_message = self._format_user_message(data)

        response = openai.chat.completions.create(
            model=self.model_name,
            max_tokens=4096,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},  # Initial system prompt
                {"role": "user", "content": user_message}  # User prompt
            ]
        )
        # print(response)
        # Get and return the content of the assistant's reply
        assistant_response = response.choices[0].message.content.strip()
        return assistant_response    

    # autopep8: off
    def _format_user_message(self, data: dict[str, str]) -> str:
        """Helper method to format the data into a user message"""
        parts = []
        for key, value in data.items():
            if key == 'file_tree':
                parts.append(f"<file_tree>\n{value}\n</file_tree>")
            elif key == 'readme':
                parts.append(f"<readme>\n{value}\n</readme>")
            elif key == 'explanation':
                parts.append(f"<explanation>\n{value}\n</explanation>")
            elif key == 'component_mapping':
                parts.append(f"<component_mapping>\n{value}\n</component_mapping>")
            elif key == 'instructions' and value != "":
                parts.append(f"<instructions>\n{value}\n</instructions>")
            elif key == 'diagram':
                parts.append(f"<diagram>\n{value}\n</diagram>")
            elif key == 'explanation':
                parts.append(f"<explanation>\n{value}\n</explanation>")
        return "\n\n".join(parts)
    # autopep8: on


    def count_tokens(self, prompt: str) -> int:
        """
        Count the number of tokens in a prompt using OpenAI-compatible tokenizer.

        Args:
            prompt (str): The prompt text
            model (str): OpenAI model name, e.g., "gpt-3.5-turbo", "gpt-4"

        Returns:
            int: Number of tokens in the prompt
        """
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")  # fallback encoding

        # For chat models, tokens come from structured messages; this assumes a single 'user' message
        tokens_per_message = 3  # role + content formatting
        tokens_per_name = 1     # if "name" is present

        num_tokens = tokens_per_message + len(encoding.encode(prompt))
        return num_tokens
