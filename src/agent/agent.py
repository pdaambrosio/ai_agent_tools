import os

from langchain_ollama import OllamaLLM

from src.utils import tools

OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

llm = OllamaLLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
)

SYSTEM_PROMPT: str = """
Você é um especialista em DevOps que monitora infraestrutura.

Você tem acesso às seguintes ferramentas para coletar informações:
1. verificar_uso_cpu() - Verifica uso de CPU
2. verificar_memoria() - Verifica uso de memória RAM
3. verificar_disco() - Verifica espaço em disco
4. listar_processos_top_5() - Lista processos com mais memória
5. informacoes_sistema() - Informações gerais do sistema

IMPORTANTE: 
- Quando perguntarem sobre o sistema, use as ferramentas para coletar dados
- Analise os dados e forneça insights
- Se uso > 80%, marque como ⚠️ crítico
- Sempre cite as ferramentas que usou
- Seja prático e direto nas recomendações

Formato esperado quando usar ferramenta:
Se a pergunta pedir para "verificar CPU", responda:
"Deixa eu verificar... verificado com a tool [nome da ferramenta aqui] ...os dados mostram que..."
"""

user_prompt_template: str = """
Use as ferramentas disponíveis para responder:

Pergunta do usuário: {pergunta}
Responda de forma clara, analise os dados coletados e forneça recomendações.
"""

def tool_call(tool_name: str) -> str:
    """
    Simulates the execution of a tool based on its name.
    In a real system, this would be done by the LangChain tools framework.
    """

    tools_map: dict = {
        "verificar_uso_cpu": tools.check_cpu,
        "verificar_memoria": tools.check_memory,
        "verificar_disco": tools.check_disk,
        "listar_processos_top_5": tools.list_top_five_process,
        "informacoes_sistema": tools.system_information
    }

    if tool_name in tools_map:
        agent_tool = tools_map[tool_name]
        return agent_tool.invoke({})
    else:
        return f"Ferramenta '{tool_name}' não encontrada"


TOOL_KEYWORDS: dict[str, tuple[str, ...]] = {
    "verificar_uso_cpu": ("cpu", "processador", "processamento"),
    "verificar_memoria": ("memória", "memoria", "ram"),
    "verificar_disco": ("disco", "armazenamento", "storage", "espaço"),
    "listar_processos_top_5": ("processo", "processos", "aplicação", "vazamento"),
    "informacoes_sistema": ("sistema", "geral", "status", "saúde"),
}


def decide_tools(question: str) -> list[str]:
    """
    Analise the question and decide which tools to use.
    Falls back to all tools when no keyword matches.
    """
    question_lower = question.lower()
    tools_to_use: list[str] = [
        name
        for name, keywords in TOOL_KEYWORDS.items()
        if any(word in question_lower for word in keywords)
    ]

    if not tools_to_use:
        tools_to_use = list(TOOL_KEYWORDS.keys())

    return tools_to_use


def agent_check(question: str) -> str:
    """
    Analise the question and decide which tools to use.
    Return the analise.
    """
    print(f"\n🤔 Analisando: {question}")
    print("⏳ Coletando dados...\n")

    necessary_tools = decide_tools(question)

    data_collected = {}
    for tool_name in necessary_tools:
        print(f" > {tool_name}...")
        result = tool_call(tool_name)
        data_collected[tool_name] = result

    data_str = "\n".join([
        f"Resultado de {name}:\n{data}"
        for name, data in data_collected.items()
    ])

    context_prompt = f"""
    {SYSTEM_PROMPT}
    
    Dados coletados do sistema:
    {data_str}
    
    Pergunta do usuário: {question}
    
    Baseado nos dados coletados, forneça uma análise completa e recomendações.
    """

    print("\n📊 Analisando dados...\n")
    response = llm.invoke(context_prompt)

    return response
