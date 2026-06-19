from src.agent import agent


def main():
    print("✅ Agente de Monitoramento com Ferramentas Pronto!")
    print("=" * 60)
    print("\n🤖 Agente DevOps - Analisador de Sistema")
    print("=" * 60)
    print("\nPergunta exemplos:")
    print("  • 'Como está o uso de CPU?'")
    print("  • 'Há problemas de memória?'")
    print("  • 'Qual é o status geral do sistema?'")
    print("  • 'Quais processos consomem mais memória?'")
    print("\nDigite 'sair' para finalizar\n")

    while True:
        pergunta = input("Você: ").strip()

        if pergunta.lower() == 'sair':
            print("Até logo!")
            break

        if not pergunta:
            continue

        try:
            resposta = agent.agent_check(pergunta)
            print(f"\nAgente: {resposta}\n")
        except Exception as e:
            print(f"❌ Erro: {e}")
            print("💡 Certifique-se que 'ollama serve' está rodando\n")


if __name__ == "__main__":
    main()