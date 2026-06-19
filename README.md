# ai-agent-tools

A small DevOps monitoring agent that combines a local LLM (via [Ollama](https://ollama.com/)) with a set of system inspection tools built on [`psutil`](https://pypi.org/project/psutil/). The user asks questions in natural language (Portuguese) and the agent picks the relevant tools, collects live data from the host, and produces an analysis with recommendations.

## Features

- Interactive terminal chat loop (`main.py`).
- LLM-backed answers using `qwen2.5-coder:3b` served by Ollama.
- Five inspection tools exposed through LangChain:
  - `check_cpu` — overall and per-core CPU usage.
  - `check_memory` — RAM total/used/free/available with critical-threshold alert.
  - `check_disk` — root filesystem usage with critical-threshold alert.
  - `list_top_five_process` — top 5 processes by memory consumption.
  - `system_information` — OS, hostname, architecture, uptime.
- Keyword-based tool routing in `decide_tools` selects only the tools relevant to the question; falls back to all tools when nothing matches.
- `> 80%` usage is flagged as `⚠️ CRÍTICO`.

## Project layout

```
.
├── main.py                  # CLI entry point and chat loop
├── pyproject.toml           # Project metadata and dependencies
├── src/
│   ├── agent/
│   │   └── agent.py         # LLM client, system prompt, routing, orchestration
│   └── utils/
│       └── tools.py         # LangChain @tool implementations (psutil-backed)
└── uv.lock
```

## Requirements

- Python `>= 3.11`
- [uv](https://docs.astral.sh/uv/) for dependency management
- [Ollama](https://ollama.com/) running locally on `http://localhost:11434`
- The `qwen2.5-coder:3b` model pulled into Ollama

Python dependencies (from `pyproject.toml`):

- `langchain-core >= 1.4.8`
- `langchain-ollama >= 1.1.0`
- `psutil >= 7.2.2`

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Make sure Ollama is running and the model is available:
   ```bash
   ollama serve
   ollama pull qwen2.5-coder:3b
   ```

## Usage

Run the chat loop:

```bash
uv run python main.py
```

Then ask things like:

- `Como está o uso de CPU?`
- `Há problemas de memória?`
- `Qual é o status geral do sistema?`
- `Quais processos consomem mais memória?`

Type `sair`, `exit`, `quit`, or `q` to exit. `Ctrl+C` and `Ctrl+D` are also handled.

### Configuration

Both the Ollama model and base URL can be overridden with environment variables:

| Variable          | Default                  |
|-------------------|--------------------------|
| `OLLAMA_MODEL`    | `qwen2.5-coder:3b`       |
| `OLLAMA_BASE_URL` | `http://localhost:11434` |

## How it works

1. `agent_check(question)` receives the user's question.
2. `decide_tools(question)` matches keywords (declared in `TOOL_KEYWORDS`, e.g. `cpu`, `memória`, `disco`, `processo`, `sistema`) to one or more tools. If nothing matches, all tools are invoked.
3. Each selected tool is executed via `tool_call`, returning JSON output from `psutil`.
4. The collected data is concatenated into a context prompt with the system instructions and sent to the Ollama model.
5. The LLM response is returned to the CLI.

## Notes

- The system prompt and CLI strings are written in Portuguese.
- The Ollama base URL and model name can be overridden with the `OLLAMA_MODEL` and `OLLAMA_BASE_URL` environment variables (defaults defined in `src/agent/agent.py`).
- The "critical" threshold (`> 80%`) is centralised as `CRITICAL_USAGE_PERCENT` in `src/utils/tools.py`.
