import os
from pathlib import Path
from typing import Callable


ENV_KEY_NAME = "OPENAI_API_KEY"


def load_env_file(env_path: str = ".env") -> None:
    """Load simple KEY=VALUE pairs from an env file without overriding existing env vars."""
    path = Path(env_path)
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_openai_api_key(env_path: str = ".env") -> str:
    load_env_file(env_path)
    key = os.getenv(ENV_KEY_NAME)
    if not key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Create a .env file (or copy .env.example) "
            "and set OPENAI_API_KEY=<your_key>."
        )
    return key


def mask_key(key: str) -> str:
    if len(key) <= 8:
        return "*" * len(key)
    return f"{key[:4]}...{key[-4:]}"


def run_test_interface(
    env_path: str = ".env",
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Small CLI interface to verify env key loading and test prompts."""
    output_fn("=== Real State Agent Test Interface ===")

    try:
        get_openai_api_key(env_path)
        output_fn("API key loaded successfully.")
    except ValueError as exc:
        output_fn(str(exc))
        return

    while True:
        prompt = input_fn("Describe the property request (or type 'exit'): ").strip()
        if prompt.lower() in {"exit", "quit", "q"}:
            output_fn("Goodbye!")
            break
        if not prompt:
            output_fn("Please write a valid request.")
            continue
        output_fn(f"Test request received: {prompt}")


if __name__ == "__main__":
    run_test_interface()
