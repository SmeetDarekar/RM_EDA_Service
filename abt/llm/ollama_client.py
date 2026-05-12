# import requests

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL = "phi3:mini"


# def call_ollama(prompt: str) -> str:
#     response = requests.post(
#         OLLAMA_URL,
#         json={
#             "model": MODEL,
#             "prompt": prompt,
#             "stream": False
#         },
#         timeout=180
#     )
#     response.raise_for_status()
#     return response.json()["response"]






# llm/ollama_client.py

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"


def call_ollama(prompt: str) -> str:
    """
    Call Ollama with a prepared prompt and return model response text.
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()
    return data.get("response", "").strip()
