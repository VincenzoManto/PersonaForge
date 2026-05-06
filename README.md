# PersonaForge

PersonaForge is an open-source tool that allows you to create digital clones of your friends, historical figures, or loved ones by parsing chat histories from popular messaging apps (WhatsApp, Telegram) and using them to fine-tune or prompt AI agents.

## Features

- **Multi-platform Chat Parsing**: Easily import exported chat logs from WhatsApp (`.txt`) and Telegram (`.json`).
- **Dataset Generation**: Converts raw chats into standard conversational datasets (e.g., JSONL) suitable for fine-tuning models like GPT-3.5/4, LLaMA, or Gemini.
- **Multi-Provider Support**: Built with `litellm` and `langchain`, allowing you to use your cloned persona with any AI provider (OpenAI, Anthropic, Gemini, Local models via Ollama, etc.).
- **In-Context Clones**: If you don't want to fine-tune a model, PersonaForge can extract the best few-shot examples and system prompts to simulate the persona using in-context learning.

## Installation

```bash
git clone https://github.com/yourusername/persona-forge.git
cd persona-forge
pip install -r requirements.txt
```

## Usage

1. **Export Chat**: Export your chat from WhatsApp or Telegram.
2. **Parse and Generate Dataset**:
```bash
python main.py parse --app whatsapp --file chat_export.txt --target "Target Person Name" --output dataset.jsonl
```

3. **Chat with the Persona** (using In-Context Learning):
```bash
export OPENAI_API_KEY="your_api_key"
python main.py chat --dataset dataset.jsonl --model "gpt-4-turbo"
```

## Come funziona (Italiano)

Questo strumento legge le chat estratte dalle tue app di messaggistica, isola i messaggi della persona target e di te stesso, e crea un dataset. Questo dataset può essere utilizzato per:
1. Effettuare il *fine-tuning* di un modello (creando un modello AI che parla nativamente come la persona).
2. Fornire un contesto (In-Context Learning) a un modello esistente per farlo rispondere simulando lo stile, il tono e i ricordi della persona.
