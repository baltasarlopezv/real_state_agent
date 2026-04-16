# real_state_agent

Minimal AI real estate agent integrated with the OpenAI API.

## Requirements

- Python 3.10+
- `OPENAI_API_KEY` environment variable

## Usage

```bash
export OPENAI_API_KEY="your_api_key"
python real_state_agent.py "I need a 2-bedroom apartment in Madrid under 400k"
```

The script sends your request to OpenAI Chat Completions and prints recommendations.
