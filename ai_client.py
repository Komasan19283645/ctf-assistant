import requests
from config import (
    LMSTUDIO_BASE_URL, LMSTUDIO_MODEL,
    OPENROUTER_BASE_URL, OPENROUTER_MODEL, OPENROUTER_API_KEY, SYSTEM_PROMPT
)


def call_api(base_url: str, model: str, messages: list, api_key: str = "") -> str:

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "max_tokens": None if model == "local-model" else 512,
        "temperature": 0 if model == "local-model" else 0.3,
    }

    response = requests.post(
        f"{base_url}/chat/completions",
        headers = headers,
        json = payload,
        timeout = None if model == "local-model" else 120
    )
    response.raise_for_status()

    """
    {
      "choices": [
        {
          "message": {
            "content": "response"
          }
        }
      ]
    }
    """
    data = response.json()
    return data["choices"][0]["message"]["content"]


def ask_local(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    return call_api(LMSTUDIO_BASE_URL, LMSTUDIO_MODEL, messages)


def ask_cloud(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    return call_api(OPENROUTER_BASE_URL, OPENROUTER_MODEL, messages, OPENROUTER_API_KEY)


def analyze_challenge(description: str, backend: str = "local") -> str:
    prompt = f"Analyze the following challenge and write the exploit:\n\n{description}"

    if backend == "local":
        return ask_local(prompt)
    return ask_cloud(prompt)