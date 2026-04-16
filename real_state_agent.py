import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"


def build_system_prompt() -> str:
    return (
        "You are a helpful real estate assistant. Ask concise follow-up questions when needed, "
        "and provide practical property recommendations based on the user's budget, location, "
        "property type, and preferences."
    )


def build_user_prompt(user_request: str) -> str:
    return f"User request: {user_request}\n\nRespond with clear recommendations and next steps."


def build_chat_payload(user_request: str, model: str = "gpt-4o-mini") -> dict[str, Any]:
    return {
        "model": model,
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": build_user_prompt(user_request)},
        ],
    }


def request_openai_completion(
    api_key: str,
    payload: dict[str, Any],
    timeout_seconds: int = 30,
    endpoint: str = OPENAI_CHAT_COMPLETIONS_URL,
) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        endpoint,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def generate_real_estate_response(user_request: str, api_key: str | None = None, model: str = "gpt-4o-mini") -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required. Set the environment variable or pass api_key explicitly.")

    payload = build_chat_payload(user_request=user_request, model=model)
    response = request_openai_completion(api_key=key, payload=payload)
    return response["choices"][0]["message"]["content"]


def generate_real_state_response(user_request: str, api_key: str | None = None, model: str = "gpt-4o-mini") -> str:
    return generate_real_estate_response(user_request=user_request, api_key=api_key, model=model)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python real_state_agent.py \"I need a 2-bedroom apartment in Madrid under 400k\"")
        return 1

    request_text = " ".join(sys.argv[1:]).strip()
    try:
        answer = generate_real_estate_response(request_text)
        print(answer)
        return 0
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    except (HTTPError, URLError, KeyError, IndexError, json.JSONDecodeError) as error:
        print(f"OpenAI request failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
