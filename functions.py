import json
import logging
import os

import requests

logger = logging.getLogger(__name__)


def _get_openrouter_headers():
    secrets_file_path = r"C:\Users\User\Desktop\secrets.json"
    api_key = None
    if os.path.exists(secrets_file_path):
        with open(secrets_file_path, "r") as f:
            secrets = json.load(f)
            api_key = secrets.get("api_key")
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set. Add it to your environment before running the app.")

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "my-ai-agent",
    }


def input_prompt(prompt, model=None, logging_on=True):
    """Send a prompt to OpenRouter and return the full generated text."""
    model_name = model or os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = _get_openrouter_headers()
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    if logging_on:
        logger.info("Sending request to OpenRouter model '%s'...", model_name)

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]

        if logging_on:
            logger.info("Response received from OpenRouter:")
            logger.info(content)

        return content

    except requests.exceptions.HTTPError as exc:
        error_details = exc.response.text if exc.response is not None else str(exc)
        raise RuntimeError(f"OpenRouter request failed: {error_details}") from exc

    except Exception as exc:
        raise RuntimeError(f"Error occurred while sending request to OpenRouter: {exc}") from exc


def stream_prompt(prompt, model=None, logging_on=True):
    """Send a prompt to OpenRouter and print the response as it streams in."""
    model_name = model or os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = _get_openrouter_headers()
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }

    if logging_on:
        logger.info("Streaming request to OpenRouter model '%s'...", model_name)

    try:
        with requests.post(url, headers=headers, json=payload, stream=True, timeout=120) as response:
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue

                if line.startswith("data: "):
                    data = line[len("data: "):].strip()
                    if data == "[DONE]":
                        break

                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0].get("delta", {}).get("content")
                        if delta:
                            print(delta, end="", flush=True)
                    except json.JSONDecodeError:
                        continue

        print()
        return None

    except requests.exceptions.HTTPError as exc:
        error_details = exc.response.text if exc.response is not None else str(exc)
        raise RuntimeError(f"OpenRouter stream failed: {error_details}") from exc

    except Exception as exc:
        raise RuntimeError(f"Error occurred while streaming from OpenRouter: {exc}") from exc
