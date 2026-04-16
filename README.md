# real_state_agent

Simple real estate agent test project with OpenAI API key loading from `.env`.

## Setup

1. Copy `.env.example` to `.env`
2. Set your key:
   - `OPENAI_API_KEY=sk-...`

## Run test interface

```bash
python real_state_agent.py
```

The CLI interface lets you quickly verify that the API key is loaded and test prompts.

## Run tests

```bash
python -m unittest discover -s tests -q
```
